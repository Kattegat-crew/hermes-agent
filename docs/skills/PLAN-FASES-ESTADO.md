# Tablero del plan — Árbol canónico único (F0–F8)

| Campo | Valor |
|---|---|
| Documento | `docs/skills/PLAN-FASES-ESTADO.md` |
| Origen | Informe `NC-2026-09-23-SK-02` Rev. 6 (capítulo 9: fases firmables) + revisiones de ejecución del 23-sep (tarde) |
| Estado | **VIGENTE** desde el 23-sep-2026 |
| Autoridad | Jesús Díaz (CTO) · Admin: Jonathan Parra |
| Alcance | Flota Hermes DEV (12 perfiles vivos). PROD se rige por F8 |
| Método | R11: toda cifra de este documento lleva comando, ruta y fecha |

Este tablero **no reescribe** el plan: lo anota con el estado real y acomoda las
acciones nuevas que surgieron al ejecutarlo. El plan sigue siendo el Rev. 6; aquí
consta qué fases cerraron, qué deuda residual dejaron y dónde cae cada acción nueva.

---

## 1. Tablero de fases

| Fase | Estado | Evidencia / nota |
|---|---|---|
| **F0** · Congelar, respaldar y rescatar | ✅ cerrada | Rescate + promoción de las 6 ediciones huérfanas; commit con `HEAD = origin/main` |
| **F1** · Gobernanza y política permanente | ✅ cerrada | `docs/skills/POLITICA-ARBOL-CANONICO.md` vigente (R1–R15, invariantes I1–I6); `protected-skills.json` |
| **F2** · Eliminar la copia (aplicar el montaje) | ✅ cerrada | `./skills` montado; inodo único verificado |
| **F3** · Edición de agentes sobre el árbol único | ✅ cerrada | Raíz de escritura repuntada en los 12; gate `guard_autoskill_create.py` activo (`rc=2`); job de higiene diario |
| **F4** · Curador con dueño, alcance y ciclo | ✅ cerrada | `curator pause` + driver semanal en seco; adopción del catálogo; pines. Revisión limpia **1/2** (`data/state/f4_curador_last.json`) |
| **F5** · Cerrar lo que vivía fuera del repositorio | ✅ cerrada **con incidente** | 3 árboles retirados; 2 crons de Meta Ads repuntados; **incidente del punto de montaje** (`data/skills`) |
| **F5.2** · Deuda residual del cierre de F5 | ✅ **cerrada** (23-sep, 13:05) | Árbol legado del host archivado y retirado; 0 referencias vivas (ver §3.0) |
| **F6** · Consolidación supervisada | ⏸️ **bloqueada** | Exige 2 revisiones limpias del curador; hoy **1/2**. No arranca: la autorización vive en el código |
| **F7** · Higiene de flota | ⏳ pendiente | 3 ítems originales + **4 nuevos** (ver §3) |
| **F8** · PROD y verificación final | ⏳ pendiente | Se le añade una comprobación (ver §3, N9) |

---

## 2. Deudas residuales descubiertas al ejecutar (23-sep-2026, tarde)

### 2.1 La verificación de la flota es una lista escrita a mano

`scripts/f3_higiene_diaria.py` verifica el árbol con dos listas **literales**:

```python
PERFILES    = ['bragi', 'brokkr', 'comms', 'freyja', 'heimdall', 'hermodr',
               'roshi', 'sindri', 'ullr', 'vigia', 'vili']          # línea 48
RAICES_CONT = ['/opt/data/skills'] + ['/opt/data/profiles/%s/skills' % p for p in PERFILES]  # línea 51
```

El chequeo V1 recorre `RAICES_CONT`, **no el censo real**. Consecuencia medida: si nace
un perfil 13, V1 no lo ve y ese perfil escribiría en su carpeta local — una **copia
real**, violación directa de I2/I3 y de R1/R14. Hoy la foto es correcta (12/12 con
inodo `541814`), pero la garantía vive en el compose y en la disciplina, no en la
verificación.

### 2.2 El `/opt/data` del **host**: capa de alias viva + payload legado

Dentro del contenedor, `/opt/data` **es** el repo (`/root/hermes-agent/data → /opt/data`,
bind). Fuera del contenedor hay **otro** `/opt/data` físico, híbrido:

