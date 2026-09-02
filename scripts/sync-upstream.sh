#!/usr/bin/env bash
# sync-upstream.sh — Sync hermes-agent fork with upstream NousResearch/hermes-agent
# Runs daily via cron at 02:00. Handles: fetch, rebase, build, deploy, verify, push.
set -euo pipefail
# Increase timeout for long Docker builds
export DOCKER_BUILDKIT=1

REPO_DIR="/root/hermes-agent"
LOG_FILE="${REPO_DIR}/scripts/sync-upstream.log"
LOCK_FILE="/tmp/hermes-sync.lock"
PRE_REBUILD_IMAGE=""
HEALTH_CHECK_RETRIES=12
HEALTH_CHECK_INTERVAL=10

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

fail() {
    log "FAILED: $*"
    rm -f "$LOCK_FILE"
    exit 1
}

cleanup() {
    rm -f "$LOCK_FILE"
}
trap cleanup EXIT

# --- Lock: prevent concurrent runs ---
if [ -f "$LOCK_FILE" ]; then
    pid=$(cat "$LOCK_FILE" 2>/dev/null || echo "")
    if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
        log "SKIP: Another sync is running (PID $pid)"
        exit 0
    fi
    log "WARN: Stale lock file found, removing"
    rm -f "$LOCK_FILE"
fi
echo $$ > "$LOCK_FILE"

# --- Step 1: Fetch upstream ---
log "=== Sync started ==="
cd "$REPO_DIR"
log "Fetching upstream..."
git fetch upstream --quiet 2>&1 || fail "git fetch upstream failed"

# --- Step 2: Check for new commits ---
BEHIND=$(git rev-list --count HEAD..upstream/main 2>/dev/null || echo "0")
if [ "$BEHIND" = "0" ]; then
    log "Up to date. No new commits from upstream."
    log "=== Sync finished (no changes) ==="
    exit 0
fi
log "Upstream has $BEHIND new commit(s)"

# --- Step 3: Save current state ---
BACKUP_TAG="pre-sync-$(date +%Y%m%d-%H%M%S)"
git tag "$BACKUP_TAG" HEAD 2>/dev/null || log "WARN: Could not create backup tag"
PRE_IMAGE=$(docker inspect hermes-agent --format '{{.Image}}' 2>/dev/null || echo "")
PRE_IMAGE_NAME=$(docker images hermes-agent-hermes:latest --format '{{.ID}}' 2>/dev/null || echo "")

# --- Step 4: Rebase ---
log "Rebasing onto upstream/main..."
if git rebase upstream/main 2>&1 | tee -a "$LOG_FILE"; then
    log "Rebase succeeded"
else
    log "Rebase had conflicts — aborting"
    git rebase --abort 2>/dev/null || true
    log "Rebase aborted. Manual intervention required."
    log "Run: cd $REPO_DIR && git rebase upstream/main"
    log "=== Sync finished (conflicts) ==="
    exit 1
fi

# --- Step 5: Verify Python syntax ---
log "Verifying key files..."
python3 -c "import py_compile; py_compile.compile('tools/mcp_tool.py', doraise=True)" 2>/dev/null || {
    log "Syntax error in mcp_tool.py after rebase — reverting"
    git reset --hard "$BACKUP_TAG" 2>/dev/null
    fail "Syntax check failed, reverted to $BACKUP_TAG"
}
python3 -c "import py_compile; py_compile.compile('agent/conversation_loop.py', doraise=True)" 2>/dev/null || {
    log "Syntax error in conversation_loop.py — reverting"
    git reset --hard "$BACKUP_TAG" 2>/dev/null
    fail "Syntax check failed, reverted to $BACKUP_TAG"
}
log "Syntax checks passed"

# --- Step 6: Build Docker image ---
log "Building Docker image..."
if docker compose build --no-cache 2>&1 | tee -a "$LOG_FILE"; then
    log "Docker image built successfully"
else
    log "Docker build failed — reverting"
    git reset --hard "$BACKUP_TAG" 2>/dev/null
    fail "Docker build failed, reverted to $BACKUP_TAG"
fi

# --- Step 7: Deploy ---
log "Deploying new container..."
if docker compose up -d 2>&1 | tee -a "$LOG_FILE"; then
    log "Container recreated"
else
    fail "Docker compose up failed"
fi

# --- Step 8: Health check ---
log "Waiting for gateways to start..."
sleep 15
ALL_UP=true
for i in $(seq 1 $HEALTH_CHECK_RETRIES); do
    GATEWAYS=$(docker exec hermes-agent /command/s6-svstat /run/service/gateway-* 2>/dev/null | grep -c "^up" || echo "0")
    if [ "$GATEWAYS" -ge 2 ]; then
        log "Health check passed: $GATEWAYS gateways up"
        break
    fi
    log "Waiting... ($i/$HEALTH_CHECK_RETRIES) — $GATEWAYS gateways up"
    sleep $HEALTH_CHECK_INTERVAL
    if [ "$i" = "$HEALTH_CHECK_RETRIES" ]; then
        ALL_UP=false
    fi
done

if [ "$ALL_UP" = false ]; then
    log "WARNING: Not all gateways are up. Checking container logs..."
    docker logs hermes-agent --tail 20 2>&1 | tee -a "$LOG_FILE"
    log "Deploy completed but health check failed — manual review recommended"
fi

# --- Step 9: Push to origin ---
log "Pushing to origin..."
if git push origin main --force-with-lease 2>&1 | tee -a "$LOG_FILE"; then
    log "Push successful"
else
    log "Push failed — code is deployed locally but not pushed"
fi

# --- Step 10: Cleanup old backup tags ---
git tag -l "pre-sync-*" | sort -r | tail -n +6 | xargs -r git tag -d 2>/dev/null || true

NEW_VERSION=$(docker exec hermes-agent cat /opt/hermes/pyproject.toml 2>/dev/null | grep "^version" | head -1 | cut -d'"' -f2 || echo "unknown")
log "=== Sync finished ==="
log "Upstream commits: $BEHIND"
log "Hermes version: $NEW_VERSION"
log "Gateways: $GATEWAYS up"
log "Backup tag: $BACKUP_TAG"
