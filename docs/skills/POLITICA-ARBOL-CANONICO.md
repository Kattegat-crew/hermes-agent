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

## F5 · Cerrar todo lo que vivía fuera del repositorio (23-sep-2026)

### Árboles retirados

| Origen | Qué era | Destino |
|---|---|---|
| `/root/.agents/skills` | 189 SKILL.md, el mayor árbol externo; alimentaba los 2 crons de Meta Ads | `data/archive/F5_*/agents_skills.original` + tar 473 MB |
| `/opt/data/skills` (host) | 5 SKILL.md: las 4 huérfanas + `web-performance-core-vitals` + un `graphify-out` del 26-ago | `data/archive/F5_*/host_opt_data_skills.original` + tar |
| `data/skills` | residuo **y punto de montaje** de `/opt/data/skills` | restaurado (ver aviso abajo) |

Las **4 skills huérfanas** se incorporaron al canon antes de archivar:
`meta-ads-discord-reporter` → `specialists/marketing-ads/`,
`mobile-landing-optimization` → `specialists/marketing/`,
`google-sheets-crm-sync` y `twenty-crm-lead-ops` → `productivity/`.
(`web-performance-core-vitals` ya vivía en `specialists/devops-infra/`.)

### Los 2 crons de Meta Ads

Repuntados de `/root/.agents/skills/...` al canon
(`skills/specialists/marketing-ads/meta-ads-discord-reporter/scripts/report.py`),
con respaldo previo de la crontab y **prueba de entrega real ANTES de archivar**:
corrida desde la ruta nueva, como root en el host, contra un webhook **temporal** en
`#sistema-servers` — `Successfully sent report to Discord!`, rc=0 — para no publicar
nada en el canal del cliente. El webhook temporal se borró después (verificado: ya no
acepta mensajes).

### El aviso del punto de montaje (incidente del 23-sep-2026)

`data/skills` parecía residuo de la purga; en realidad es el **punto de montaje** de
`/opt/data/skills` en el namespace del contenedor. Al moverlo en el host, el montaje
quedó huérfano, `/opt/data/skills` dejó de existir y el perfil default perdió su raíz
de skills. Se restauró moviendo el directorio de vuelta (el montaje sigue pegado al
inodo). Regla que queda: **los puntos de montaje no se mueven en caliente**; su retiro
exige recrear el contenedor. El job de higiene lo detectó en la misma corrida y ahora
V1 informa la **ruta ausente**, no solo un conteo.

### Catálogos ajenos

`/neuralcrew_agent` (182 SKILL.md, PRD/TRD y `core/`) es el **catálogo del producto
nca-api**: contenedores `nca-*`. Queda FUERA del inventario de Hermes por definición
(R10): no se mezcla, no se consolida y no entra en el censo del canon.

### Cierre de D2

El inventario por grupo, con rutas, tamaños, entradas y sha256, queda publicado en
`docs/skills/INVENTARIO-ARCHIVO.md`, generado desde el disco.


## F5.2 · Retiro del árbol legado del host (23-sep-2026)

### Qué era `/opt/data` en el host

Un directorio físico **distinto** del árbol de datos del contenedor (inodos `305848` vs
`543357`; el contenedor ve `/root/hermes-agent/data` montado en su `/opt/data`). Era
híbrido, y esa mezcla es la que lo volvía peligroso:

| Parte | Contenido | Rol |
|---|---|---|
| Capa de alias | 6 symlinks al repo: `scripts`, `secrets`, `bin`, `.ssh`, `.env`, `connections-map.json` | Viva: la crontab de root la usaba |
| Carga viva | `vps-monitor.env`, `backup-keys/master-backup.key`, `home/.config/rclone/rclone.conf`, `backups/manifests` | Viva: la leen/escriben los 2 jobs de cron |
| Residuo | `venvs/`, `home/`, `profiles/` (con un perfil `rochi`), `state/`, `cron/`, `brain/`, `memories/`, `plans/`, `workspace/`, `strix-scans/`, `logs/` | Muerto: 0 referencias vivas |

