#!/usr/bin/env bash
# F5 · ¿qué hermes corre en el HOST y con qué HERMES_HOME? + verificación real
# del webhook temporal (posteando: si está borrado, da 401/404).
set -uo pipefail

echo "=== procesos hermes del host (con su entorno si se puede) ==="
ps -eo pid,ppid,etime,args | grep "[h]ermes" | head -12
echo "  total: $(ps -eo args | grep -c '[h]ermes')"
echo
echo "=== HERMES_HOME de esos procesos ==="
for p in $(pgrep -f hermes | head -12); do
  hh=$(tr '\0' '\n' < /proc/$p/environ 2>/dev/null | grep '^HERMES_HOME=' | head -1)
  ar=$(tr '\0' ' ' < /proc/$p/cmdline 2>/dev/null | cut -c1-90)
  printf '  pid %-8s %-28s %s\n' "$p" "${hh:-HERMES_HOME=(no seteado)}" "$ar"
done

echo
echo "=== ¿algún /proc/*/environ menciona data/skills? ==="
grep -l "hermes-agent/data/skills" /proc/*/environ 2>/dev/null | head -5 || echo "  ninguno"

echo
echo "=== verificación del webhook temporal (posteo de prueba) ==="
W=$(cat /tmp/f5_webhook_url.txt 2>/dev/null)
if [ -z "$W" ]; then echo "  (no tengo la url guardada)"; else
python3 - "$W" <<'PY'
import json, sys, urllib.request, urllib.error
url = sys.argv[1]
req = urllib.request.Request(url, method='POST')
req.add_header('Content-Type', 'application/json')
body = json.dumps({'content': 'prueba de limpieza'}).encode()
try:
    with urllib.request.urlopen(req, data=body, timeout=25) as r:
        print('  ⚠️ el webhook SIGUE VIVO (status %s) — hay que borrarlo' % r.status)
except urllib.error.HTTPError as e:
    print('  ✅ el webhook ya no acepta mensajes (status %s) = borrado' % e.code)
except Exception as e:
    print('  ? error inesperado:', e)
PY
fi
