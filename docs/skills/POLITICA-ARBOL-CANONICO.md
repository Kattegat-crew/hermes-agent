# Política del árbol canónico de Skills — NeuralCrew Labs

| Campo | Valor |
|---|---|
| Documento | `docs/skills/POLITICA-ARBOL-CANONICO.md` |
| Origen | Informe `NC-2026-09-23-SK-02` Rev. 6 (Roshi) + evaluación `NC-2026-09-23-EVALUACION-RAGNOR` |
| Estado | **VIGENTE** desde el 23-sep-2026 |
| Autoridad | Jesús Díaz (CTO) · Admin: Jonathan Parra |
| Alcance | Flota Hermes DEV (12 perfiles). PROD se rige por su propia réplica (fase F8) |
| Árbol nombrado | Canon = `<repo>/skills` · Runtime = `/opt/hermes/skills` (mismo inodo desde F2) |

---

## 1. Objetivo y modelo

Un solo árbol de skills: el canon del repositorio, montado como raíz de skills del
runtime. Cero copias, cero skills fuera del control de versión, y los agentes con
capacidad real de editar lo que enriquece el catálogo.

El reparto de autoridad es el siguiente:

| Acción | Quién | Qué la protege |
|---|---|---|
| Enriquecer una skill (`patch`, `write_file`, `edit`) | El agente, sin ceremonia | git: cada edición es un diff reversible |
| Crear un fragmento nuevo | El gate de decisión (sección 4) | La skill nace en el árbol y versionada |
| Borrar, archivar por lote, fusionar familias | Firma del dueño | Gate en código + ledger con hash |
| Mantener el inventario (agrupar, proponer) | El curador, en modo propuesta | Revisión humana antes de consolidar |

**Por qué el agente puede editar:** el guard de proveniencia del runtime
(`tools/skill_manager_tool.py`) exige la marca `created_by` **solo** para `delete` y
`remove_file`; para `patch`, `write_file` y `edit` las escrituras autónomas se permiten
a propósito «so canonical fleet skills can be nourished and improved without manual
intervention». La marca de proveniencia es una decisión de **política de destrucción**,
no un permiso de escritura.

---

## 2. Invariantes (verificables con un comando)

| # | Invariante | Verificación |
|---|---|---|
| I1 | Un solo árbol físico de skills de la flota | `stat -c '%d %i'` sobre la ruta del repo y la del runtime devuelve el mismo par |
| I2 | Cero copias del catálogo (ni espejo, ni imagen, ni carpeta de perfil) | Barrido de árboles + comparación de inodo |
| I3 | Cero skills fuera del control de versión | Toda ruta de `SKILL.md` aparece en `git ls-files skills/` |
| I4 | La escritura del agente es un cambio versionado | Toda edición produce un diff en `git status` del repo |
| I5 | Un único dueño de escritura: el uid del runtime (10000), con grupo y setgid | `docker exec hermes-agent touch /opt/hermes/skills/.write-probe` exitoso |
| I6 | El gate humano solo donde el daño es irreversible | `delete`/`remove_file` y las operaciones por lote exigen firma; el enriquecimiento no |

Mientras el montaje de F2 no esté aplicado, I1, I2 e I5 están **pendientes** y el
árbol se mantiene por sincronización firmada: este documento declara esa transición en
lugar de disimularla.

---

## 3. Reglas permanentes

| # | Regla | Por qué | Cómo se verifica |
|---|---|---|---|
| R1 | Un solo árbol: el canon del repositorio. Prohibido crear copias o espejos. | Toda copia reintroduce la deriva y hace descartable el trabajo del agente. | Barrido de árboles con lista blanca + comparación de inodo |
| R2 | Los agentes enriquecen libremente; lo destructivo exige firma. | Es el diseño real del runtime y el mandato del CTO. | Ledger + gate en código para `delete` y operaciones por lote |
| R3 | Ninguna skill se borra: se archiva con respaldo y entrada en el ledger. | Las bibliotecas se degradan por poda irreversible. | Aduana + comprobación de archivo previo |
| R4 | Toda edición de agente queda versionada: commit diario con perfil y sesión de origen. | La reversibilidad es la contraparte de la libertad de escritura. | Árbol limpio al cierre del día + log del job de higiene |
| R5 | La clase de disparo cabe en los primeros 57 caracteres de la descripción. | El índice del prompt trunca ahí: fuera de esa ventana la skill es invisible. | `scripts/lint_skills_catalog.py` |
| R6 | Skill de clase, no de sesión: cuerpo rico + `references/` para el detalle. | Es la forma objetivo definida por el propio curador de Hermes. | Revisión de consolidación |
| R7 | Nomenclatura kebab-case, sin sinónimos del mismo objeto (`integration` ≠ `integrations`). | Los pares casi idénticos son el 100 % de los duplicados reales por nombre. | `scripts/lint_skills_catalog.py` |
| R8 | Consolidación automática apagada hasta dos revisiones limpias; toda fusión con revisor independiente. | Fusionar contenido sin red es irreversible en la práctica. | Estado del curador auditado |
| R9 | Toda skill con dependencia de cron se marca y se protege. | El curador no debe podar lo que un job necesita. | `docs/skills/protected-skills.json` + cruce con `data/cron/jobs.json` |
| R10 | Los catálogos de otros productos se declaran y se excluyen; nunca se mezclan. | Mezclar productos crea falsos duplicados. | Inventario con dueño por árbol |
| R11 | Toda cifra publicada lleva comando, ruta y fecha. | Sin eso no es verificable ni firmable. | Revisión previa a publicar |
| R12 | El gate humano vive en el código, con firma verificable. | El candado no puede depender de la disciplina del agente. | Token del dueño + sha256 en servidor, probado por aborto |
| R13 | Antes de crear una autoskill: validar necesidad, preferir enriquecer una existente, descartar si ya hay equivalente. Descarte por defecto. | Evita que la biblioteca crezca sin retorno. | Gate de decisión (sección 4) |
| R14 | Toda skill creada por un agente nace dentro del árbol versionado y con marca de origen. | Una autoskill fuera de git es indistinguible de un árbol externo. | `git ls-files` + campo de origen en el frontmatter |
| R15 | Las autoskills se integran a los paraguas de `core/` al tercer caso de la misma clase. Nunca se borra. | Condensar es sano; podar sin red degrada la biblioteca. | Gate de decisión + revisión periódica + ledger |

