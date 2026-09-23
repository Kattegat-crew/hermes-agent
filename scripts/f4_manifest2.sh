#!/usr/bin/env bash
# F4 paso 2 (rutas del CONTENEDOR): archivar el manifiesto auto-referencial
# y medir la procedencia real del canon.
set -uo pipefail
export HOME=/opt/data
cd /opt/data
H=/opt/hermes/.venv/bin/hermes
TS=$(date +%Y%m%d-%H%M%S)
A=/opt/data/archive/F4_manifiesto_${TS}
M=/opt/data/skills/.bundled_manifest

mkdir -p "$A"
if [ -f "$M" ]; then
  cp "$M" "$A/bundled_manifest.bak"
  rm -f "$M"
  echo "manifiesto archivado en $A y retirado del canon ($(wc -l < "$A/bundled_manifest.bak") lineas)"
else
  echo "no habia manifiesto en $M"
fi
echo
echo "=== procedencia DESPUES ==="
$H curator usage 2>&1 | head -2
echo
echo "=== list-unmanaged ==="
$H curator list-unmanaged 2>&1 | head -6
echo
echo "=== status ==="
$H curator status 2>&1 | head -4
