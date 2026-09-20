# Rollout del cron de guardado diario (Engram + memoria) en VPS de producción — 2026-08-24

Ejecutado en `169.58.189.222` (vmi3513784). Hermes Agent en Docker; `HERMES_HOME=/opt/data`
(symlink a `/opt/hermes/data`). Gateway multi-perfil con **un s6 gateway por perfil**
(`gateway-<perfil>`), ticker dispara los crons a la hora programada.

## Inventario real (served_profiles)

`default (Bob, admin)`, `helmer`, `jacqueline`, `nancy`, `yulieth`, `neural-admin-test`.
**No existe `roshi` en prod** (es solo del entorno staging 147.93.3.250).

## Columnas de la arquitectura

| Perfil | MCP engram | Engram físico | Variante del cron |
|---|---|---|---|
| default (Bob) | project `neuralcrew` (central) | `/opt/hermes/data/.engram/engram.db` | COMPLETA (all_projects) |
| neural-admin-test | project `neuralcrew` | central | COMPLETA |
| helmer | `--project neuralcrew-helmer` | `profiles/helmer/home/.engram/engram.db` (237 KB) | AISLADA |
| jacqueline | `--project neuralcrew-jacqueline` | `profiles/jacqueline/home/.engram/engram.db` (0 B) | AISLADA |
| yulieth | `--project neuralcrew-yulieth` | `profiles/yulieth/home/.engram/engram.db` (0 B) | AISLADA |
| nancy | `--project neuralcrew-nancy` | **NO tiene** (solo lógico sobre central) | AISLADA — pendiente crear `.engram` físico |

## Método correcto (lo que funcionó)

```bash
# 1) Desplegar el recolector en el home de cada perfil (uid del gateway = 10000)
install -m 0644 -o 10000 -g 10000 daily_session_report.py <home>/scripts/

# 2) Crear el cron DENTRO del contenedor con HERMES_HOME del perfil (¡no el CLI del host!)
docker exec -e HERMES_HOME=/opt/data/profiles/<perfil> hermes-agent hermes cron create \
  "0 23 * * *" "$PROMPT" --name guardar-diario-memoria --deliver local \
  --script daily_session_report.py --skill engram-memory-system --skill guardado-doble-memoria </dev/null

# 3) Probar SIN bloquear el SSH (el job corre el LLM, tarda 2-3 min)
nohup docker exec -e HERMES_HOME=/opt/data/profiles/<perfil> hermes-agent hermes cron run <job_id> \
  </dev/null >/tmp/cron_run_<perfil>.log 2>&1 &

# 4) Verificar desde jobs.json (no desde la salida del CLI)
python3 - <<'EOF'
import json; d=json.load(open("<home>/cron/jobs.json"))
for j in d["jobs"]:
    if j.get("name")=="guardar-diario-memoria":
        print(j.get("id"), j.get("last_status"), j.get("last_error"))
EOF
# resultado en <home>/cron/output/<job_id>/<ts>.md — leer el final para ver el resumen
```

El script `daily_session_report.py` resuelve su DB **relativa a sí mismo**
(`scripts/../state.db`), así que copiándolo a `<home>/scripts/` de cada perfil lee
automáticamente la DB de ESE perfil — la verificación de aislamiento es ejecutarlo y
ver `DB resuelta: .../profiles/<p>/state.db`.

## Prompts usados

- COMPLETA (default, neural-admin-test): busca con `mem_search(all_projects=True)`,
  topic_key estable, mem_save What/Why/Where/Learned, memoria nativa batch.
- AISLADA (helmer, jacqueline, nancy, yulieth): **"NUNCA uses all_projects=True: busca
  y guarda SOLO en tu propio proyecto Engram"** + memoria nativa solo en su MEMORY.md.

## Resultados de prueba (24/08)

| Perfil | Job ID | Resultado |
|---|---|---|
| default (Bob) | `0b7e6cd66bb2` | ok — Engram 5→8 obs (3 nuevas), sin duplicar nativa |
| helmer | `eb3a20d02998` | ok — `[SILENT]` (sin sesiones propias hoy) |
| jacqueline | `e910b79c37bd` | ok — `[SILENT]` |
| nancy | `9d8fa3715b7b` | ok — `[SILENT]` |
| yulieth | `73deb8868ced` | ok — `[SILENT]` |
| neural-admin-test | `744303976bbd` | ok (1º intento 429 → reintento ok) |

`[SILENT]` = comportamiento CORRECTO de la variante: sin sesiones de trabajo del perfil
ese día, no inventa memorias. No es un error.

## Errores cometidos y lecciones

1. Crear crons con el CLI del host (`hermes cron ...`) → el wrapper hace `docker exec`
   sin `-e HERMES_HOME` y todos los jobs cayeron en default (5 duplicados + 1 en
   default). Fix: eliminar los duplicados con `docker exec -e HERMES_HOME=... hermes
   cron remove <id>` y recrear por perfil.
2. `hermes cron create` varias veces en un mismo heredoc `bash -s` → el CLI consume el
   stdin y corta el script tras el 1er job. Fix: un comando SSH por perfil, o
   `</dev/null`.
3. `cron run` en foreground SSH → timeout a los 60s (pero el job sigue). Fix: nohup
   background + verificación por jobs.json.
4. 429 al lanzar 5 jobs en paralelo → transitorio, reintento secuencial.
5. Verificador `"all_projects=True" in prompt` daba falso positivo en los aislados
   (la cadena aparece en la prohibición "NUNCA uses"). Verificar semántica.