- **Capa de alias (viva):** 6 symlinks al repo — `scripts`, `secrets`, `bin`, `.ssh`,
  `.env`, `connections-map.json`. La crontab de root **depende** de ella:
  `vps_health_watchdog.py` (cada 15 min), notificación 09:00 y `vps_master_backup.py`
  (03:30) se invocan como `/opt/data/scripts/…`.
- **Payload legado (~600 MB):** `home/` 200M, `venvs/` 198M, `backups/` 7M,
  `profiles/` 4.8M (esqueletos con `cron/`, `sessions/`, `memories/`, `hooks/`,
  `state.db`; incluye un perfil **`rochi`**), `workspace/`, `strix-scans/`, `state/`,
  `brain/`, `memories/`, `plans/`, `logs/`, `_stale-20260917/`.
- **Comprobado:** sus `skills/` están **vacíos** (0 `SKILL.md`; los 17 hallazgos eran
  cachés del paquete `typer`). El `/opt/data/skills` del host sigue **ausente** (F5 bien hecho).
- **Por qué importa:** es primo del incidente de F5 — un directorio del host que parece
  residuo y tiene rol activo y **no está declarado en ninguna parte** (R10 declara
  catálogos ajenos; esto no). Un segundo `profiles/` confunde cualquier censo.

### 2.3 El censo de slots de gateway no cuadra con el de perfiles

| Censo | Valor medido |
|---|---|
| Slots en `data/logs/gateways/` | **16**: bragi, brokkr, **coder**, comms, default, freyja, heimdall, hermodr, **ragnarcho**, **rochi**, roshi, **shared**, sindri, ullr, vigia, vili |
| Perfiles en `data/profiles/` | **12**: los mismos menos `coder`, `ragnarcho`, `rochi`, `shared` |

Los 4 sin perfil tienen `logs/gateways/<slot>/` **detenidos desde el 1-sep** y **0
declaración** en config (solo aparecen en cachés de `graphify-out` y en dos scripts de
host: `phase_d_restart_cleanup.sh`, `patch_ragnarcho.sh`). El capítulo 12.2 del Rev. 6
declara 16 slots como radio de impacto de F2: **la cifra hay que corregirla**.

### 2.4 Huecos menores de expediente por perfil

`vigia` **no tiene `AGENTS.md`** (hay 10 de 11 perfiles). El perfil `default` no tiene
carpeta propia: su config, memoria y `AGENTS.md` viven en la raíz de datos.

### 2.5 Afirmaciones del plan que la medición de hoy no reproduce

- **«Claves duplicadas de vigía» (F7):** con cargador YAML estricto (falla en clave
  repetida al mismo nivel), **0 de 12** configs presentan duplicados. O la afirmación
  era de otro objeto, o ya se corrigió: pasa a *no reproducible*.
- **Symlinks rotos (F7):** 157 en crudo, de los cuales **145** son caché `uv`,
  **3** un respaldo declarado (`.bak-20260828-symlinks/`) y **9** quedan fuera de caché
  técnica — todos en `roshi`: `.chrome-profile/Singleton*` (3), `home/.local/share/uv/python/cpython-3.11…`,
  `workspace/.venv-docx/bin/python{3,3.11}` (3) y `lsp/bin/{yaml-language-server,pyright-langserver}` (2).
  Coincide con la lista del plan (Chrome, `.venv-docx`, `lsp/bin`, `.bak` de vigía).

---

## 3. Acciones acomodadas por fase

Cada acción lleva dueño de fase, riesgo, firma y criterio de aceptación. Ninguna se
ejecuta sin cerrar la anterior dentro de su fase.

### F5.2 · Deuda residual del cierre de F5

