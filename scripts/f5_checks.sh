#!/usr/bin/env bash
# F5 · comprobaciones antes de archivar: webhook, equivalencia de data/skills
# con el canon, y relevancia de graphify-out.
set -uo pipefail
R=/root/hermes-agent

echo "=== 1) webhook temporal borrado? ==="
docker exec -u 10000 hermes-agent python3 -c "
import json, urllib.request
from pathlib import Path
tok = Path('/opt/data/.env').read_text(encoding='utf-8').split('DISCORD_BOT_TOKEN=',1)[1].split(chr(10),1)[0].strip()
req = urllib.request.Request('https://discord.com/api/v10/channels/1552059363500228618/webhooks')
req.add_header('Authorization', 'Bot %s' % tok)
with urllib.request.urlopen(req, timeout=30) as r:
    hooks = json.loads(r.read().decode())
print('  webhooks en el canal: %d' % len(hooks))
for h in hooks:
    print('   -', h['id'], h.get('name'))
" 2>&1 | tail -6

echo
echo "=== 2) data/skills es copia exacta del canon? (muestra) ==="
n=0; iguales=0
for f in $(find "$R/skills" -name SKILL.md | head -40); do
  rel=${f#$R/skills/}
  g="$R/data/skills/$rel"
  n=$((n+1))
  if [ -f "$g" ]; then
    a=$(sha256sum "$f" | cut -c1-16); b=$(sha256sum "$g" | cut -c1-16)
    [ "$a" = "$b" ] && iguales=$((iguales+1))
  fi
done
echo "  muestra: $iguales de $n identicas"
echo "  --- SKILL.md solo en data/skills (no en el canon) ---"
comm -23 <(cd "$R/data/skills" && find . -name SKILL.md | sed 's|/SKILL.md||;s|^\./||' | sort) \
         <(cd "$R/skills" && find . -name SKILL.md | sed 's|/SKILL.md||' | sort) | head -10
echo "  --- SKILL.md solo en el canon ---"
comm -13 <(cd "$R/data/skills" && find . -name SKILL.md | sed 's|/SKILL.md||;s|^\./||' | sort) \
         <(cd "$R/skills" && find . -name SKILL.md | sed 's|/SKILL.md||' | sort) | head -10

echo
echo "=== 3) graphify-out del host: quién lo usa? ==="
ls -la /opt/data/skills/graphify-out/ 2>/dev/null
stat -c '  tamaño=%s fecha=%y' /opt/data/skills/graphify-out/graph.json 2>/dev/null
grep -rl "opt/data/skills/graphify-out" /root/hermes-agent/scripts /etc/cron.d /root/*.sh 2>/dev/null | head -3
echo "  --- grafo que sí usa la flota ---"
ls -la /opt/data/brain/graphify-out/graph.json 2>/dev/null || docker exec hermes-agent ls -la /opt/data/brain/graphify-out/graph.json 2>/dev/null

echo
echo "=== 4) hermes en el host? (¿algún proceso usa data/ como HERMES_HOME?) ==="
command -v hermes || echo "  (no hay binario hermes en el PATH del host)"
ps -eo args | grep -c "[h]ermes" | sed 's/^/  procesos con 'hermes' en el host: /'
