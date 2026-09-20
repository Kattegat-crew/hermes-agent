---
name: vps-web-deployment
version: 1.1.0
description: Deploy static sites to VPS with NPM and migration.
author: ragnar
triggers:
  - deploy static site to VPS
  - migrate files between servers
  - gallery deployment
  - reels.neural deployment
  - nginx reverse proxy setup
  - version guard 503 hermes
metadata:
  hermes:
    tags: [deploy, vps, nginx, npm, static-site, migration]
    related_skills: [web-serving-diagnosis, hermes-admin-operations, vps-ops]
---

# VPS Web Deployment

Deploy static sites, galleries, and web apps to VPS infrastructure with NPM reverse proxy. Covers inter-server file migration, inventory-driven site generation, and the Hermes v0.21.0+ version guard pitfall.

## Architecture Pattern

```
Cloudflare → NPM (:80/:443) → Backend container/service (:port)
                                  ↳ /opt/<app>/ (mount or direct)
```

NPM (nginx-proxy-manager) runs on VPS prod (.222) at `100.73.30.29`. Config files: `/opt/docker/nginx-proxy-manager/data/nginx/proxy_host/`. Each proxy host is a numbered `.conf` file.

### Adding a new domain
1. Create the conf file in proxy_host/ with upstream port
2. `docker exec nginx-proxy-manager nginx -s reload`
3. SSL via Let's Encrypt is automatic in NPM

### Proxy host inventory (source of truth — NOT psql)
The live list of domains → forwards lives in the NPM **SQLite** DB at `/data/database.sqlite` (verified 02/09/2026). npm-postgres is EMPTY — querying it wastes a round-trip. Inspect headlessly:

```bash
docker run --rm -v /opt/docker/nginx-proxy-manager/data:/d:ro alpine sh -c \
  'apk add -q sqlite >/dev/null 2>&1; sqlite3 /d/database.sqlite "SELECT domain_names, forward_host, forward_port, enabled, certificate_id FROM proxy_host WHERE is_deleted=0 ORDER BY domain_names;"'
```

Forward target types seen in prod (18 hosts live):
- `172.19.0.1:PORT` — Docker-published service on the host (landings 9001/9002/9003, reels-web 9020)
- `172.19.0.5:8648` — fixed container IP inside the proxy network (connect-gate)
- `100.73.30.29:PORT` — Tailscale IP: internal-only services never exposed publicly (wiki 3042, crm 3020, auth 3043, ap 8088, langfuse, dashboard, pdf, form, docuseal, docs, status)

## Inter-Server File Migration

When the container (on .250) can't SSH directly to target (.222), stream via tar pipe:

```bash
docker run --rm -v /:/hostfs:ro alpine:latest tar czf - -C /hostfs/<src_dir> <subdir> | \
  ssh -o ConnectTimeout=15 -o BatchMode=yes root@<target_ip> "tar xzf - -C <dest>"
```

**Key details:**
- Uses docker on source host to access host filesystem via bind mount
- Pipes through container stdout to SSH on target
- No SSH key needed between servers (only container→target)
- For large transfers (>100MB), set `timeout 300` or higher on the terminal call
- Verify after: `ssh root@<target> "du -sh <dest> && ls <dest>"`

For syncing generated HTML (small files), rsync via SSH works:
```bash
tar czf - -C /local/dir <site> | ssh root@<target> "cd /opt/reels && tar xzf -"
```

## Hermes v0.21.0+ Version Guard (503)

**NEW in v0.21.0 "Pantheon Release" (08/31/2026):**

The dashboard process (`hermes serve` / `hermes dashboard`) now compares the running process's loaded code hash against the checkout on disk. If they differ, the model picker returns:

```
503: {"detail":"Restart required: This process is running code from <old-hash> \
but the checkout on disk is now <new-hash>..."}
```

**Common cause:** `sync-upstream.sh` runs at 2AM via cron, rebases the repo (moving HEAD forward), but doesn't restart `hermes-serve`. The running process still has old code.

**Fix:**
```bash
# On the HOST (not container) via nsenter
docker run --rm --privileged --pid=host alpine:latest nsenter -t 1 -m -u -i -n \
  bash -c "systemctl restart hermes-serve && sleep 5 && curl -sf http://127.0.0.1:9112/api/health"
```

**Prevention:** Any script that modifies `/root/hermes-agent/` checkout (git rebase, pull, push) MUST also restart hermes-serve. Add this to sync-upstream.sh Step 8b:

```bash
# --- Step 8b: Restart host services on new code (dashboard 503 guard) ---
log "Restarting hermes-serve to load the new code..."
systemctl restart hermes-serve 2>>"$LOG_FILE" || log "WARN: systemctl restart hermes-serve failed"
sleep 5
if curl -sf -m 8 -o /dev/null http://127.0.0.1:9112/api/health; then
    log "hermes-serve healthy after restart"
else
    log "WARN: hermes-serve health check failed after restart"
fi
```

**Verify after any code change:**
```bash
curl -sf http://127.0.0.1:9112/api/health  # returns {"ok":true,"version":"0.21.0"}
```

## Static Site Generation Pattern

For media galleries with real file inventory:

1. **Inventory via SSH:** `ssh root@<server> "find /opt/<app> -type f \( -name '*.mp4' -o -name '*.png' ...\) -exec ls -l {} \;"`
2. **Parse inventory** into Python dict with paths + sizes
3. **Generate HTML** with shared CSS/JS design system (inline, no build step)
4. **Deploy** via tar pipe or rsync
5. **Verify** with curl status checks on key URLs

**Design system tokens (Runway-inspired dark cinematic):**
- `--bg: #000; --surface: #0A0A0E; --border: #1E1E24`
- `--gold: #D4AF37` (Golden Game), `--emerald: #00C853` (Lucky Brothers)
- Inter font, zero shadows, video-first layout
- Lightbox via vanilla JS (click img → overlay)

## Pitfalls

- **Docker volume mount resolves against HOST:** When running `docker run -v /path:/dest` from INSIDE a container (hermes-agent), the `-v` path resolves against the HOST filesystem. Inside hermes-agent: `/opt/data/workspace` = `/root/hermes-agent/data/workspace` on host. Use HOST paths for all `-v` mounts. Verify: `docker exec <container> ls /dest/` — empty = wrong path.
- **docker run tar pipe timeout:** For >200MB transfers, foreground terminal may timeout at 60s. Use `timeout 300` or run in background with `notify=true`.
- **NPM conf numbering:** Proxy host confs are numbered (1.conf, 20.conf...). Find the right one with `grep -l 'domain' /opt/docker/nginx-proxy-manager/data/nginx/proxy_host/*.conf`.
- **server_proxy.conf is included in EVERY proxy host (15+), not just the apex:** a `location = /` there without a host guard replaced the home pages of wiki/docuseal/docs (incident 29/08). ANY custom location in `/data/nginx/custom/server_proxy.conf` must be scoped with `if ($host !~* ^(www\.)?neuralcrewlabs\.com$)` → rewrite to the apex static path.
- **staging vs prod paths:** Always confirm which directory nginx actually serves. `docker inspect <container> --format '{{range .Mounts}}{{.Source}} -> {{.Destination}}'` shows the mount.
- **golden-web-proxy on .250 may be stopped:** If it was used for a domain that's now migrated to .222, leave it stopped. DNS points to .222 via Cloudflare.
- **Absolute URLs in migrated HTML:** Check for hardcoded IPs (e.g. `http://147.93.3.250/`) in migrated index.html files. Replace with relative paths or the canonical domain.