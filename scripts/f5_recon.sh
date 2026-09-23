#!/usr/bin/env bash
# F5 · censo de todo lo que vive fuera del canon.
set -uo pipefail
R=/root/hermes-agent

echo "########## 1) ARBOLES FUERA DEL CANON ##########"
for d in /root/.agents/skills /neuralcrew_agent /opt/data/skills "$R/data/skills"; do
  if [ -d "$d" ]; then
    printf '  %-42s SKILL.md=%-5s entradas=%s\n' "$d" \
      "$(find "$d" -name SKILL.md 2>/dev/null | wc -l)" "$(ls -A "$d" 2>/dev/null | wc -l)"
  else
    printf '  %-42s (no existe)\n' "$d"
  fi
done

echo
echo "########## 2) LAS 4 HUERFANAS DEL HOST ##########"
for s in google-sheets-crm-sync meta-ads-discord-reporter mobile-landing-optimization twenty-crm-lead-ops web-performance-core-vitals; do
  p="/opt/data/skills/$s"
  if [ -d "$p" ]; then
    printf '  %-32s SKILL.md=%s  archivos=%s  bytes=%s\n' "$s" \
      "$([ -f "$p/SKILL.md" ] && echo sí || echo NO)" \
      "$(find "$p" -type f | wc -l)" "$(du -sb "$p" | cut -f1)"
    head -6 "$p/SKILL.md" 2>/dev/null | sed 's/^/      /'
  else
    printf '  %-32s (no existe)\n' "$s"
  fi
  echo
done
echo "  ¿ya viven en el canon?"
for s in google-sheets-crm-sync meta-ads-discord-reporter mobile-landing-optimization twenty-crm-lead-ops web-performance-core-vitals; do
  printf '    %-32s %s\n' "$s" "$(find $R/skills -maxdepth 3 -type d -name "$s" | head -1)"
done

echo
echo "########## 3) QUIEN REFERENCIA /root/.agents/skills ##########"
grep -rl "/root/.agents/skills" /root/.agents 2>/dev/null | head -5
echo "  --- crons root ---"
crontab -l 2>/dev/null | grep -n "agents/skills" || echo "  (ninguno)"
echo "  --- otros consumidores ---"
grep -rl "\.agents/skills" /etc/cron.d /root/*.sh /root/hermes-agent/data 2>/dev/null | head -8

echo
echo "########## 4) CONTENEDORES / SERVICIOS nca-* ##########"
docker ps -a --format '{{.Names}}\t{{.Status}}' 2>/dev/null | grep -i "nca" | head -10 || echo "  (ninguno)"
