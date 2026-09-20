---
name: git-rebase-sync
description: Synchronize local branches with upstream using interactive rebase and clean conflict resolution.
license: MIT
compatibility: opencode
---

# Git Rebase & Sync

Workflow for safely updating branches with upstream changes.

## Workflow
1. Fetch latest changes from remote: `git fetch origin main`.
2. Rebase feature branch: `git rebase origin/main`.
3. Resolve conflicts deliberately, verifying tests at each step.
4. Push safely using `git push --force-with-lease`.
