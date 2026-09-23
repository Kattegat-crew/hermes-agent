#!/usr/bin/env bash
# F4 paso 1: opt-out del sync de bundled en los 12 perfiles + archivo del
# manifiesto auto-referencial del canon. Objetivo: procedencia HONESTA
# (unmanaged) en vez de "bundled" para todo, que es lo que deja al curador ciego.
set -uo pipefail
export HOME=/opt/data
cd /opt/data
H=/opt/hermes/.venv/bin/hermes

echo "=== help de opt-out ==="
$H skills opt-out --help 2>&1 | head -14
echo
echo "=== ANTES: procedencia ==="
$H curator usage 2>&1 | head -2
echo
echo "=== opt-out por perfil ==="
$H skills opt-out 2>&1 | tail -2
for p in bragi brokkr comms freyja heimdall hermodr roshi sindri ullr vigia vili; do
  printf '  %-9s %s\n' "$p" "$($H -p $p skills opt-out 2>&1 | tail -1)"
done
echo
echo "=== marcadores creados ==="
ls -la /opt/data/.no-bundled-skills 2>/dev/null
ls /opt/data/profiles/*/.no-bundled-skills 2>/dev/null | wc -l
