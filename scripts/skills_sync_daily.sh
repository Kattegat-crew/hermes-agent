#!/usr/bin/env bash
# DEPRECADO 23-sep-2026 (F3): medía la paridad canon ⇄ copia, que ya NO
# existe (la raíz de escritura de los 12 perfiles es el canon montado).
# Reemplazado por scripts/f3_higiene_diaria.py (cron 05:20). Se conserva
# como referencia histórica; ya no está programado.
# =============================================================================
# skills_sync_daily.sh — Corrida diaria de vigilancia (SOLO LECTURA)
#
#   1. Diagnóstico canon ⇄ espejo (por contenido) + sedimentos de los perfiles.
#   2. Persiste el JSON y, si hay algo que atender (diferencias o sedimento
#      pendiente), deja aviso MÁQUINA-LEGIBLE en data/state/skills_sync_alert.json
#      + bloque ALERTA en el log.
#   3. Refresca los consumidores del grafo.
#
# No muta skills. La promoción/resolución (--apply --firma) exige firma del dueño.
# =============================================================================
set -uo pipefail

REPO="/root/hermes-agent"
LOG="/var/log/skills-sync-check.log"
STATE="$REPO/data/state"
CHECK_JSON="$STATE/skills_sync_last.json"
ALERT_JSON="$STATE/skills_sync_alert.json"

mkdir -p "$STATE"
{
    echo ""
    echo "================================================================="
    echo "🕔 $(date '+%Y-%m-%d %H:%M:%S') — vigilancia diaria de skills"
    echo "================================================================="
} >> "$LOG"

"$REPO/scripts/sync_container_skills.sh" --check --json "$CHECK_JSON" >> "$LOG" 2>&1
CHECK_RC=$?

python3 - "$CHECK_JSON" "$ALERT_JSON" <<'PY' >> "$LOG" 2>&1 || true
import json, sys, time
src, dst = sys.argv[1], sys.argv[2]
try:
    d = json.load(open(src))
except Exception as e:
    d = {"error": f"no se pudo leer {src}: {e}"}
sed_n = d.get("sedimento_nuevas", [])
sed_r = d.get("sedimento_resiembra", [])
sed_s = d.get("sedimento_sombra", [])
atender = (not d.get("parity", False)) or bool(sed_n) or bool(sed_s) or bool(sed_r)
alerta = {
    "ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    "requiere_atencion": atender,
    "parity": d.get("parity"),
    "canon_count": d.get("canon_count"),
    "container_count": d.get("container_count"),
    "drift": d.get("drift", []),
    "drift_hint": d.get("drift_hint", {}),
    "new_in_container": d.get("new_in_container", []),
    "new_hint": d.get("new_hint", {}),
    "missing_in_container": d.get("missing_in_container", []),
    "sedimento_nuevas": sed_n,
    "sedimento_resiembra": sed_r,
    "sedimento_sombra": sed_s,
    "resolucion": {
        "paridad": "scripts/sync_container_skills.sh --apply --firma <TOKEN>",
        "sedimento": "scripts/sync_container_skills.sh --apply --firma <TOKEN> --adopt-sediment",
        "sombra": "renombrar o descartar la skill del sedimento: su nombre ya vive en el canon",
        "resiembra": "re-siembra bundled (anterior al ultimo commit): revisar y, si procede, purgar el sedimento",
    },
}
json.dump(alerta, open(dst, "w"), indent=2, ensure_ascii=False)
if atender:
    print("🚨 ALERTA: hay algo que atender ->", dst)
    print(json.dumps(alerta, indent=2, ensure_ascii=False))
else:
    print("✅ paridad por contenido y sedimentos limpios.")
PY

if grep -q '"requiere_atencion": true' "$ALERT_JSON" 2>/dev/null; then
    echo "🚨 hay algo que atender (exit check=$CHECK_RC) — detalle en $ALERT_JSON" >> "$LOG"
else
    echo "✅ OK (exit check=$CHECK_RC)" >> "$LOG"
fi

# Frescura del grafo (SOUL §8 lo consulta; la copia era manual)
"$REPO/scripts/sync_graph_consumers.sh" >> "$LOG" 2>&1 || echo "⚠️ sync_graph_consumers devolvió error" >> "$LOG"

exit 0