82.923 ficheros / 95.496 entradas. **Sin skills propias** (0 `SKILL.md`).

### Qué se hizo

1. **Migrar la carga viva al repositorio** (`<repo>/data/…`): `vps-monitor.env`,
   `backup-keys/`, `home/.config/rclone/`, y merge de `backups/`.
2. **Repuntar la dependencia**: las 3 líneas de la crontab de root y las constantes
   `/opt/data` de `vps_health_watchdog.py` (2) y `vps_master_backup.py` (10) pasan a
   rutas del repositorio. Respaldos `.bak-f52-<ts>` de cada fichero tocado.
3. **Archivar y retirar**: tar verificado (entradas + prueba de extracto por hash) a
   `data/archive/F52_<ts>/`, y el directorio movido al archivo como `.original`.
4. **Espejo obsoleto**: `/opt/hermes/skills` del host (409 `SKILL.md`, sin ningún
   consumidor y desactualizado frente al canon) va al mismo archivo.
5. **Script muerto**: `/root/update_soul.py` (escribía en un perfil `golden-game` que no
   existe) queda declarado y archivado; no se parchea.

### Las dos reglas que quedan

- **R16 · Una sola ruta para los datos de Hermes.** En el host, todo script y job apunta
  a `<repo>/data/…`; en el contenedor, a `/opt/data/…` (que es el mismo árbol por bind).
  No se crean alias, symlinks de raíz ni segundas rutas de datos.
- **R17 · Los puntos de montaje no se mueven en caliente.** Un directorio que sea punto
  de montaje (o que comparta nombre con el árbol de datos, como `data/skills` con
  `/opt/data/skills`) no se mueve, no se renombra y no se archiva con el contenedor
  corriendo: su retiro exige recrearlo. El caso del perfil `default` es el ejemplar — su
  raíz de skills **es** el punto de montaje del árbol de datos, y por eso el incidente de
  F5 lo golpeó solo a él.

### Hallazgos abiertos que este retiro NO cierra

| # | Hallazgo | Evidencia | Estado |
|---|---|---|---|
| A1 | El backup maestro tiene **fuentes inexistentes** (`/opt/hermes/data/…`, 18 líneas) y solo respalda lo que sí existe | `manifest_*.json` → `total_files: 0`; `ls /opt/hermes/data` → no existe | **escalado al CTO** |
| A2 | El token de OneDrive dio `invalid_grant` en la corrida de las 03:30 (`ESTADO: FAILED`) | `/var/log/vps-master-backup.log` | **escalado al CTO** |
| A3 | Los scripts de producción del host viven en `data/scripts/`, que está **gitignoreado**: 0 versionado | `git ls-files data/scripts` → 0 | pendiente (F7) |
| A4 | 4 slots de gateway sin perfil (`coder`, `ragnarcho`, `rochi`, `shared`): logs detenidos desde el 1-sep | `ls data/logs/gateways/` (16) vs `data/profiles/` (12) | pendiente (F7 / N6) |
| A5 | `/etc/cron.d/hermes-gateway-fleet` usa `/opt/data/scripts/…` **dentro** del contenedor vía `docker exec`: es ruta de contenedor, no del host | `/etc/cron.d/hermes-gateway-fleet` | **correcto, no se toca** |

## F7 · Higiene de flota (23-sep-2026)

### Reglas nuevas

- **R18 · El censo manda sobre la lista.** Todo perfil que exista en disco debe
  tener su raíz de skills montada, y todo destino de skills que declare el
  compose debe estar en la lista que el job mide. Una lista escrita a mano no es
  una garantía: es un recordatorio. Se verifica con **V1b**.
- **R19 · Los catálogos ajenos se declaran en un fichero.**
  `docs/skills/catalogos-ajenos.json` es la fuente única: cualquier árbol de
  `SKILL.md` fuera del repositorio que no esté declarado ahí **bloquea** la
  vigilancia. Se verifica con **V10**.

