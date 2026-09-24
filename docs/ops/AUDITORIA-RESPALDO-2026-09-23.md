# Auditoría del respaldo — 23-sep-2026

**Auditor:** Roshi · **Sujeto auditado:** `data/scripts/vps_master_backup.py` (modificado hoy
19:09) + su cadena · **Origen:** Plon afirma haber resuelto los problemas de respaldo (A1/A2/A5).
**Método:** verificación contra el **destino real** y el código, no contra la afirmación.

---

## Veredicto corto

**Plon tiene razón: los tres problemas están resueltos**, y con un diseño mejor que el mínimo.
La evidencia se leyó **desde OneDrive**, no desde el disco local.

| # | Problema | Estado | Evidencia |
|---|---|---|---|
| **A2** | Destino con token muerto | ✅ **RESUELTO** | `rclone lsd onedrive:` responde y **hay 3 snapshots en el remoto**: 22-sep 19:11 · 23-sep 11:10 · **23-sep 19:01**. Además el script **refresca el token solo** (helper embebido contra Graph API que reescribe el `rclone.conf`) |
| **A1** | No respaldaba lo que importa | ✅ **RESUELTO** | `restic stats latest` **contra el remoto**: **23.073 ficheros / 2,754 GiB**. Fuentes del snapshot: `state.db`, `projects/kanban/response_store/runs_idempotency/verification_evidence`, `whatsapp/`, `profiles/`, `sessions/`, `skills/`, `config.yaml`, `.env`, `scripts/`, `/root/.engram`, `/opt/vault`, `/opt/vps-brain` |
| **A5** | El manifiesto mentía | ✅ **RESUELTO** | El script tiene una sección **"7. Integrity Invariants Validation (Honest Semaphore)"**: `final_status` se deriva de `backup_result["success"]` + invariantes (`state.db.bak` debe existir, ser `OK` y **≥ 50 MB**; volumen de restic **≥ 50 MB**), y al incumplirse **fuerza `FAILED`** y anota `integrity_reasons` en el manifiesto y en el aviso de Discord |

**Extras que añadió y no estaban pedidos:** volcado de bases de datos con `status` por base
(`OK`/`FAILED`/`ERROR`), inventario de "cerebros" y sesiones, retención 7/4/3, y el aviso a Discord
con campo de **alerta de integridad**.

## Cómo se verificó (comandos, no opiniones)

```bash
# 1. el destino vive
rclone lsd onedrive:
# 2. hay snapshots
RESTIC_PASSWORD_FILE=data/backup-keys/master-backup.key \
  restic -r rclone:onedrive:Backups/.250 snapshots      # -> 3 snapshots
# 3. el contenido está y se puede LEER desde el remoto
  restic -r rclone:onedrive:Backups/.250 stats latest   # -> 23.073 ficheros / 2,754 GiB
  restic -r rclone:onedrive:Backups/.250 ls latest | grep -E 'state.db|config.yaml'
```

Nota metodológica: la corrida de las **16:11** aún escribió `status=SUCCESS` con `files=0` — era
la mentira de A5 viva. El arreglo es **posterior** (≈19:0x), y la corrida de las **19:04** ya
reporta `files=19.939 / 2.820 MB / 2 dbs / 20 brains` con estado derivado.

## Residuos que quedan (refinamientos, no fallos)

1. **Destino único.** Solo OneDrive: si cae, el día se pierde. El auto-refresco del token reduce
   mucho el riesgo, pero un **snapshot local** (restic a disco) daría la red que no depende de
   ningún proveedor.
2. **Nadie prueba que se pueda RESTAURAR.** El snapshot se escribe y se puede listar; un
   **restore de muestra semanal** (una base + un config, con hash) sería la prueba definitiva.
3. **Sin alarma de obsolescencia.** El watchdog **no** vigila la edad del último respaldo
   (`vps_health_watchdog.py` no menciona `manifest`, `backup` ni `restic`). Si el cron muriera
   *antes* de notificar, nadie se enteraría: falta un "último snapshot off-site OK: hace N h"
   con alarma a las 24 h.
4. **`data/home/**` está excluido del respaldo** — y ahí vive justo el `rclone.conf` con el token
   de OneDrive que usa el auto-refresco. Un restaurar no traería las credenciales del destino
   (habría que re-autenticar a mano). Espejar ese fichero a una ruta respaldada lo cierra.
5. **Detalle latente:** `DATA_DIR = /opt/data if exists else <repo>/data`. Hoy es inocuo (en el
   host no existe y en el contenedor es el mismo árbol), pero si esa ruta reapareciera, el
   respaldo cambiaría de fuente en silencio. Merece un comentario o eliminarse.

## Conclusión

La cadena **funciona y dice la verdad**. Los residuos 1-3 son el diseño que propuse como capas
1, 3 y 4; los 4 y 5 son detalles. Nada de esto bloquea: el respaldo **existe, es reciente y
contiene lo que importa**.
