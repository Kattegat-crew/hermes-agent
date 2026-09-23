# Cadena de respaldo — diseño propuesto (F-Resp)

**Fecha:** 23-sep-2026 · **Autor:** Roshi · **Estado:** propuesta, espera decisión del CTO
**Origen:** los hallazgos A1/A2/A5 escalados el 23-sep y la reserva del revisor independiente
(R8) sobre material de reversión que solo vivía en disco.

---

## 1. Diagnóstico en una línea

Hoy el respaldo **dice que sí, sube 2,56 MB y no guarda nada que importe**; su destino tiene el
token muerto. Son **tres fallos apilados**, y el peor no es el token: es que **el panel miente**.

| # | Qué pasa | Evidencia |
|---|---|---|
| A2 | El destino está caído desde hace días | `oauth2: invalid_grant ... The token was issued for a different client id` en `/var/log/vps-master-backup.log` (03:30 diario) |
| A1 | Aunque subiera, no lleva lo que importa | Último manifiesto: `total_files: 361`, `total_bytes_mb: 2.56`, `databases: []`, `agent_brains: []`. El script cita **18 rutas `/opt/hermes/data/*` que ya no existen** (más `/opt/docker`, `/opt/vps-brain`) |
| A5 | El semáforo miente | La corrida imprime `ESTADO: FAILED` y **el manifiesto que escribe dice `"status": "SUCCESS"`**, y notifica a Discord/ActivePieces "exitosamente" |

## 2. Diseño: cinco capas

### Capa 0 · Declaración de fuentes (la que hoy no existe)

Un fichero único **`data/backup-sources.yaml`** con lo que *debe* entrar, por clase:

- **Identidad y llaves:** `data/config.yaml`, `data/profiles/*/config.yaml`, `data/.env`,
  `data/secrets/`, `data/backup-keys/`, `data/home/.config/rclone/`
- **Bases de datos:** `state.db` (y por perfil), `kanban.db`, `projects.db`, `response_store.db`,
  `verification_evidence.db`, `home/.engram/engram.db`
- **Conocimiento:** `data/brain/`, `skills/` (ya está en git, se incluye por completitud)
- **Código operativo:** `data/scripts/` **fuentes** (`*.py`, `*.sh`, `*.js`: 283 ficheros, 2,4 MB)
- **Mensajería:** `data/whatsapp/session/` (9 MB)
- **Contenido:** `data/workspace/`, `data/drafts/`, `data/personajes/` *(decisión del CTO)*

Y **exclusiones explícitas**, para que nadie tenga que adivinar:
`.cache` (4.638 MB), `data/archive` (3.048 MB), `data/backups` (139 MB), `data/logs` (74 MB),
`data/checkpoints` (430 MB), `data/composio-linux-x64` (345 MB), `data/bin` (126 MB),
`state.db.malformed-backup-*` (197 MB), `*.mp4`/`*.zip` de staging.

**Por qué:** el script actual lleva la lista *dentro del código*, y cuando el árbol se movió la
lista se quedó apuntando a rutas muertas **sin que nadie se enterara**. Declararla aparte permite
que un verificador la compare con la realidad.

### Capa 1 · Snapshot LOCAL (la red que siempre funciona)

`restic` a un repositorio **local** (`/root/hermes-backups/restic-local`), retención 7 diarios /
4 semanales / 3 mensuales. Sin red, sin tokens, sin excusas: **siempre hay una copia en el mismo
disco**. Hoy el único destino es remoto, así que cuando OneDrive cayó **no quedó nada**.

### Capa 2 · Copia off-site

`restic copy` del snapshot local al destino remoto (`rclone:onedrive:Backups/.250`) — solo sube
los objetos que faltan, así que el costo diario es incremental. **Requiere tu re-autenticación:**
`rclone config reconnect onedrive:`.
Candidato a segundo destino: el bundle que ya viaja por `scp` a `169.58.189.222`
(`/root/hermes-backups/gateway-mirror/`) — aprovechar ese canal evita depender de un solo proveedor.

### Capa 3 · Prueba de entrega + estado honesto (aquí muere A5)

1. Tras escribir, **leer de vuelta** el snapshot en el destino (`restic snapshots` / `ls` contra el
   remoto) y comprobar que existe y tiene ≥ N ficheros.
2. El **manifiesto se deriva del resultado real**: `status` = lo que pasó, nunca una constante.
3. La notificación dice **FAILED y por qué** (código, salida de restic, destino), no "exitosamente".
4. **Alarma de obsolescencia:** si el último snapshot off-site correcto tiene **> 24 h**, el
   watchdog avisa. Un fallo silencioso no puede volver a esconderse detrás de una luz verde.

