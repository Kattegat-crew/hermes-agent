#!/usr/bin/env bash
# F4 paso 5b: habilitar el curador SOLO para el manual y pausar el automático.
set -uo pipefail
export HOME=/opt/data
cd /opt/data
H=/opt/hermes/.venv/bin/hermes

echo "=== root: enabled=true (necesario para el run manual) ==="
$H config set curator.enabled true 2>&1 | tail -1

echo
echo "=== pausar el driver automático ==="
$H curator pause 2>&1 | tail -2

echo
echo "=== status ==="
$H curator status 2>&1 | head -6

echo
echo "=== prueba: ¿el run manual --dry-run sigue permitido con el automático pausado? ==="
timeout 900 $H curator run --dry-run --sync 2>&1 | tail -12
echo "rc=$?"
