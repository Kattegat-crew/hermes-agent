#!/usr/bin/env bash
# F4 paso 5: verificar alcance real y apagar el driver automático en los 12.
set -uo pipefail
export HOME=/opt/data
cd /opt/data
H=/opt/hermes/.venv/bin/hermes

echo "=== status (alcance del curador) ==="
$H curator status 2>&1 | head -10
echo
echo "=== la lista de protegidas sigue pineada? ==="
for s in skill-library-ops meta-ads-ops plan; do
  printf '  %-24s %s\n' "$s" "$($H curator status 2>&1 | grep -c "$s")"
done
echo
echo "=== apagando el driver automático (enabled=false) en los 12 ==="
$H config set curator.enabled false >/dev/null 2>&1 && echo "  root OK" || echo "  root FALLO"
for p in bragi brokkr comms freyja heimdall hermodr roshi sindri ullr vigia vili; do
  $H -p $p config set curator.enabled false >/dev/null 2>&1 && echo "  $p OK" || echo "  $p FALLO"
done
echo
echo "=== consolidación apagada por defecto? ==="
$H config get curator.consolidate 2>&1 | tail -2
echo
echo "=== valores efectivos (root) ==="
python3 -c "
import yaml
d=yaml.safe_load(open('/opt/data/config.yaml',encoding='utf-8'))
print(yaml.safe_dump(d.get('curator'), allow_unicode=True))
"
