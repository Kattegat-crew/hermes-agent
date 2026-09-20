#!/usr/bin/env python3
"""Template de vigilante cron (no_agent) — retry + parseo robusto + silencio en fallos.
Adaptar: POLL_CMD (comando que produce la salida), condición de cambio real (do_report),
y LOG_PATH (ruta bajo /opt/data/cron/output/<job_id>/).

Reglas:
- Print SOLO en cambio real de estado → no_agent entrega stdout al usuario.
- Fallos transitorios → reintentos, luego log local, exit 0 SIN print.
"""
import subprocess, sys, json, time

POLL_CMD = ["python3", "/path/to/checker.py", "--flag"]  # ADAPTAR
WORKDIR = "/path/to/workdir"                             # ADAPTAR
LOG_PATH = "/opt/data/cron/output/<JOB_ID>/last_error.log"  # ADAPTAR job id
MAX_ATTEMPTS = 3


def poll():
    """Devuelve (status, issues) o (None, msg_error) tras agotar reintentos."""
    last_err = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            r = subprocess.run(POLL_CMD, capture_output=True, text=True,
                               timeout=120, cwd=WORKDIR)
            raw = r.stdout or ""
            start = raw.find("{")
            if start == -1:
                last_err = f"sin JSON (stdout={raw[:200]!r}, stderr={r.stderr[:200]!r}, rc={r.returncode})"
                time.sleep(5 * attempt)
                continue
            d = json.loads(raw[start:])
            return d.get("status"), d.get("issues", [])
        except subprocess.TimeoutExpired:
            last_err = "timeout 120s"
            time.sleep(5 * attempt)
        except Exception as e:
            last_err = str(e)
            time.sleep(5 * attempt)
    return None, last_err


def do_report(status, issues):
    """ADAPTAR: condición de cambio real. True → se imprime mensaje."""
    if status == "VALID":
        return True
    codes = {i.get("code") for i in issues}
    return status == "INVALID" and codes != {"KNOWN_CODE"}  # ADAPTAR


status, issues = poll()

if status is None:
    with open(LOG_PATH, "a") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} fallo: {issues}\n")
    sys.exit(0)

if do_report(status, issues):
    print(f"Estado: {status} — issues: {json.dumps(issues, ensure_ascii=False)[:600]}")
sys.exit(0)
