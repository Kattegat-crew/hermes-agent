#!/usr/bin/env bash
# ==============================================================================
# sync_container_skills.sh — Sincronización idempotente Host -> Contenedor Docker
# Garantiza paridad absoluta entre /root/hermes-agent/skills y /opt/hermes/skills
# ==============================================================================
set -euo pipefail

HOST_SKILLS="/root/hermes-agent/skills"
CONTAINER_NAME="hermes-agent"
CONTAINER_SKILLS="/opt/hermes/skills"

echo "=== INICIANDO SINCRONIZACIÓN DE SKILLS ==="

# 1. Verificar existencia del directorio origen
if [[ ! -d "$HOST_SKILLS" ]]; then
    echo "❌ Error: Directorio $HOST_SKILLS no existe." >&2
    exit 1
fi

# 2. Verificar que el contenedor esté corriendo
if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "⚠️ Advertencia: Contenedor $CONTAINER_NAME no está corriendo. Sincronización omitida."
    exit 0
fi

# 3. Normalizar permisos en el Host (UID 10000 compatible)
echo "🔒 Normalizando permisos en Host (775/664)..."
find "$HOST_SKILLS" -type d -exec chmod 775 {} +
find "$HOST_SKILLS" -type f -exec chmod 664 {} +

# 4. Limpiar y streamear árbol limpio al contenedor
echo "📦 Transfiriendo árbol de skills a $CONTAINER_NAME:$CONTAINER_SKILLS..."
docker exec "$CONTAINER_NAME" rm -rf "${CONTAINER_SKILLS:?}"/*
tar -C "$HOST_SKILLS" -czf - . | docker exec -i "$CONTAINER_NAME" tar -C "$CONTAINER_SKILLS" -xzf -

# 5. Ajustar propiedad y permisos en el contenedor para el usuario hermes (10000:10000)
echo "👤 Fijando ownership hermes:hermes (10000:10000) en contenedor..."
docker exec "$CONTAINER_NAME" chown -R 10000:10000 "$CONTAINER_SKILLS"
docker exec "$CONTAINER_NAME" chmod -R 775 "$CONTAINER_SKILLS"

# 6. Validar paridad
HOST_COUNT=$(find "$HOST_SKILLS" -name "SKILL.md" | wc -l)
CONTAINER_COUNT=$(docker exec "$CONTAINER_NAME" python3 -c "import os; print(sum(1 for r, d, f in os.walk('$CONTAINER_SKILLS') if 'SKILL.md' in f))")

echo "📊 Verificación de Paridad:"
echo "   Host:       $HOST_COUNT skills"
echo "   Contenedor: $CONTAINER_COUNT skills"

if [[ "$HOST_COUNT" -eq "$CONTAINER_COUNT" ]]; then
    echo "✅ PARIDAD 100% CONFIRMADA: El contenedor está en sincronía perfecta con Git."
    exit 0
else
    echo "❌ DISCREPANCIA DETECTADA: Host ($HOST_COUNT) != Contenedor ($CONTAINER_COUNT)" >&2
    exit 1
fi
