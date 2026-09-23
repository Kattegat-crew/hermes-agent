#!/usr/bin/env bash
# ¿Qué perfiles tienen credenciales de Discord? ¿Hay un bot por equipo o compartido?
set -uo pipefail
echo "=== .env con DISCORD por perfil ==="
for f in /opt/data/.env /opt/data/profiles/*/.env; do
  [ -f "$f" ] || continue
  n=$(grep -c "DISCORD" "$f" 2>/dev/null)
  printf '%-46s DISCORD=%s\n' "$f" "$n"
done
echo
echo "=== claves DISCORD declaradas (sin valores) ==="
grep -ho "DISCORD[A-Z_]*" /opt/data/.env /opt/data/profiles/*/.env 2>/dev/null | sort -u
echo
echo "=== token presente? (solo si existe, sin mostrarlo) ==="
for f in /opt/data/.env /opt/data/profiles/*/.env; do
  [ -f "$f" ] || continue
  if grep -q "^DISCORD_BOT_TOKEN=..*" "$f" 2>/dev/null; then
    echo "  CON TOKEN: $f"
  fi
done
echo
echo "=== discovery de canales: channel_directory de roshi y default ==="
for f in /opt/data/profiles/roshi/channel_directory.json /opt/data/channel_directory.json; do
  [ -f "$f" ] || continue
  echo "--- $f"
  python3 -c "
import json,sys
d=json.load(open(sys.argv[1]))
p=d.get('platforms',{})
for plat,info in p.items():
    print('   ', plat, json.dumps(info, ensure_ascii=False)[:600])
" "$f"
done