---

## 4. El pipeline de decisión de autoskills

El corpus de decisión es **exactamente `core/`**: los 19 paraguas con su `SKILL.md`,
sus ~200 `references/` y el `SKILLS_INDEX.md`. El resto del catálogo actúa solo como red
secundaria anti-duplicado, nunca como árbitro de la decisión.

Comprobaciones, en orden, y su salida:

| # | Comprobación | Salida |
|---|---|---|
| 1 | Nombre exacto contra los ficheros de `references/` de los 19 paraguas | **OMITIR** — ya está guardado; se devuelve la ruta exacta |
| 2 | Nombre exacto contra los 19 paraguas | **EDITAR** — patch al `SKILL.md` del paraguas |
| 3 | Similitud del borrador (nombre + descripción + cuerpo) contra las descripciones de los 19 y sus `references/`; mejor candidato ≥ umbral | **EDITAR** — se absorbe como `references/<caso>.md` del paraguas ganador |
| 4 | Ningún candidato supera el umbral | **CREAR** — nace en el árbol y queda candidato a paraguas al tercer caso de su clase |

**Destino exacto de lo absorbido:** `skills/core/<paraguas>/references/<caso>.md`.

**Métrica oficial:** similitud coseno **TF-IDF, umbral 0,45**, medida sobre nombre +
descripción + cuerpo, publicada con comando, ruta y fecha (referencia del 22-sep-2026:
85 pares / 45 grupos / 115 skills, 16,0 %). La cifra del informe del 21-sep (491 / 73 /
312) no es reproducible y queda descartada.

**Criterio de fusión (2 de 3):** (i) mismo disparador de entrada; (ii) solape
confirmado por la métrica oficial; (iii) mismo dueño y misma fase del flujo.

**Anatomía obligatoria del paraguas:** `SKILL.md` = clase + criterio de decisión +
checklist · `references/<caso>.md` = procedimiento íntegro de cada caso absorbido ·
`scripts/` = comandos repetibles · `templates/` = moldes.

---

## 5. El gate de firma

- Archivo del dueño: `/root/.sync-firma.sha256` (`root:root`, `0600`). Contiene el
  sha256 de un token secreto. **Un agente nunca lo crea, ni lo lee, ni lo guarda.**
- Scripts que lo exigen: `scripts/sync_container_skills.sh` y
  `scripts/f0_rescate_direccional.py`.
- El aborto está probado: sin `--firma` el script sale con `exit 1` y **cero
  escrituras** (evidencia en el informe Rev. 6).

---

## 6. Skills protegidas

Fuente única: **`docs/skills/protected-skills.json`** (versionado).

**Nota de arquitectura:** `hermes curator pin <skill>` **rechaza** las skills que viven
en `skills.external_dirs` («is bundled or hub-installed — cannot pin»), verificado el
23-sep-2026. Por eso, mientras el canon sea externo, la protección es **declarativa** y
la vigila el chequeo diario. Una vez aplicado el modelo A2 (fase F3, canon como raíz de
skills de cada perfil), los pines del curador se activan sobre la misma lista.

Ninguna skill de esa lista puede aparecer como candidata a poda, archivo o
consolidación.

---

## 7. Procedimiento de rollback

| Qué | Cómo se revierte |
|---|---|
| Una edición del canon | `git revert <commit>` (o `git checkout <hash> -- <ruta>`) |
| Un lote de consolidación | Lo archivado en `data/archive/<lote>/` es restaurable por nombre |
| Un despliegue al runtime | El motor archiva antes de pisar: `data/archive/sync_<ts>/` |
| El contenedor | Tag previo de la imagen + `docker compose down && docker compose up -d` con el tag anterior |
| El canon completo | `data/archive/canon_pre_<fase>_<fecha>.tar.gz` + su `.sha256` |

