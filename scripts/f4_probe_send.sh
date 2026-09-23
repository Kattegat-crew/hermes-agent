#!/usr/bin/env bash
# Opciones de `hermes send` + canales configurados en el perfil vigia.
set -uo pipefail
H=/opt/hermes/.venv/bin/hermes
export HOME=/opt/data
cd /opt/data
echo "=== hermes send --help ==="
$H send --help 2>&1 | head -40
echo
echo "=== canales que conoce vigia ==="
$H -p vigia send --help 2>&1 | sed -n '1,30p'
echo
echo "=== channel_directory de vigia ==="
python3 - <<'PY'
import json
from pathlib import Path
for p in ['/opt/data/profiles/vigia/channel_directory.json', '/opt/data/channel_directory.json']:
    f = Path(p)
    if f.is_file():
        d = json.loads(f.read_text(encoding='utf-8'))
        print(p)
        print(json.dumps(d, indent=1, ensure_ascii=False)[:1500])
PY
echo
echo "=== bloque discord del config de vigia ==="
python3 - <<'PY'
import yaml
from pathlib import Path
d = yaml.safe_load(Path('/opt/data/profiles/vigia/config.yaml').read_text(encoding='utf-8'))
g = d.get('gateway') or {}
print(json.dumps({k: v for k, v in g.items() if 'discord' in str(k).lower() or 'channel' in str(k).lower() or 'home' in str(k).lower()}, indent=1, ensure_ascii=False)[:1200] if False else '')
import json
dis = {k: v for k, v in g.items() if isinstance(v, (str, int, bool, list, dict)) and 'discord' in k.lower()}
print(json.dumps(dis, indent=1, ensure_ascii=False)[:1500])
PY
