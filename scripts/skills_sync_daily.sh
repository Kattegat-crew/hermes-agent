#!/usr/bin/env bash
# =============================================================================
# skills_sync_daily.sh — Corrida diaria de vigilancia (SOLO LECTURA)
#
#   1. Diagnóstico de paridad canon ⇄ espejo (por contenido) → JSON persistido.
#   2. Si hay diferencias, deja un aviso MÁQUINA-LEGIBLE para que la flota lo vea
#      (data/state/skills_sync_alert.json) + bloque ALERTA en el log.
#   3. Refresca los consumidores del grafo (copia manual que se quedaba vieja).
#
# No muta skills. La resolución (--apply) exige firma del dueño.
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

if [[ "$CHECK_RC" -eq 0 ]]; then
    echo "OK $(date '+%Y-%m-%dT%H:%M:%S%z')" > "$ALERT_JSON"
    echo "✅ paridad por contenido confirmada (exit 0)" >> "$LOG"
else
    python3 - "$CHECK_JSON" "$ALERT_JSON" <<'PY' >> "$LOG" 2>&1 || true
import json, sys, time
src, dst = sys.argv[1], sys.argv[2]
try:
    d = json.load(open(src))
except Exception as e:
    d = {"error": f"no se pudo leer {src}: {e}"}
alerta = {
    "ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    "parity": d.get("parity"),
    "canon_count": d.get("canon_count"),
    "container_count": d.get("container_count"),
    "drift": d.get("drift", []),
    "drift_hint": d.get("drift_hint", {}),
    "new_in_container": d.get("new_in_container", []),
    "new_hint": d.get("new_hint", {}),
    "missing_in_container": d.get("missing_in_container", []),
    "resolucion": "scripts/sync_container_skills.sh --apply --firma <TOKEN> (firma del dueno)",
}
json.dump(alerta, open(dst, "w"), indent=2, ensure_ascii=False)
print("🚨 ALERTA: hay diferencias pendientes ->", dst)
print(json.dumps(alerta, indent=2, ensure_ascii=False))
PY
    echo "🚨 diferencias detectadas (exit $CHECK_RC) — aviso en $ALERT_JSON" >> "$LOG"
fi

# Frescura del grafo (SOUL §8 lo consulta; la copia era manual)
"$REPO/scripts/sync_graph_consumers.sh" >> "$LOG" 2>&1 || echo "⚠️ sync_graph_consumers devolvió error" >> "$LOG"

exit 0
