#!/usr/bin/env bash
# ==============================================================================
# sync_container_skills.sh — Sincronización robusta y bidireccional Host <-> Contenedor
# 
# Modos de ejecución:
#   ./sync_container_skills.sh [--check]  -> Modo dry-run por defecto. Audita paridad y detecta skills nuevas.
#   ./sync_container_skills.sh --apply    -> Adopta skills nuevas del contenedor al repo y sincroniza el canon.
# ==============================================================================
set -euo pipefail

HOST_SKILLS="/root/hermes-agent/skills"
CONTAINER_NAME="hermes-agent"
CONTAINER_SKILLS="/opt/hermes/skills"
ADOPT_TARGET="/root/hermes-agent/skills/specialists"

MODE="check"
for arg in "$@"; do
    case "$arg" in
        --apply)
            MODE="apply"
            ;;
        --check)
            MODE="check"
            ;;
        -h|--help)
            echo "Uso: $0 [--check|--apply]"
            echo "  --check   (Por defecto) Inspecciona paridad, detecta skills huérfanas y candidatas a adopción."
            echo "  --apply   Ejecuta la adopción al repo host y sincroniza el árbol hacia el contenedor."
            exit 0
            ;;
        *)
            echo "❌ Opción desconocida: $arg. Usa --check o --apply." >&2
            exit 1
            ;;
    esac
done

echo "=== SINCRONIZADOR DE SKILLS: MODO ${MODE^^} ==="

# 1. Verificaciones previas
if [[ ! -d "$HOST_SKILLS" ]]; then
    echo "❌ Error: Directorio host $HOST_SKILLS no existe." >&2
    exit 1
fi

if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "⚠️ Advertencia: Contenedor $CONTAINER_NAME no está corriendo. Operación omitida."
    exit 0
fi

# 2. Análisis de paridad y detección de skills creadas en el contenedor
echo "🔍 Analizando paridad entre Host y Contenedor..."