| # | Acción | Riesgo | Firma | Criterio de aceptación |
|---|---|---|---|---|
| **N3** | ✅ Declarar en la política el retiro del árbol legado y la convención de una sola ruta (`R16`) | Nulo | No | **Hecho**: `POLITICA-ARBOL-CANONICO.md` § F5.2 |
| **N4** | ✅ Quitar la dependencia viva: repuntar los 3 jobs de la crontab y las constantes `/opt/data` de los 2 scripts | Medio | Sí (CTO) | **Hecho**: `rc=0` en ambos jobs desde la ruta nueva; cron de las 13:00 corrió ya repuntado |
| **N5** | ✅ Inventariar y archivar el árbol legado (82.923 ficheros) + el espejo `/opt/hermes/skills` | Medio | Sí (CTO) | **Hecho**: tar 266 MB (`7b5acc40a70024f8`) restaurado y cotejado 1:1 (10/10 hashes) |
| **N7** | ✅ Documentar la asimetría del default | Nulo | No | **Hecho**: regla `R17` en la política |

**Orden obligatorio: N4 antes de N5.** Igual que en F5 con los crons de Meta Ads:
primero se corta la dependencia, después se archiva.

### F7 · Higiene de flota (originales + nuevos)

| # | Acción | Estado | Criterio de aceptación |
|---|---|---|---|
| **N1** | **Chequeo censo-vs-montaje (V1b)** en el job diario: comparar `/opt/data/profiles/*` contra `PERFILES` y los destinos del compose contra `RAICES_CONT` | **nuevo** | Falla si existe un perfil sin raíz montada. Probado con un perfil fantasma |
| **N2** | **Chequeo V10 «nada fuera del repo ni del alias declarado»**: rutas de skills/perfiles/estado | **nuevo** | 0 rutas no declaradas; el legado aparece como violación hasta su cierre |
| **N6** | **Reconciliar el censo de slots**: declarar vivos o residuo `coder`, `ragnarcho`, `rochi`, `shared`; limpiar sus `logs/gateways/`; corregir el cap. 12.2 del Rev. 6 | **nuevo** | 0 slots sin perfil o sin declaración; cifra del informe corregida |
| **N8** | Completar el expediente de perfil: `AGENTS.md` de **vigia** (10 de 11) | **nuevo** | 11/11 perfiles con `config`, `AGENTS.md`, `SOUL.md` y `memories/` |
| **N3-org** | Cadenas de respaldo asimétricas: `default`, `roshi` y `vigia` con **0** fallbacks frente a **3** de los otros 9 *(medido)* | original | Los 12 con cadena alineada y conmutación probada |
| **N8-org** | Claves duplicadas de vigía → **no reproducible** con detector estricto (0/12). Se integra el detector a la aduana y se cierra con nota | original (re-medido) | Detector en la aduana; semáforo verde |
| **N9-org** | Symlinks rotos fuera de caché técnica: **9**, todos en `roshi` | original (re-medido) | 0 fuera de `/.cache/` y `/.bak-*` |

### F6 · Consolidación (bloqueada — sin cambios de alcance)

- **Condición de arranque intacta:** 2 revisiones limpias consecutivas del curador
  (hoy **1/2**; la segunda cae el lunes) + firma del CTO, lote por lote.
- **Nota nueva:** el **lote 0** no debe nutrirse de nada que provenga del árbol legado
  del host ni de los slots huérfanos; el insumo de F6 es exclusivamente el canon
  versionado (722 `SKILL.md`).

### F8 · PROD

| # | Acción | Criterio de aceptación |
|---|---|---|
| **N9** | Verificar que **PROD no arrastre la misma trampa**: árbol legado, punto de montaje con nombre ambiguo, crons apuntando a árboles ajenos | Barrido documentado en PROD con comando y salida; hallazgos tratados como F5.2 |

---

### 3.0 F5.2 ejecutada (23-sep-2026, 13:00-13:05) — evidencia

