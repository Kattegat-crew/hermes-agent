#!/usr/bin/env bash
# F5 · salud tras los archivados + caza del censo de catálogos de producto.
set -uo pipefail
R=/root/hermes-agent

echo "=== 1) referencias vivas a lo archivado ==="
printf '  crons con .agents/skills : %s\n' "$(crontab -l 2>/dev/null | grep -c '\.agents/skills')"
printf '  crons con data/skills    : %s\n' "$(crontab -l 2>/dev/null | grep -c 'hermes-agent/data/skills')"
printf '  crons con host /opt/data/skills: %s\n' "$(crontab -l 2>/dev/null | grep -c ' /opt/data/skills')"
grep -rl "\.agents/skills" /etc/cron.d 2>/dev/null | sed 's/^/  cron.d: /' || true

echo
echo "=== 2) la flota sigue sana? (higiene) ==="
python3 "$R/scripts/f3_higiene_diaria.py" --sin-notificar 2>&1 | tail -12

echo
echo "=== 3) /neuralcrew_agent: qué es ==="
ls /neuralcrew_agent 2>/dev/null | head -10
echo "  SKILL.md: $(find /neuralcrew_agent -name SKILL.md 2>/dev/null | wc -l)"
find /neuralcrew_agent -maxdepth 2 -name "docker-compose*" -o -maxdepth 2 -name "*.md" 2>/dev/null | head -5
printf '  contenedores nca-*: %s\n' "$(docker ps -a --format '{{.Names}}' | grep -c '^nca-')"

echo
echo "=== 4) censo de catálogos de producto / grupos de limpieza ==="
ls "$R/data/archive/" 2>/dev/null | head -20
echo "  --- informes con la palabra censo ---"
grep -rl "censo" "$R/data/archive"/*.md "$R/docs" 2>/dev/null | head -5
grep -rln "grupo de limpieza\|grupos de limpieza\|cascarones" "$R/docs" "$R/data/state" 2>/dev/null | head -5