### Capa 4 · Auditor independiente (semanal)

Un `verify-backup.py` que **restaura de verdad** una muestra desde el destino remoto (una base de
datos + un config) a un directorio temporal y compara hashes. Es la única prueba que vale: que se
pueda **volver**. Reporta a Discord y a `data/state/backup-verify.json`.

## 3. Flujo diario propuesto (03:30)

```
[1] snapshot LOCAL (restic)                     -> si falla: FAILED + alarma, se corta
[2] leo de vuelta el snapshot local             -> prueba de entrega local
[3] restic copy -> OneDrive                     -> si falla: FAILED, el local queda (no se pierde el dia)
[4] leo de vuelta el snapshot en OneDrive       -> prueba de entrega off-site
[5] retencion (forget --prune 7/4/3)
[6] manifiesto con el estado REAL + notificacion (FAILED si algo fallo)

SEMANAL  restore de muestra desde OneDrive -> hash -> reporte
DIARIO   el watchdog publica: "ultimo snapshot off-site OK: hace N h" (>24 h = alarma)
```

## 4. Qué pesa de verdad (para decidir el alcance)

De los **21.504 MB** de `<repo>/data`, lo pesado es **caché, binarios y archivos históricos**:

| Bloque | MB | ¿Al respaldo? |
|---|---|---|
| `data/home` (de los cuales `.cache` = 4.638) | 7.041 | No (salvo configs puntuales) |
| `data/archive` (F52/F7/F6) | 3.048 | Una vez, aparte (no diario) |
| `data/profiles` (roshi 1.221, con `home` 840) | 1.656 | Sí, salvo `home/`, `logs/`, `lsp/` |
| `data/workspace` + `hermes-workspace` | 2.464 | **Decisión tuya** (contenido) |
| `data/state.db` | 859 | Sí |
| `data/drafts` | 658 | **Decisión tuya** |
| `data/checkpoints` | 430 | No |
| `data/composio-linux-x64` | 345 | No (binario reinstalable) |
| `data/brain` | 307 | Sí (conocimiento) |
| `state.db.malformed-backup-20260816` | 197 | No (residuo de agosto) |
| `data/personajes` | 187 | **Decisión tuya** |

**Alcance recomendado:** bases de datos + configuración + llaves + conocimiento + scripts +
mensajería + (a tu elección: workspace/drafts/personajes) ≈ **1,5–4 GB** frente a 21,5 GB.
Restic deduplica y cifra: la primera subida es la cara, **después son incrementales de megas**.

## 5. Fases, con reversión y prueba en negativo

| Fase | Qué | Depende de | Prueba en negativo |
|---|---|---|---|
| **P1** | Estado honesto (A5) + prueba de entrega | nada | Simular un fallo y comprobar que **el manifiesto dice FAILED y suena la alarma** |
| **P2** | `backup-sources.yaml` + repunte de fuentes (A1) | tu decisión de alcance | Quitar una fuente a propósito → el verificador debe cantarla |
| **P3** | Snapshot local (capa 1) | nada | Borrar el repo local → el script debe fallar ruidosamente |
| **P4** | Off-site + lectura de vuelta (capa 2) | **tu re-auth de OneDrive** | Apagar la red → debe quedar el local y avisar |
| **P5** | Versionar los scripts de producción (A3) | nada | `git ls-tree origin/main` debe listarlos |
| **P6** | Auditor semanal + alarma de obsolescencia (capa 4) | P3/P4 | Envejecer el manifiesto → la alarma debe disparar |

Cada fase: respaldo antes, prueba real después, y **reversión de una línea**. Igual que en los
lotes de F6 — y con la lección de Ragnar: **toda afirmación se verifica contra el destino real**,
no contra la vista local (`git ls-tree origin/main`, `restic snapshots` remoto), porque un
`.gitignore` o un token muerto pueden hacer que "hecho" sea mentira.

## 6. Lo que necesito de ti

1. **Alcance:** ¿datos vivos (≈1,5–4 GB, recomendado) o todo `<repo>/data` (21,5 GB)?
2. **¿Entran** `workspace/`, `drafts/` y `personajes/`? (2,5–3,2 GB de contenido)
3. **Re-autenticación de OneDrive** (5 min tuyos): `rclone config reconnect onedrive:`
4. **Retención** 7/4/3 — ¿te sirve?
5. **Versionar los 2,4 MB de scripts** de `data/scripts/` en git (hoy: 283 ficheros, 0 versionados).
6. ¿**Segundo destino** off-site aprovechando el canal `scp` a `.222`?
