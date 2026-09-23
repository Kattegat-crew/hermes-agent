#!/usr/bin/env bash
# F4 · fuente bundled, opciones de adopt y modo del curador automatico.
set -uo pipefail
export HOME=/opt/data
cd /opt/data
H=/opt/hermes/.venv/bin/hermes

echo "=== 1) get_bundled_skills_dir (¿se referencia a sí mismo?) ==="
python3 - <<'PY'
import sys
sys.path.insert(0, '/opt/hermes')
from hermes_constants import get_bundled_skills_dir, get_optional_skills_dir, get_hermes_home, get_skills_dir
for f in (get_hermes_home, get_skills_dir, get_bundled_skills_dir, get_optional_skills_dir):
    try:
        p = f()
        import os
        n = sum(1 for r, d, fl in os.walk(p) for x in fl if x == 'SKILL.md') if p.is_dir() else 0
        print('  %-28s %-45s SKILL.md=%s' % (f.__name__, p, n))
    except Exception as e:
        print('  %-28s ERROR %s' % (f.__name__, e))
PY

echo
echo "=== 2) curator adopt --help ==="
$H curator adopt --help 2>&1 | head -18
echo
echo "=== 3) curator run --help (¿hay dry-run?) ==="
$H curator run --help 2>&1 | head -18
echo
echo "=== 4) ¿el curador automatico muta por defecto? ==="
cd /root/hermes-agent 2>/dev/null || cd /opt/data
grep -rn "dry_run\|archive_after_days\|def run_curator\|auto_apply" /root/hermes-agent/agent/curator.py 2>/dev/null | head -14
