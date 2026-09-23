#!/usr/bin/env bash
# ============================================================================
# install_skill_hooks.sh — registra el gate de autoskills en los 13 configs
# ============================================================================
# Idempotente: si un config ya declara el bloque `hooks:` no lo toca.
# GATE DE FIRMA: los 12 perfiles + el default son un cambio masivo -> exige firma.
#
# USO:  ./scripts/install_skill_hooks.sh --apply --firma TOKEN
#       ./scripts/install_skill_hooks.sh                 (dry-run)
# ============================================================================
set -uo pipefail

REPO="/root/hermes-agent"
# El hook lo ejecuta el gateway DENTRO del contenedor: la ruta debe ser la que
# ve el contenedor. /root/hermes-agent no existe ahí; /host/root/hermes-agent sí
# (el compose monta / del host en /host, y uid 10000 puede leerlo — verificado).
HOOK="/host/root/hermes-agent/scripts/hooks/guard_autoskill_create.py"
SHA_FILE="/root/.sync-firma.sha256"
APPLY=0
FIRMA=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --apply) APPLY=1 ;;
    --firma) FIRMA="${2:-}"; shift ;;
    *) echo "❌ opción desconocida: $1" >&2; exit 1 ;;
  esac
  shift
done

CONFIGS=("$REPO/data/config.yaml")
for f in "$REPO"/data/profiles/*/config.yaml; do CONFIGS+=("$f"); done

echo "=== install_skill_hooks ==="
echo "hook : $HOOK"
echo "configs: ${#CONFIGS[@]}"
[[ -x "$REPO/scripts/hooks/guard_autoskill_create.py" ]] || { echo "❌ el hook no es ejecutable en el repo"; exit 1; }

BLOQUE='hooks_auto_accept: true
hooks:
  pre_tool_call:
    - matcher: '"'"'^skill_manage$'"'"'
      command: '"$HOOK"'
      timeout: 20
      fail_closed: true
'

if [[ $APPLY -eq 0 ]]; then
  echo ""
  echo "🧪 DRY-RUN — se añadiría este bloque al final de cada config que no lo tenga:"
  printf '%s\n' "$BLOQUE"
  for c in "${CONFIGS[@]}"; do
    if grep -qE '^hooks:' "$c" 2>/dev/null; then echo "   = ya tiene hooks: $(basename "$(dirname "$c")")"
    else echo "   + añadir a $(basename "$(dirname "$c")")"; fi
  done
  exit 0
fi

# ── GATE ────────────────────────────────────────────────────────────────────
if [[ ! -f "$SHA_FILE" ]]; then echo "🔒 GATE CERRADO — no existe $SHA_FILE" >&2; exit 1; fi
if [[ -z "$FIRMA" ]]; then echo "🔒 GATE CERRADO — falta --firma TOKEN." >&2; exit 1; fi
GOT="$(printf '%s' "$FIRMA" | sha256sum | awk '{print $1}')"
if [[ "$GOT" != "$(cat "$SHA_FILE")" ]]; then echo "❌ FIRMA INVÁLIDA." >&2; exit 1; fi
echo "✅ Firma válida."

BK="$REPO/data/backups/hooks_$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BK"
N=0
for c in "${CONFIGS[@]}"; do
  cp "$c" "$BK/$(basename "$(dirname "$c")")-config.yaml"
  if grep -qE '^hooks:' "$c" 2>/dev/null; then
    echo "   = ya declarado: $(basename "$(dirname "$c")")"
    continue
  fi
  printf '\n%s' "$BLOQUE" >> "$c"
  N=$((N+1))
  echo "   + registrado en $(basename "$(dirname "$c")")"
done
echo ""
echo "configs modificados: $N · respaldos en $BK"
echo ""
echo "→ Los hooks se registran al arrancar el gateway. Para aplicarlos:"
echo "   docker exec hermes-agent sh -c 'for s in /run/service/gateway-*/; do s6-svc -r \$s; done'"
echo "   (o reiniciar los servicios de gateway de la flota)"