HOST_LIST=$(python3 -c "
import os
skills = set()
for r, d, f in os.walk('$HOST_SKILLS'):
    if 'SKILL.md' in f:
        skills.add(os.path.basename(r))
print('\n'.join(sorted(skills)))
")

CONTAINER_LIST=$(docker exec "$CONTAINER_NAME" python3 -c "
import os
skills = set()
for r, d, f in os.walk('$CONTAINER_SKILLS'):
    if 'SKILL.md' in f:
        skills.add(os.path.basename(r))
print('\n'.join(sorted(skills)))
")

HOST_COUNT=$(echo "$HOST_LIST" | grep -v '^$' | wc -l)
CONTAINER_COUNT=$(echo "$CONTAINER_LIST" | grep -v '^$' | wc -l)

# Encontrar skills en el contenedor que NO existen en el host (creadas por agentes)
NEW_IN_CONTAINER=$(python3 -c "
host = set('''$HOST_LIST'''.splitlines())
cont = set('''$CONTAINER_LIST'''.splitlines())
diff = sorted(cont - host)
for s in diff:
    if s:
        print(s)
")

MISSING_IN_CONTAINER=$(python3 -c "
host = set('''$HOST_LIST'''.splitlines())
cont = set('''$CONTAINER_LIST'''.splitlines())
diff = sorted(host - cont)
for s in diff:
    if s:
        print(s)
")

echo "📊 Diagnóstico actual:"
echo "   Host (Git canónico):   $HOST_COUNT skills"
echo "   Contenedor (/opt):     $CONTAINER_COUNT skills"

if [[ -n "$NEW_IN_CONTAINER" ]]; then
    echo ""
    echo "🚨 SKILLS NUEVAS EN CONTENEDOR (Candidatas a Adopción):"
    while IFS= read -r skill; do
        [[ -z "$skill" ]] && continue
        echo "   ⭐ $skill"
    done <<< "$NEW_IN_CONTAINER"
fi

if [[ -n "$MISSING_IN_CONTAINER" ]]; then
    echo ""
    echo "📦 SKILLS PENDIENTES DE DESPLEGAR AL CONTENEDOR:"
    PENDING_COUNT=$(echo "$MISSING_IN_CONTAINER" | wc -l)
    echo "   Total pendientes: $PENDING_COUNT skills"
fi

if [[ "$MODE" == "check" ]]; then
    echo ""
    if [[ -z "$NEW_IN_CONTAINER" && -z "$MISSING_IN_CONTAINER" && "$HOST_COUNT" -eq "$CONTAINER_COUNT" ]]; then
        echo "✅ PARIDAD PERFECTA (100% sincronizado). No se requieren acciones."
        exit 0
    else
        echo "⚠️ Se detectaron diferencias. Para adoptar y sincronizar, ejecuta:"
        echo "   $0 --apply"
        exit 0
    fi
fi

# ==============================================================================
# MODO --apply: ADOPCIÓN Y SINCRONIZACIÓN EFECTIVA
# ==============================================================================
echo ""
echo "🚀 Iniciando proceso de sincronización con salvaguardas..."

# 3. Paso de ADOPCIÓN: Rescatar skills creadas en el contenedor hacia el host
if [[ -n "$NEW_IN_CONTAINER" ]]; then
    echo "📥 Rescatando skills nuevas del contenedor hacia $ADOPT_TARGET..."
    mkdir -p "$ADOPT_TARGET"
    while IFS= read -r skill; do
        [[ -z "$skill" ]] && continue
        echo "   💾 Adoptando: $skill..."
        
        # Encontrar la ruta dentro del contenedor
        CONT_PATH=$(docker exec "$CONTAINER_NAME" python3 -c "
import os
for r, d, f in os.walk('$CONTAINER_SKILLS'):
    if os.path.basename(r) == '$skill' and 'SKILL.md' in f:
        print(r)
        break
")
        if [[ -n "$CONT_PATH" ]]; then
            TARGET_DIR="$ADOPT_TARGET/$skill"
            mkdir -p "$TARGET_DIR"
            docker exec "$CONTAINER_NAME" tar -C "$CONT_PATH" -czf - . | tar -C "$TARGET_DIR" -xzf -
            echo "   ✅ $skill guardada en host ($TARGET_DIR)"
        fi
    done <<< "$NEW_IN_CONTAINER"
    
    # Regenerar índice si hubo adopciones
    if [[ -f "/root/hermes-agent/scripts/build_skills_index.py" ]]; then
        python3 /root/hermes-agent/scripts/build_skills_index.py
    fi
fi

# 4. Normalizar permisos en el Host
echo "🔒 Normalizando permisos en Host (775 dirs / 664 files)..."
find "$HOST_SKILLS" -type d -exec chmod 775 {} +
find "$HOST_SKILLS" -type f -exec chmod 664 {} +

# 5. Sincronizar hacia el contenedor
echo "📦 Desplegando árbol canónico al contenedor..."
docker exec "$CONTAINER_NAME" rm -rf "${CONTAINER_SKILLS:?}"/*
tar -C "$HOST_SKILLS" -czf - . | docker exec -i "$CONTAINER_NAME" tar -C "$CONTAINER_SKILLS" -xzf -

# 6. Fijar ownership y permisos en el contenedor
echo "👤 Fijando ownership hermes:hermes (10000:10000) y permisos en contenedor..."
docker exec "$CONTAINER_NAME" chown -R 10000:10000 "$CONTAINER_SKILLS"
docker exec "$CONTAINER_NAME" chmod -R 775 "$CONTAINER_SKILLS"

# 7. Verificación final de paridad
FINAL_HOST_COUNT=$(find "$HOST_SKILLS" -name "SKILL.md" | wc -l)
FINAL_CONTAINER_COUNT=$(docker exec "$CONTAINER_NAME" python3 -c "import os; print(sum(1 for r, d, f in os.walk('$CONTAINER_SKILLS') if 'SKILL.md' in f))")

echo ""
echo "📊 Verificación Final de Paridad:"
echo "   Host:       $FINAL_HOST_COUNT skills"
echo "   Contenedor: $FINAL_CONTAINER_COUNT skills"

if [[ "$FINAL_HOST_COUNT" -eq "$FINAL_CONTAINER_COUNT" ]]; then
    echo "🎉 SINCRONIZACIÓN EXITOSA: Paridad 100% confirmada entre Git y el contenedor."
    exit 0
else
    echo "❌ Error: Discrepancia detectada tras sincronizar ($FINAL_HOST_COUNT vs $FINAL_CONTAINER_COUNT)." >&2
    exit 1
fi
