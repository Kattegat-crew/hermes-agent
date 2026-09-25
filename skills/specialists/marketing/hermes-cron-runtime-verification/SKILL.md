---
name: hermes-cron-runtime-verification
description: "Use when verifying that Hermes cron jobs actually run."
tags: [cron, verificacion, gateway, namespace, nsenter, hermes]
version: 1.0.0
author: Ragnar
---

# Hermes Cron Runtime & Verification

Crons created via `cronjob_manage` do NOT run in my shell's environment. They run as **uid 10000 (`hermes`) with `HOME=/opt/data` inside the gateway's container namespace**. The most common failure mode in this system has been "verified" crons that fail in production: setpriv-only verification is FALSE PROOF.

## Namespace & volume map (memorize)

| Gateway container view | Host/agent shell view | Note |
|---|---|---|
| `/opt/data` | `/root/hermes-agent/data` (same inode) | THE shared volume cron can reach |
| `/root` | ≠ host `/root` (700, different dir) | host repos INVISIBLE to cron |
| `/opt/data/home` | `/root/hermes-agent/data/home` | real HOME for Composio (`.composio/`) |
| `/usr/local/bin/composio` (host) | does not exist in container | use `/opt/data/home/.composio/composio` inside |
| `/opt/data/cron/output/<jobid>` | `/root/hermes-agent/data/cron/output/<jobid>` | must be uid-10000-owned or Errno 13 |
| `/opt/data/.ssh` | `/root/hermes-agent/data/.ssh` | ssh config/keys cron's git will use |

**Consequence**: any repo or script a cron touches must live under `data/` (visible to the gateway as `/opt/data/...`). Anything under host `/root/...` is unreachable by cron even if MY shell can read it.

## Golden verification protocol (before saying "verificado")

1. **Inspect the gateway's actual view**: `PID=$(pgrep -f 'hermes gateway run' | head -1); ls -ld /proc/$PID/root/root /proc/$PID/root/opt/data; ls /proc/$PID/root/usr/local/bin/composio`. If a path is missing in `/proc/$PID/root/...`, the cron cannot use it — end of discussion.
2. **Execute IN the gateway namespace**: `nsenter -t $PID -m -- setpriv --reuid=10000 --regid=10000 --clear-groups env HOME=/opt/data <script>`. Only a pass here is proof. setpriv in my own namespace tests MY filesystem view, not cron's.
3. **Output dirs**: `data/cron/output/<job_id>/` must be `10000:10000` writable. A root-created dir makes the scheduler die with `Permission denied: '...output_....tmp'` — which the user receives as a WhatsApp failure alert.
4. `last_status: ok` from cron list is necessary but not sufficient: read the run's output artifact too.
5. **Composio from cron context**: absolute path `/opt/data/home/.composio/composio` with `HOME=/opt/data/home` (the host wrapper script hardcodes a host path that doesn't exist in the container).
6. **Git from cron**: deploy keys are PER-REPO — a key bound to repo A returns "Repository not found" (looks like missing repo, is actually permission) on repo B. Create a write deploy key per repo (`gh api repos/<org>/<repo>/keys -f key=... -f read_only=false`), register the IdentityFile in the ssh config visible to the gateway, and ensure uid 10000 has a `/etc/passwd` entry (git/ssh complain "No user exists for uid 10000" otherwise).

## Independent reviewer pattern (this is what caught the false verification)

When about to tell the user a cron system is "100% operativo", first dispatch a fresh, read-only audit session:

```
hermes -z "$(cat /tmp/reviewer_prompt.txt)" --yolo     # background, ~10 min, report to file
```

Prompt must contain: numbered checks each demanding PASS/FAIL/BLOCKED + exact evidence; explicit prohibitions (no publish, no commit/push, no external messages, no paid generation, dry-runs only); and the instruction to test **inside the gateway namespace (nsenter / /proc/<pid>/root), not in the tester's own env**. Verdict format: APROBADO / APROBADO CON HALLAZOS / RECHAZADO.

A fresh-context reviewer reproduces the real failure path self-review misses, and costs one cheap-model session.

## TWO tickers, TWO views of `/opt/data` (gotcha verified 2026-09-10)

A job can be claimed by either of two schedulers, and they do NOT share a filesystem view:

| Ticker | User | `/opt/data` resolves to |
|---|---|---|
| gateway (`gateway-default`, s6) | uid 10000 (container ns) | the real shared tree (container `/opt/data`) |
| root ticker = Hermes Desktop SSH backend (`hermes serve --isolated`, `HERMES_DESKTOP=1`) | root, **host mount ns** | a nearly EMPTY host dir; the real tree is `/root/hermes-agent/data` |

Consequence: a wrapper that hardcodes `/opt/data/...` passes when the gateway claims it and dies with `ENOENT` when the root ticker claims it. Real case: `content-intel-daily` failed 2 days in a row with `python3: can't open file '/opt/data/content-intel-build/content_harvest.py': [Errno 2]` because `/opt/data/content-intel-build` on the host is an empty dir.

Diagnose (no guessing):

```bash
readlink /proc/<job_pid>/ns/mnt          # host ns (4026531841) vs container ns (different)
ls /proc/<job_pid>/root/opt/data/<path>  # what the job's owner actually sees
```

Rule for every cron wrapper: resolve the repo/build dir by probing BOTH roots, and run the steps that need the container through `docker exec` when the wrapper itself runs on the host:

```bash
IN_CONTAINER=0; [ -f /.dockerenv ] && IN_CONTAINER=1
in_gw() { if [ "$IN_CONTAINER" = 1 ]; then bash -c "$1"; else docker exec -u 10000 hermes-agent bash -c "$1"; fi; }
```

Also note: root-ticker runs leave root-owned residue in shared git repos (`.git/objects/**`), after which uid 10000 can no longer commit (`insufficient permission for adding an object`). Repair: `chown -R 10000:10000 <repo>/.git` from the host — on the host the group `hermes` does not exist, so use numeric ids.

## Pitfalls

- `terminal(background=true, notify=true)` may serialize `notify` as string "True" → "notify must be true/false..." error; relaunch silent-background and drive it with `process(action='wait'/'poll')` (wait window is clamped to 60s — poll in a loop or run a blocking `while kill -0 <pid>; do sleep 10; done` in foreground with a generous timeout).
- Cron `script:` field must be a wrapper under `HERMES_HOME/scripts/`; scheduler validates the location.
- chown EVERYTHING the cron writes to (output dirs, job-id subdirs, repo copy under data/, ssh dir) — root-created files on the shared volume are read-only-ish traps for uid 10000.
- Symlinks created in MY `/opt/data` do NOT exist in the gateway's `/opt/data` (different dirs, same name). Only files under `data/` cross the boundary.
- IG Graph API renamed `media_id` → `ig_media_id` (mid-2026) on GET_IG_MEDIA/insights; link stickers on Stories unsupported by API; Meta FB photo/video upload >100MB → HTTP 413, serve `file_url` from the public portal instead.
- IG media insights are **media-type dependent**: Stories reject `likes/comments/saved/shares/total_interactions` ("not compatible with this media's product type"). Send a probe set and fall back — full set → `[views, reach, replies, navigation, follows]` → `[views, reach]` — keying the retry on the error text (`not compatible` / `does not support`). Fixed 2026-09-10 in `content-intel/harvest.py` (+ the `content-intel-build/` copy): harvest went 16/18 → 18/18.
