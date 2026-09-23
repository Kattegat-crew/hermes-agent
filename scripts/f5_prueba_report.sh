#!/usr/bin/env bash
# F5 paso 2: prueba del repunte — correr el reporte DESDE LA RUTA DEL CANON,
# como lo hace el cron (root, host), entregando al webhook TEMPORAL de operaciones
# para no publicar en el canal del cliente.
set -uo pipefail
R=/root/hermes-agent
SKILL=$R/skills/specialists/marketing-ads/meta-ads-discord-reporter/scripts/report.py

echo "=== entorno que necesita el script ==="
printf '  composio : %s\n' "$(command -v composio || echo 'NO ENCONTRADO')"
printf '  python3  : %s (%s)\n' "$(command -v python3)" "$(python3 -V 2>&1)"
printf '  script   : %s\n' "$SKILL"
[ -f "$SKILL" ] && echo "  existe   : sí" || { echo "  existe   : NO"; exit 1; }

# el webhook temporal vive dentro del contenedor: lo traigo sin mostrarlo
docker exec hermes-agent cat /tmp/ops_webhook.txt > /tmp/f5_webhook_url.txt 2>/dev/null
W=$(cat /tmp/f5_webhook_url.txt 2>/dev/null)
if [ -z "$W" ]; then echo "  ❌ no pude obtener el webhook temporal"; exit 1; fi
echo "  webhook  : temporal de #sistema-servers (oculto)"

echo
echo "=== corrida de prueba (la misma campaña del cron de las 16:00) ==="
/usr/bin/python3 "$SKILL" \
  --campaign-id "120248680832720714" \
  --account "metaads_moly-ponent" \
  --webhook-url "$W" \
  --client-name "PRUEBA F5 (canal interno)" 2>&1 | tail -12
echo "rc=$?"
