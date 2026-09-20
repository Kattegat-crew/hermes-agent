#!/usr/bin/env bash
# =============================================================================
# sync_graph_consumers.sh — Propaga el grafo canónico del repo a sus consumidores
#
# El repo reconstruye `graphify-out/graph.json` en segundo plano en cada commit.
# Los consumidores (SOUL §8 y los AGENTS.md de perfil) NO lo ven solos: este script
# los iguala por sha256 y reporta.
#
#   ./sync_graph_consumers.sh            -> sincroniza y verifica
#   ./sync_graph_consumers.sh --check    -> solo reporta diferencias (no copia)
# =============================================================================
set -euo pipefail

REPO="/root/hermes-agent"
ORIGEN="$REPO/graphify-out/graph.json"
CONSUMIDORES=(
    "$REPO/data/brain/graphify-out/graph.json"
    "$REPO/data/profiles/roshi/graphify-out/graph.json"
)
MODE="apply"
[[ "${1:-}" == "--check" ]] && MODE="check"

if [[ ! -f "$ORIGEN" ]]; then
    echo "❌ No existe el grafo canónico: $ORIGEN" >&2
    exit 1
fi

SRC_HASH=$(sha256sum "$ORIGEN" | awk '{print $1}')
SRC_SIZE=$(stat -c%s "$ORIGEN")
echo "🧠 Grafo canónico: graphify-out/graph.json"
echo "   sha256=${SRC_HASH:0:16}… · ${SRC_SIZE} B · $(date -r "$ORIGEN" '+%Y-%m-%d %H:%M')"

RC=0
for dst in "${CONSUMIDORES[@]}"; do
    dir=$(dirname "$dst")
    if [[ ! -d "$dir" ]]; then
        echo "   ⏭️  $dst (sin directorio de consumidor; se omite)"
        continue
    fi
    if [[ -f "$dst" ]]; then
        DST_HASH=$(sha256sum "$dst" | awk '{print $1}')
    else
        DST_HASH=""
    fi
    if [[ "$DST_HASH" == "$SRC_HASH" ]]; then
        echo "   ✅ al día: $dst"
        continue
    fi
    if [[ "$MODE" == "check" ]]; then
        echo "   ⚠️  DESACTUALIZADO: $dst (${DST_HASH:0:16}…)"
        RC=2
        continue
    fi
    cp -f "$ORIGEN" "$dst"
    chown 10000:10000 "$dst" 2>/dev/null || true
    chmod 664 "$dst" 2>/dev/null || true
    if [[ "$(sha256sum "$dst" | awk '{print $1}')" == "$SRC_HASH" ]]; then
        echo "   📥 actualizado y verificado: $dst"
    else
        echo "   ❌ fallo al copiar: $dst" >&2
        RC=1
    fi
done

if [[ "$MODE" == "check" && "$RC" -eq 0 ]]; then
    echo "✅ Consumidores al día."
fi
exit "$RC"
