#!/usr/bin/env bash
# F4 paso 4: adoptar el catálogo (marcador de procedencia) — el "dueño" del curador.
set -uo pipefail
export HOME=/opt/data
cd /opt/data
H=/opt/hermes/.venv/bin/hermes

echo "=== adopt --all-unmanaged --dry-run ==="
$H curator adopt --all-unmanaged --dry-run 2>&1 | head -12
echo
echo "=== adopt real (--yes) ==="
$H curator adopt --all-unmanaged --yes 2>&1 | tail -6
echo
echo "=== estado despues ==="
$H curator status 2>&1 | head -8
echo
echo "=== unmanaged restantes ==="
$H curator list-unmanaged 2>&1 | head -4