---

## 8. Registro de cambios

| Fecha | Cambio |
|---|---|
| 2026-09-23 | Creación. Deriva del informe Rev. 6 y de la evaluación independiente de Ragnar, con las condiciones C1–C3 incorporadas como requisitos de fase. |

## Notas de borde verificadas (23-sep-2026)

### Gate de autoskills · D1 vs D2 en el caso homónimo

Cuando una skill absorbida tiene EXACTAMENTE el mismo nombre que su paraguas
—hoy ocurre en `core/video-reel-pipeline`, que conserva
`references/video-reel-pipeline.md`—, el nombre intentado resuelve primero por
D1 (caso de `references/`) y no por D2 (clase de `core/`). El veredicto sigue
siendo **bloquear**, con la ruta exacta en el mensaje, y la instrucción de
enriquecer el fichero existente en lugar de crear; lo único que cambia es el
texto (dice OMITIR donde el caso de clase diría EDITAR). Se deja documentado en
vez de corregir el hook en caliente: tocar el script invalida la aprobación del
allowlist en los 12 perfiles y exige un ciclo de re-aprobación con reinicio.

### Lint de catálogo dentro de la aduana (R5 / R7)

`verify_skills.py` ejecuta ahora `lint_skills_catalog.py` (fuente única del
criterio) y publica:

- **R5** como MÉTRICA: cuántas descripciones cierran su primera frase fuera de
  la ventana de 57 caracteres (línea base medida el 23-sep-2026: 321). No
  bloquea; el objetivo es que la cifra baje.
- **R7** como REGLA BLOQUEANTE para grupos NUEVOS: los grupos de nombres
  equivalentes conocidos al integrar la regla quedan en
  `data/state/nombres_equivalentes_baseline.json` y se reportan; cualquier par
  nuevo que aparezca bloquea la aduana. Así el semáforo es útil (verde hoy) y
  no se normaliza el defecto que R7 existe para evitar.

## F4 · Curador con dueño, alcance y ciclo (23-sep-2026)

### El problema que tenía el curador

Antes de F3 el canon vivía en `skills.external_dirs`, y el curador excluye por
regla dura esos árboles: su universo estaba VACÍO. Con el canon ya montado como
raíz del runtime, apareció un segundo bloqueo, más silencioso:

`get_bundled_skills_dir()` devuelve **el mismo directorio que** `get_skills_dir()`
(`/opt/data/skills`). El sync de bundled, al comparar el árbol consigo mismo,
escribía `.bundled_manifest` con las **718** entradas del catálogo → el curador
clasificaba todo como `bundled`, y por diseño no toca, ni poda, ni deja pinear
lo bundled. El catálogo estaba visible pero intocable.

### Lo que se hizo

1. **Opt-out del sync de bundled** (`hermes skills opt-out`) en los 12 perfiles:
   siembra solo las esenciales y no borra nada de lo que ya está en disco.
2. **Manifiesto auto-referencial archivado** (`data/archive/F4_manifiesto_*`).
   Efecto: `curator usage` pasa de `bundled=594` a **`bundled=0`**.
3. **Adopción del catálogo**: `hermes curator adopt --all-unmanaged --yes` —
   la procedencia del canon es una **declaración del dueño**, no una heurística.
4. **Pin de las protegidas**: 22 de las 23 de `protected-skills.json`
   (`meta-ads-discord-reporter` aún no vive en el canon: entra en F5). El pin
   era imposible mientras el árbol fuera `external_dirs`; ya es ejecutable.
5. **Driver automático neutralizado**: `curator.enabled: true` (necesario para
   el run manual) **+ `curator pause`**. El automático exige
   `enabled && !paused && intervalo vencido`, así que no puede mutar nada.
   `consolidate: false` (prune-only) por defecto.
6. **Un solo curador para un solo árbol**: el driver vive en el perfil raíz;
   los 11 perfiles quedan con `curator.enabled: false` para que nadie más
   opere sobre el árbol compartido.
7. **Ciclo semanal en seco**: `scripts/f4_curador_semanal.py` (cron lunes
   07:00) corre una revisión REAL con `--dry-run`, **no confía en la bandera**:
   compara un retrato del árbol antes/después (SKILL.md, archivo, ledger) y
   falla si algo cambió. Publica el informe en `#sistema-servers`.

### La regla de las dos revisiones

La consolidación (fusión de contenido, F6) **no se enciende** hasta acumular
**dos revisiones limpias consecutivas** (0 mutaciones, rc=0) y contar con
respaldo y firma del CTO. El job lleva el contador en
`data/state/f4_curador_last.json` (`revisiones_limpias`) y escribe
`consolidacion_autorizada: false` en cada corrida: la autorización no depende
de que nadie se acuerde.

Primera revisión: **1/2**, con 594 candidatas y 0 transiciones propuestas.
