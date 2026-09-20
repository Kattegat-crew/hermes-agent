#!/usr/bin/env bash
# ==============================================================================
# sync_container_skills.sh — Sincronizador canónico bidireccional Host <-> Contenedor
#
#   ./sync_container_skills.sh                       -> DRY-RUN (por defecto).
#                                                      Paridad por CONTENIDO (sha256),
#                                                      detecta nuevas, drift y faltantes.
#   ./sync_container_skills.sh --check                -> igual que arriba (explícito).
#   ./sync_container_skills.sh --apply --firma TOKEN  -> adopta nuevas + despliega el canon.
#                                                      EXIGE el token del dueño.
#   ... --apply --firma TOKEN --adopt-sediment        -> promueve al canon las skills creadas
#                                                      por los agentes en los sedimentos
#                                                      (dirs locales de los perfiles) y limpia.
#   ... --apply --firma TOKEN --adopt-new             -> adopta al canon las skills que
#                                                      solo existen en el espejo.
#   ... --apply --firma TOKEN --adopt-drift           -> además promueve al canon el
#                                                      contenido del contenedor para skills
#                                                      ya existentes (respalda el canónico).
#   ... --commit                                      -> git add+commit de las adopciones (no push).
#   ./sync_container_skills.sh --json /ruta.json      -> guarda el diagnóstico en JSON.
#
# GATE DE FIRMA (bloqueo duro en código, no en la disciplina del agente):
#   El dueño crea UNA vez el hash de su token:
#     printf '%s' 'TU_TOKEN_SECRETO' | sha256sum | awk '{print $1}' > /root/.sync-firma.sha256
#     chmod 600 /root/.sync-firma.sha256
#   Sin ese archivo, --apply aborta. Un agente NUNCA debe crear ni leer el token.
#
# NADA se destruye sin respaldo: toda skill nueva o con drift se archiva en
#   <repo>/data/archive/sync_<timestamp>/ ANTES de tocar el espejo del contenedor.
# ==============================================================================
set -euo pipefail

REPO="/root/hermes-agent"
ENGINE="$REPO/scripts/sync_skills_sync.py"

MODE="check"
FIRMA=""
ADOPT=0
ADOPT_NEW=0
ADOPT_SED=0
COMMIT=0
JSON_OUT=""

usage() {
    sed -n '2,26p' "$0" | sed 's/^# \{0,1\}//'
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --check)       MODE="check" ;;
        --apply)       MODE="apply" ;;
        --firma)       FIRMA="${2:-}"; shift ;;
        --adopt-new)      ADOPT_NEW=1 ;;
        --adopt-sediment) ADOPT_SED=1 ;;
        --adopt-drift) ADOPT=1 ;;
        --commit)      COMMIT=1 ;;
        --json)        JSON_OUT="${2:-}"; shift ;;
        -h|--help)     usage; exit 0 ;;
        *)             echo "❌ Opción desconocida: $1" >&2; echo; usage; exit 1 ;;
    esac
    shift
done

if [[ ! -f "$ENGINE" ]]; then
    echo "❌ Motor no encontrado: $ENGINE" >&2
    exit 1
fi

ARGS=(--mode "$MODE" --repo "$REPO" --host "$REPO/skills")
[[ -n "$JSON_OUT" ]] && ARGS+=(--json-out "$JSON_OUT")
[[ "$ADOPT" -eq 1 ]] && ARGS+=(--adopt-drift)
[[ "$ADOPT_NEW" -eq 1 ]] && ARGS+=(--adopt-new)
[[ "$ADOPT_SED" -eq 1 ]] && ARGS+=(--adopt-sediment)
[[ "$COMMIT" -eq 1 ]] && ARGS+=(--commit)
[[ -n "$FIRMA" ]] && ARGS+=(--firma "$FIRMA")

exec python3 "$ENGINE" "${ARGS[@]}"
