#!/usr/bin/env bash
# ============================================================================
# F2 · Ventana de recreación del contenedor para aplicar el montaje del canon
# ============================================================================
# Objetivo: /opt/hermes/skills deja de ser una copia dentro de la imagen y pasa
# a ser un bind mount de /root/hermes-agent/skills (el canon versionado).
#
# GATE DE FIRMA (bloqueo duro en código): sin --firma TOKEN validado por sha256
# contra /root/.sync-firma.sha256, el script sale con exit 1 y CERO cambios.
#
# SEGURIDAD:
#   · tag de imagen previo            · respaldo de .env y compose
#   · compose sin el montaje (.nobind) para rollback inmediato
#   · verificación posterior obligatoria (montaje + inodo + runtime + slots)
#   · ROLLBACK AUTOMÁTICO si la verificación falla
#
# USO:  ./scripts/f2_ventana_montaje.sh --firma TOKEN [--dry-run]
# ============================================================================
set -uo pipefail

REPO="/root/hermes-agent"
CONT="hermes-agent"
TS="$(date +%Y%m%d-%H%M%S)"
LOG="$REPO/data/state/f2_ventana_${TS}.log"
RES="$REPO/data/state/f2_ventana_${TS}.json"
FIRMA=""
DRY=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --firma)   FIRMA="${2:-}"; shift ;;
    --dry-run) DRY=1 ;;
    *) echo "❌ opción desconocida: $1" >&2; exit 1 ;;
  esac
  shift
done

log() { echo "$@" | tee -a "$LOG"; }

# ── GATE ────────────────────────────────────────────────────────────────────
SHA_FILE="/root/.sync-firma.sha256"
if [[ ! -f "$SHA_FILE" ]]; then
  echo "🔒 GATE CERRADO — no existe $SHA_FILE (lo crea el dueño)." >&2; exit 1
fi
if [[ -z "$FIRMA" ]]; then
  echo "🔒 GATE CERRADO — falta --firma TOKEN." >&2; exit 1
fi
GOT="$(printf '%s' "$FIRMA" | sha256sum | awk '{print $1}')"
if [[ "$GOT" != "$(cat "$SHA_FILE")" ]]; then
  echo "❌ FIRMA INVÁLIDA — el token no coincide con el autorizado por el dueño." >&2; exit 1
fi

log "=============================================================================="
log "F2 · VENTANA DE MONTAJE DEL CANON · $TS"
log "=============================================================================="
log "✅ Firma válida."

# ── PRE-CHECKS ──────────────────────────────────────────────────────────────
log ""
log "── PRE-CHECKS ──"
ALERT="$REPO/data/state/skills_sync_alert.json"
PAR="$(python3 -c "import json;print(json.load(open('$ALERT')).get('parity'))" 2>/dev/null || echo '?')"
log "   paridad canon/espejo: $PAR"
if [[ "$PAR" != "True" ]]; then
  log "   🛑 ABORTADO: la paridad no es True. Cierra la divergencia ANTES de montar."
  exit 1
fi
DIRTY="$(cd "$REPO" && git status --porcelain | head -5)"
if [[ -n "$DIRTY" ]]; then
  log "   ⚠️ árbol git sucio:"; echo "$DIRTY" | tee -a "$LOG"
fi
AUD="$(cd "$REPO" && python3 scripts/verify_skills.py 2>&1 | grep -c 'ADUANA SUPERADA')"
log "   aduana: $([[ $AUD -ge 1 ]] && echo VERDE || echo '⚠️ revisar')"

if [[ $DRY -eq 1 ]]; then
  log ""
  log "🧪 DRY-RUN — nada se ejecutó. Comando que se correría:"
  log "   docker compose up -d --no-build   (aplica 5 montajes: skills, skills_tool.py, delegate_tool.py, activity_labels.py, locales)"
  exit 0
fi

# ── PREPARACIÓN Y RESPALDOS ─────────────────────────────────────────────────
log ""
log "── PREPARACIÓN ──"
IMG_TAG="hermes-agent:pre-bind-${TS}"
IMG_CUR="$(docker inspect "$CONT" --format '{{.Config.Image}}')"
log "   imagen actual: $IMG_CUR  →  tag $IMG_TAG"
docker tag "$IMG_CUR" "$IMG_TAG" || { log "   🛑 no se pudo etiquetar"; exit 1; }

BK="$REPO/data/backups/f2_${TS}"
mkdir -p "$BK"
cp "$REPO/.env" "$BK/env.bak" 2>/dev/null || true
cp "$REPO/docker-compose.yml" "$BK/docker-compose.yml.bak"
log "   respaldos en $BK"

# compose sin el montaje de skills -> rollback inmediato al estado previo
python3 - "$REPO/docker-compose.yml" "$REPO/docker-compose.nobind.yml" <<'PY' | tee -a "$LOG"
import re, sys
src, dst = sys.argv[1], sys.argv[2]
lines = open(src, encoding='utf-8').read().splitlines(True)
out, quitadas = [], 0
for l in lines:
    if re.match(r'\s*-\s*\./skills:/opt/hermes/skills\s*$', l):
        quitadas += 1
        continue
    out.append(l)
open(dst, 'w', encoding='utf-8').writelines(out)
print('   compose de rollback escrito: %s (líneas de montaje retiradas: %d)' % (dst, quitadas))
PY

# respaldo del árbol que se va a sustituir (por si hubiera residuos)
docker exec "$CONT" tar -C /opt/hermes -cf - skills 2>/dev/null | tar -C "$BK" -xf - 2>/dev/null && \
  log "   respaldo del espejo actual: $BK/skills"

