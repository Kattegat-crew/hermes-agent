#!/usr/bin/env bash
# F4 paso 3: ¿funciona el pin ahora? y si sí, aplicar la lista de protegidas.
set -uo pipefail
export HOME=/opt/data
cd /opt/data
H=/opt/hermes/.venv/bin/hermes

echo "=== prueba de pin ==="
$H curator pin skill-library-ops 2>&1 | tail -3
echo
echo "=== si funciono: aplicar la lista de protegidas (F1) ==="
PROTEGIDAS="agent-roster-ops brain-knowledge-ops campaign-ops colombia-legal-ops copy-quality-es github-workflow google-workspace-ops hermes-cron-ops hermes-desktop-ops hermes-fleet-operations hermes-provider-ops hermes-runtime-ops informes-cliente-pipeline meta-ads-ops multi-agent-collaboration oauth-connection-ops skill-library-ops video-reel-pipeline vps-deployment-ops plan engram-memory-system hermes-scheduled-jobs"
ok=0; fallos=0
for s in $PROTEGIDAS; do
  out=$($H curator pin "$s" 2>&1 | tail -1)
  case "$out" in
    *"pinned"*|*"Pin"*|*"ok"*) ok=$((ok+1)); printf '  ✅ %-30s %s\n' "$s" "$out" ;;
    *) fallos=$((fallos+1)); printf '  ⚠️  %-30s %s\n' "$s" "$out" ;;
  esac
done
echo
echo "pinned ok=$ok fallos=$fallos"
