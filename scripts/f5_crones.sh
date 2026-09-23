#!/usr/bin/env bash
# F5 paso 3: repuntar los 2 crons de Meta Ads a la ruta del canon, verificar
# que quedaron bien y limpiar el webhook temporal de la prueba.
set -uo pipefail
R=/root/hermes-agent
VIEJO="/root/.agents/skills/meta-ads-discord-reporter/scripts/report.py"
NUEVO="$R/skills/specialists/marketing-ads/meta-ads-discord-reporter/scripts/report.py"
TS=$(date +%Y%m%d-%H%M%S)

[ -f "$NUEVO" ] || { echo "❌ no existe el destino: $NUEVO"; exit 1; }

echo "=== respaldo de crontab ==="
crontab -l > "$R/data/backups/crontab_${TS}.txt" && echo "  $R/data/backups/crontab_${TS}.txt"

echo
echo "=== repunte ==="
TMP=$(mktemp)
crontab -l | sed "s|$VIEJO|$NUEVO|g" > "$TMP"
n=$(grep -c "marketing-ads/meta-ads-discord-reporter" "$TMP")
m=$(grep -c "\.agents/skills/meta-ads-discord-reporter" "$TMP")
echo "  lineas apuntando al canon: $n   apuntando al arbol viejo: $m"
[ "$m" -eq 0 ] || { echo "❌ quedan referencias viejas; NO aplico"; rm -f "$TMP"; exit 1; }
crontab "$TMP" && echo "  crontab actualizada"
rm -f "$TMP"

echo
echo "=== crontab resultante (solo las lineas de reporting) ==="
crontab -l | grep "discord-reporter" | sed 's|--webhook-url "[^"]*"|--webhook-url "***"|g'

echo
echo "=== limpieza: webhook temporal ==="
docker exec -u 10000 hermes-agent python3 - <<'PY'
import json, urllib.request
from pathlib import Path
url = Path('/tmp/ops_webhook.txt').read_text(encoding='utf-8').strip()
tok = Path('/opt/data/.env').read_text(encoding='utf-8').split('DISCORD_BOT_TOKEN=', 1)[1].split('\n', 1)[0].strip()
wid = url.split('/webhooks/')[1].split('/')[0]
req = urllib.request.Request('https://discord.com/api/v10/webhooks/%s' % wid, method='DELETE')
req.add_header('Authorization', 'Bot %s' % tok)
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        print('  webhook %s borrado (status %s)' % (wid, r.status))
except Exception as e:
    print('  ⚠️ no pude borrar el webhook %s: %s' % (wid, e))
PY