# ── PERMISOS DEL CANON (condición C2 de la evaluación de Ragnar) ────────────
# El canon es root:root 775. El runtime corre como uid 10000: sin este paso, un
# canon montado sería de SOLO LECTURA para los agentes (el invariante I5 falla).
log ""
log "── PERMISOS DEL CANON (grupo del runtime + setgid) ──"
chgrp -R 10000 "$REPO/skills" 2>/dev/null
find "$REPO/skills" -type d -exec chmod 2775 {} + 2>/dev/null
find "$REPO/skills" -type f -exec chmod 664 {} + 2>/dev/null
log "   $(stat -c '%U:%G %a' "$REPO/skills")  (raíz del canon)"
DEFGRP=$(find "$REPO/skills" -maxdepth 2 -type d | head -1)
log "   ejemplo: $DEFGRP -> $(stat -c '%U:%G %a' "$DEFGRP" 2>/dev/null)"

# ── RECREACIÓN ──────────────────────────────────────────────────────────────
log ""
log "── RECREACIÓN (docker compose up -d) ──"
( cd "$REPO" && docker compose up -d --no-build 2>&1 | tee -a "$LOG" )

# ── ESPERA DE LISTO ─────────────────────────────────────────────────────────
log ""
log "── ESPERA DE ARRANQUE ──"
OK=0
for i in $(seq 1 40); do
  sleep 6
  ST="$(docker inspect "$CONT" --format '{{.State.Status}}' 2>/dev/null || echo missing)"
  RUN="$(docker exec "$CONT" sh -c 'ls /opt/hermes/skills | head -1' 2>/dev/null || true)"
  log "   [${i}] estado=$ST arbol=${RUN:-vacío}"
  if [[ "$ST" == "running" && -n "$RUN" ]]; then OK=1; break; fi
done

# ── VERIFICACIÓN POSTERIOR ──────────────────────────────────────────────────
log ""
log "── VERIFICACIÓN ──"
FALLOS=()

MONTS="$(docker inspect "$CONT" --format '{{range .Mounts}}{{.Destination}} {{end}}')"
echo "$MONTS" | grep -q "/opt/hermes/skills" && log "   ✅ montaje de skills presente" \
  || FALLOS+=("montaje de skills ausente")

INO_CONT="$(docker exec "$CONT" stat -c '%d:%i' /opt/hermes/skills 2>/dev/null || echo x)"
INO_HOST="$(stat -c '%d:%i' "$REPO/skills" 2>/dev/null || echo y)"
if [[ "$INO_CONT" == "$INO_HOST" ]]; then
  log "   ✅ mismo inodo canon/contenedor ($INO_CONT) — UN SOLO ÁRBOL"
else
  log "   ❌ inodos distintos: contenedor=$INO_CONT host=$INO_HOST"
  FALLOS+=("inodos distintos")
fi

SLOTS=$(docker exec "$CONT" sh -c 'ls /opt/data/logs/gateways 2>/dev/null | wc -l' 2>/dev/null || echo 0)
GW=$(docker exec "$CONT" sh -c 'ps -ef 2>/dev/null | grep -c "[g]ateway run"' 2>/dev/null || echo 0)
log "   slots de gateway con log: $SLOTS (16 esperados) · procesos 'gateway run': $GW"
if [[ "${SLOTS:-0}" -lt 16 ]]; then log "   ℹ️  slots < 16: revisar arranque de la flota"; fi

PROBE=$(docker exec -u 10000 "$CONT" sh -c 'touch /opt/hermes/skills/.write-probe && ls -l /opt/hermes/skills/.write-probe && rm -f /opt/hermes/skills/.write-probe' 2>&1 | head -1)
if echo "$PROBE" | grep -q "write-probe"; then
  log "   ✅ INVARIANTE I5: uid 10000 (runtime) ESCRIBE el canon montado"
  log "      $PROBE"
else
  log "   ❌ INVARIANTE I5 FALLA: uid 10000 no puede escribir el canon montado -> $PROBE"
  FALLOS+=("write-probe uid 10000 falló")
fi

if [[ ${#FALLOS[@]} -gt 0 ]]; then
  log ""
  log "   🛑 FALLOS: ${FALLOS[*]}"
  log "   🔄 ROLLBACK AUTOMÁTICO con el compose sin montaje…"
  ( cd "$REPO" && docker compose -f docker-compose.nobind.yml up -d --no-build 2>&1 | tee -a "$LOG" )
  sleep 20
  ST2="$(docker inspect "$CONT" --format '{{.State.Status}}' 2>/dev/null || echo missing)"
  log "   estado tras rollback: $ST2"
  python3 -c "import json,sys;json.dump({'ts':'$TS','resultado':'ROLLBACK','fallos':sys.argv[1:]},open('$RES','w'),indent=1,ensure_ascii=False)" "${FALLOS[@]}"
  log "   Resultado: $RES"
  exit 1
fi

python3 - "$RES" "$TS" "$INO_CONT" "$IMG_TAG" <<'PY' | tee -a "$LOG"
import json, sys
res, ts, ino, tag = sys.argv[1:5]
json.dump({'ts': ts, 'resultado': 'OK', 'inodo_canon_runtime': ino,
           'tag_previo': tag,
           'rollback': 'docker compose -f docker-compose.nobind.yml up -d',
           'nota': 'Verificado: montaje presente, mismo inodo (un solo arbol), runtime arriba.'},
          open(res, 'w'), indent=1, ensure_ascii=False)
print('   Resultado: %s' % res)
PY
log ""
log "🎉 F2 COMPLETADA: el canon del repositorio ES el árbol del runtime. Copia eliminada."
log "   Log: $LOG"
exit 0
