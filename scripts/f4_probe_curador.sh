#!/usr/bin/env bash
# F4 · alcance y procedencia del curador sobre el canon ya montado.
set -uo pipefail
export HOME=/opt/data
cd /opt/data
H=/opt/hermes/.venv/bin/hermes

echo "=== 1) lista de NO gestionadas (elegibles sin marcador de procedencia) ==="
$H curator list-unmanaged 2>&1 | head -12
echo
echo "=== 2) procedencia (usage, top) ==="
$H curator usage 2>&1 | head -14
echo
echo "=== 3) manifiesto bundled del canon ==="
python3 - <<'PY'
import json
from pathlib import Path
p = Path('/opt/data/skills/.bundled_manifest')
print('existe:', p.is_file(), 'bytes:', p.stat().st_size if p.is_file() else 0)
t = p.read_text(encoding='utf-8')[:400]
print('cabecera:', t[:400])
try:
    d = json.loads(p.read_text(encoding='utf-8'))
    print('tipo:', type(d).__name__, 'entradas:', len(d) if hasattr(d, '__len__') else '?')
    if isinstance(d, dict):
        ks = list(d)[:5]
        for k in ks:
            print('  ', k, '->', json.dumps(d[k])[:120])
except Exception as e:
    print('no es JSON:', e)
PY
echo
echo "=== 4) ¿el pin funciona ahora? (prueba con una protegida) ==="
$H curator pin skill-library-ops 2>&1 | tail -3
echo
echo "=== 5) estado del curador ==="
cat /opt/data/skills/.curator_state