| Paso | Resultado medido |
|---|---|
| Migrar carga viva | `vps-monitor.env`, `backup-keys/`, `home/.config/rclone/` copiados; `backups/` mergeado en `<repo>/data` |
| Repuntar | `vps_health_watchdog.py` 2 reemplazos · `vps_master_backup.py` 10 · crontab 3 líneas. Respaldos `.bak-f52-20260923-125926` |
| Archivar | `opt_data_legado.tar.gz` 266 MB `7b5acc40a70024f8` · `hermes_skills_host.tar.gz` 8 MB `61fde256eb690b6e` |
| Verificar archive | Restauración completa: **82.923 ficheros / 12.069 dirs / 505 symlinks** idénticos al original · 10/10 hashes OK · 17 `SKILL.md` en ambos lados |
| Retiro | `/opt/data` y `/opt/hermes/skills` **ya no existen**; `update_soul.py` (muerto) al archivo |
| Referencias vivas | crontab **0** · systemd **0** · scripts de `/root` **0** · `/etc/cron.d` 1 (**ruta de contenedor, correcta**) |
| Servicio | cron de las **13:00 ya corrió repuntado** (`/var/log/vps-watchdog.log` mtime 13:00:04); ambos jobs `rc=0` |
| Contenedor | **intacto**: 12 rutas con inodo `541814` y 722 `SKILL.md` |
| Reversión | `tar xzf data/archive/F52_20260923-130039/opt_data_legado.tar.gz -C /` + restaurar `.bak-f52-*` + `crontab data/backups/F52_20260923-125926/crontab_root.txt` |

**Hallazgos escalados al CTO (no cerrados por F5.2):**

| # | Hallazgo | Evidencia |
|---|---|---|
| A1 | El backup maestro apunta a `/opt/hermes/data/…` (18 referencias) que **no existe**: solo respalda lo que sí existe | `manifest_*.json` → `total_files: 0` |
| A2 | OneDrive devolvió `invalid_grant` en la corrida de las 03:30 → `ESTADO: FAILED` | `/var/log/vps-master-backup.log` |
| A3 | Los scripts de producción del host viven en `data/scripts/`, **gitignoreado**: 0 versionado | `git ls-files data/scripts` → 0 |
| A4 | 4 slots de gateway sin perfil (`coder`, `ragnarcho`, `rochi`, `shared`) | 16 slots vs 12 perfiles |
| A5 | Una corrida en `--dry-run` del backup reporta `ESTADO: SUCCESS` y **notifica a Discord** | salida de la verificación de F5.2 |

## 4. Orden de ejecución recomendado

```
F5.2 (N3 -> N4 -> N5)  -->  F7 (N1, N2, N6, N8 + originales)  -->  F6 (al llegar 2/2)  -->  F8
        ^                              ^
        |                              |
   reversible y quita el          corto; cabe en la espera
   riesgo vivo primero            del curador
```

**La ventana natural es la espera de F6.** F6 no puede arrancar hasta el lunes (segunda
revisión limpia del curador), y esa espera es exactamente el hueco para F5.2 y los ítems
nuevos de F7: todo es de riesgo bajo o medio, reversible, y no se pisa con la
consolidación.

---

## 5. Líneas base re-medidas (23-sep-2026)

| Medición | Comando | Resultado |
|---|---|---|
| Inodo único en las 12 raíces | `stat -c '%i %n' /opt/data/skills /opt/data/profiles/*/skills` (contenedor) | `541814` en 12/12 |
| Catálogo versionado vs alcanzable | `data/state/skills_higiene_last.json` → `V4_catalogo` | `722 = 722`, `faltan: []` |
| Rutas medidas por V1 | ídem → `V1_inodo` | `rutas: 12`, `ausentes: []` |
| Montajes del canon en compose | `grep -c 'skills:' docker-compose.yml` | 13 destinos (12 de escritura + `/opt/hermes/skills`) |
| Cadenas de respaldo | `yaml.safe_load(...)['fallback_providers']` por config | default/roshi/vigía = 0; los otros 9 = 3 |
| Duplicados de clave | cargador YAML estricto (falla en repetida) | 0/12 |
| Symlinks rotos | `find -L data/profiles -type l` | 157 crudo -> 145 caché `uv` + 3 `.bak` + **9 reales** |
| Slots de gateway | `ls data/logs/gateways/` | 16 (4 sin perfil) |
| Autorización de consolidación | `data/state/f4_curador_last.json` | `revisiones_limpias: 1`, `consolidacion_autorizada: false` |

---

## 6. Registro de cambios

| Fecha | Cambio |
|---|---|
| 2026-09-23 | Creación. Acomoda las acciones surgidas al ejecutar F0–F5 en el plan del Rev. 6: abre **F5.2** (deuda residual del cierre de F5) e incorpora **N1, N2, N6, N8** a F7 y **N9** a F8. Re-mide la línea base de F7 y marca como *no reproducible* la afirmación de claves duplicadas. |
