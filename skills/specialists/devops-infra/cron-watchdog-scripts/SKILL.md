---
name: cron-watchdog-scripts
description: Use when creating/debugging Hermes no_agent cron watchdogs.
---
# Cron Watchdog Scripts (Hermes)

## When to use
- Creating a scheduled cron job whose script polls an API / checks a condition and should alert only on change (watchdogs, threshold alerts, exemption/publish watchers, heartbeats).
- Debugging a cron job that ran "ok" but produced no useful output, or delivered a confusing message.
- Designing `no_agent=True` script jobs vs LLM-driven jobs.

## CRITICAL: no_agent delivery semantics
In `no_agent=True` mode the scheduler delivers stdout VERBATIM:
- **Non-empty stdout** → delivered as a message to the target chat.
- **Empty stdout** → SILENT (nothing sent). This is the watchdog pattern: stay quiet when there is nothing to report.
- Non-zero exit / timeout → an error alert is sent (so a broken watchdog can't fail silently).

**Consequence:** any `print()` in the script IS a user-facing message. A transient technical failure that prints an error gets delivered as if it were a real result — the user sees garbage instead of silence.

## CRITICAL: script path must be container-relative
Hermes (v0.20.4+) bloquea el job en el scheduler si el campo `script` resuelve fuera de `HERMES_HOME/scripts/` (en contenedor: `/opt/data/scripts`, NO `/root/hermes-agent/data/scripts` — ruta del HOST). Error típico:
```
Blocked: script path resolves outside the scripts directory (/opt/data/scripts): '/root/hermes-agent/data/scripts/foo.py'
```
Fix: `hermes cron edit <job_id> --script <solo-nombre>.py` (relativo al scripts dir). No usar rutas absolutas del host en el campo `script`. Los jobs por PROMPT no tienen este guard (el agente resuelve rutas él mismo), solo los que usan `script`/`--script`.

## CRITICAL: el script se EJECUTA en el host — nunca uses rutas del contenedor dentro del código
Aunque el campo `script` deba ser relativo a `/opt/data/scripts`, el scheduler lanza el proceso desde el HOST (`/root/hermes-agent/data/scripts/`). Un `Path('/opt/data/config.yaml')` hardcodeado dentro del script lanza `FileNotFoundError` en cada corrida (caso real: `glm53_watchdog.py` falló ×2 el 27/08, ~14h sin chequeos). Fix probado: resolver rutas relativas al propio script:
```python
from pathlib import Path
SCRIPTS_DIR = Path(__file__).resolve().parent
HERMES_HOME = SCRIPTS_DIR.parent          # host: /root/hermes-agent/data — contenedor: /opt/data
cfg = (HERMES_HOME / 'config.yaml').read_text(encoding='utf-8', errors='replace')
```
Así el mismo archivo funciona idéntico desde host y contenedor. Relacionado: los run outputs en `/opt/data/cron/output/<job_id>/` quedan root-owned; si el agente (usuario `hermes`) necesita leerlos, usar `docker exec hermes-agent cat <ruta>`.

## Watchdog design rules (pitfalls learned)
0. **Instancia única cross-container: usa `flock`, NO chequeo de PID.** El mismo proceso puede existir en namespaces contenedor/host y los PID se ven distintos o no existen entre ellos — un check `ps`/pidfile falla. Patrón probado (DaviBank 28/08): `fcntl.flock(fd, LOCK_EX|LOCK_NB)` sobre un archivo compartido (`/opt/data/.../*.lock`); si falla → otra instancia viva → exit 0.
0b. **Polling vs IMAP IDLE para alertas de correo <1 min:** un cron cada 2 min es el mínimo viable; para segundos, daemon con IMAP IDLE + watchdog cron que solo verifica el flock. El scope `gmail.readonly` NO sirve para IMAP XOAUTH2 — exige `https://mail.google.com/`.
0c. **Baseline de UID al sembrar estado:** un daemon de correo que arranca sin `last_uid` debe ponerlo en `max(UID real en buzón)`, NO en 0 ni en un valor bajo — si no, re-escanea TODO el historial y dispara ráfaga de notificaciones viejas (incidente 28/08: 190+ correos). Añade blindaje temporal: ignora mensajes con fecha >24 h.
1. **Only print on REAL state change** (e.g. status flips to VALID, issue set changes). Normal "still waiting" → print nothing.
2. **Transient failures (timeout, network, API hiccup) → retry with backoff, do NOT print.** After retries, log the error to a local file (`/opt/data/cron/output/<job_id>/last_error.log`) and exit 0 silently. Keep diagnostics in a file, not in stdout.
3. **Parse robustly**: never `json.loads(stdout)` on raw subprocess output. Find the first `{` (`raw.find("{")`), slice from there, then parse. Guard for empty stdout (`start == -1`).
4. **Exit 0 always** in a watchdog — the script's exit code is not the signal; stdout is.
5. **Verify manually after creating**: run the script once with `python3 <script>` and confirm (a) silence when nothing changed, (b) message when state changed. Then check `cronjob action=list` shows `last_run_at` populated and `last_status: ok`.
6. **Check output after a run**: inspect `/opt/data/cron/output/<job_id>/` — the scheduler writes a run record per execution, including any error text. This is where "ran ok but weird" jobs reveal their real failure.

## Template
`templates/watchdog_retry_template.py` — generic retry+parse+silent-log watchdog. Copy and adapt the polling command and the state-change condition.

## Verification checklist before declaring a watchdog done
- [ ] Manual run: silent when unchanged, prints ONLY on real change
- [ ] `cronjob action=list`: job exists, schedule right, `last_status: ok` after first tick
- [ ] Output dir `/opt/data/cron/output/<job_id>/` exists and contains a run record
- [ ] Error path: transient failure → local log file, NOT stdout

## References
- `references/2026-08-18-gtin-watchdog-failure.md` — real case: GTIN exemption watcher failed silently with JSON parse error, delivered confusing message; root cause and fix.
