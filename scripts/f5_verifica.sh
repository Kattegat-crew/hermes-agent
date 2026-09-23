#!/usr/bin/env bash
# F5 · verificación previa a archivar: webhook borrado + referencias vivas.
set -uo pipefail
R=/root/hermes-agent

echo "=== 1) el webhook temporal sigue existiendo? ==="
docker exec -u 10000 hermes-agent python3 - <<'PY'
import json, urllib.request
from pathlib import Path
tok = Path('/opt/data/.env').read_text(encoding='utf-8').split('DISCORD_BOT_TOKEN=', 1)[1].split('\n', 1)[0].strip()
req = urllib.request.Request('https://discord.com/api/v10/channels/1552059363500228618/webhooks')
req.add_header('Authorization', 'Bot %s' % tok)
with urllib.request.urlopen(req, timeout=30) as r:
    hooks = json.loads(r.read().decode())
print('  webhooks en #sistema-servers ahora: %d' % len(hooks))
for h in hooks:
    print('   - id=%s nombre=%s' % (h['id'], h.get('name')))
PY

echo
echo "=== 2) quien referencia todavía /root/.agents/skills ==="
crontab -l 2>/dev/null | grep -c "\.agents/skills" | sed 's/^/  crons root: /'
grep -rl "\.agents/skills" /etc/cron.d /root/hermes-agent/scripts 2>/dev/null | head -5 | sed 's/^/  script: /'
echo "  (el propio árbol /root/.agents/rules/*.md se archiva con él)"

echo
echo "=== 3) data/skills: ¿alguien lo referencia? ==="
grep -rl "hermes-agent/data/skills\|data/skills\b" "$R/scripts" 2>/dev/null | head -5 | sed 's/^/  script: /'
echo "  --- contenido: $(find $R/data/skills -name SKILL.md 2>/dev/null | wc -l) SKILL.md, $(du -sh $R/data/skills 2>/dev/null | cut -f1)"

echo
echo "=== 4) /opt/data/skills del host: contenido ==="
ls -A /opt/data/skills
echo "  SKILL.md: $(find /opt/data/skills -name SKILL.md | wc -l)"
echo "  graphify-out: $(ls /opt/data/skills/graphify-out 2>/dev/null | head -3 | tr '\n' ' ')"

echo
echo "=== 5) el SKILL.md modificado por un agente (tiktok-ingestion) ==="
cd "$R" && git diff --stat skills/specialists/hermes-internal/tiktok-ingestion/SKILL.md
git diff skills/specialists/hermes-internal/tiktok-ingestion/SKILL.md | tail -12