### Chequeos nuevos en el job diario

| Chequeo | Qué hace | Prueba realizada |
|---|---|---|
| **V1b** (N1) | Compara el **censo real** de `data/profiles/` con `PERFILES` y los destinos del compose con `RAICES_CONT` | Perfil fantasma → falla con su nombre; retirado → vuelve a verde |
| **V10** (N2) | Lista negra de rutas retiradas + árboles de `SKILL.md` fuera del repo que no estén en `catalogos-ajenos.json` | Árbol fantasma → falla; retirado → verde |
| **V3 ampliado** | Además del YAML roto, detecta **claves repetidas en el mismo nivel** con un cargador estricto | 12/12 configs limpios |

### Lo que encontró la primera corrida (y se cerró)

| # | Hallazgo | Acción |
|---|---|---|
| 1 | 4 slots de gateway sin perfil (`coder`, `ragnarcho`, `rochi`, `shared`): cascarones vacíos de ago 18-20 | Retirados al archivo; `logs/gateways/` queda con los **12 vivos**. `rochi` y `ragnarcho` constan como retirados (`.deleted/` y el archivo del 22-ago) |
| 2 | `/root/archivo-optdata-20260822`: respaldo manual del árbol legado con un perfil dentro | Archivado y retirado (tar `d412f85ac3b77373`) |
| 3 | 7 árboles de skills fuera del repo **sin declarar** (ai-platform, akari, gemini/antigravity ×3, opencode ×2, landing de cliente, orca) | Declarados en `catalogos-ajenos.json` (12 entradas). Verificado: la librería de `opencode` tiene **intersección 0** con el canon — no es copia |
| 4 | `vigia` sin `AGENTS.md` (10 de 11 perfiles) | Escrito: **11/11** con `config`, `AGENTS.md`, `SOUL.md` y `memories/` |
| 5 | Cadenas de respaldo asimétricas: `default`, `roshi` y `vigia` con **0** fallbacks frente a **3** de los 9 especialistas | Alineados los 3 a `NaN-Builders → B.AI → OpenCode-Go`, con respaldo por perfil y validación estructural. Resolubilidad comprobada: los 3 nombres existen en el catálogo de cada perfil |
| 6 | «Claves duplicadas de vigía» | **Re-lectura correcta:** no eran claves YAML repetidas sino **alias de proveedor en minúscula** (`nan-builders`, `b.ai`). Retirados los 42 renglones duplicados. La hipótesis inicial («no reproducible») queda corregida |
| 7 | Symlinks rotos fuera de caché: 9 medidos desde el host | **Criterio afinado: se miden desde el contenedor**, que es quien los usa. Resultado: 3 resuelven (usaban rutas `/opt/data/...`), 1 estaba realmente roto (`lsp/bin/yaml-language-server` → perfil `rochi` borrado: repuntado) y el resto son artefactos de runtime (locks de Chrome — Chrome está corriendo — y socket de pulse) |

### Reversión de F7

| Qué | Cómo |
|---|---|
| Configs (cadenas + alias) | `data/backups/config/F7_20260923-132411/{default,roshi,vigia}.config.yaml` (sha256 verificado contra el estado previo) |
| Slots huérfanos y residuo del 22-ago | `data/archive/F7_20260923-132223/` |
| Job de vigilancia | `scripts/f3_higiene_diaria.py.bak-f7-20260923-131431` y `.bak-f7b-20260923-131854` |
| `AGENTS.md` de vigia | Es un fichero nuevo: se retira y listo |

**Nota de vigencia:** los cambios de config toman efecto en el próximo arranque
del gateway de cada perfil (el proceso tiene la config en memoria). No se
reiniciaron: el plan no lo pedía para F7 y reiniciar el gateway propio cortaría
la sesión del operador a mitad de trabajo.
