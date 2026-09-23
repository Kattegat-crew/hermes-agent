#!/usr/bin/env bash
# F5 paso 1: incorporar las 4 skills huérfanas del host al canon versionado.
# Destino elegido por familia (ads / paid-traffic / ops de herramientas SaaS).
set -uo pipefail
R=/root/hermes-agent
ORIG=/opt/data/skills

declara() {  # nombre destino
  local n="$1" d="$2"
  if [ ! -d "$ORIG/$n" ]; then echo "  ⚠️  $n no existe en $ORIG"; return; fi
  if [ -d "$R/skills/$d/$n" ]; then echo "  –  $n ya está en $d"; return; fi
  mkdir -p "$R/skills/$d"
  cp -a "$ORIG/$n" "$R/skills/$d/"
  echo "  ✅ $n → skills/$d/"
}

echo "=== incorporando ==="
declara meta-ads-discord-reporter  specialists/marketing-ads
declara mobile-landing-optimization specialists/marketing
declara google-sheets-crm-sync     productivity
declara twenty-crm-lead-ops        productivity

echo
echo "=== permisos del canon (grupo del runtime + setgid) ==="
for p in $R/skills/specialists/marketing-ads/meta-ads-discord-reporter \
         $R/skills/specialists/marketing/mobile-landing-optimization \
         $R/skills/productivity/google-sheets-crm-sync \
         $R/skills/productivity/twenty-crm-lead-ops; do
  [ -d "$p" ] || continue
  find "$p" -type d -exec chmod 2775 {} + 2>/dev/null
  find "$p" -type f -exec chmod 664 {} + 2>/dev/null
  chown -R 10000:10000 "$p" 2>/dev/null
  printf '  %-70s %s\n' "$(basename "$p")" "$(stat -c '%U:%G %a' "$p")"
done

echo
echo "=== visibles para el runtime? ==="
docker exec hermes-agent bash -lc 'for s in meta-ads-discord-reporter mobile-landing-optimization google-sheets-crm-sync twenty-crm-lead-ops; do printf "  %-32s %s\n" "$s" "$(find /opt/data/skills -maxdepth 3 -type d -name "$s" | head -1)"; done'

echo
echo "=== estado git del canon ==="
cd "$R" && git status --porcelain skills/ | head -8
