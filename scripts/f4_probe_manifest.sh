#!/usr/bin/env bash
# F4 · ¿el manifiesto cubre también NUESTRAS skills, y quién lo regenera?
set -uo pipefail
R=/root/hermes-agent
M=$R/skills/.bundled_manifest
echo "=== lineas del manifiesto ==="
wc -l "$M"
echo
echo "=== ¿están las nuestras (paraguas) en el manifiesto? ==="
for s in skill-library-ops hermes-fleet-operations meta-ads-ops copy-quality-es migracion-raices-skills-al-canon; do
  printf '  %-40s %s\n' "$s" "$(grep -c "^$s:" "$M")"
done
echo
echo "=== totales del canon vs manifiesto ==="
echo "  SKILL.md en el canon: $(find $R/skills -name SKILL.md | wc -l)"
echo
echo "=== quién llama al sync de bundled ==="
cd $R
grep -rn "sync_bundled_skills\|bundled_sync\|def sync" --include=*.py tools/skills_sync.py | head -10
grep -rn "from tools.skills_sync import\|import skills_sync\|sync_bundled" --include=*.py gateway/ agent/ hermes_cli/ tools/ 2>/dev/null | grep -v "tools/skills_sync.py" | grep -v test | head -12
echo
echo "=== config relacionada ==="
python3 - <<'PY'
import yaml
from pathlib import Path
d = yaml.safe_load(Path('/root/hermes-agent/data/config.yaml').read_text(encoding='utf-8'))
print('skills:', yaml.safe_dump(d.get('skills'), allow_unicode=True).strip()[:400])
for k in ('curator', 'skills_sync'):
    if k in d:
        print(k, ':', yaml.safe_dump(d[k], allow_unicode=True).strip()[:400])
PY
