---
name: git-best-practices
description: Git workflow best practices, conventional commits, atomic changes, branch management, interactive rebase, and clean history maintenance.
license: MIT
compatibility: hermes, opencode, bash
metadata:
  hermes:
    tags: [git, commits, rebase, conventional-commits, version-control, workflow]
    category: software-development
---

# Git Best Practices & Clean History Standards

Architectural guidelines and conventions for maintaining an auditable, bisectable, and clean Git history across multi-agent and engineering teams.

## 1. Commit Hygiene & Conventions

### A. Conventional Commits Standard
Commit messages must strictly follow the conventional commits specification:
- `feat(<scope>): <description>` - A new user-facing capability.
- `fix(<scope>): <description>` - A bug fix.
- `refactor(<scope>): <description>` - Code change that neither fixes a bug nor adds a feature.
- `docs(<scope>): <description>` - Documentation-only changes.
- `test(<scope>): <description>` - Adding or correcting tests.
- `chore(<scope>): <description>` - Maintenance, build, or dependency updates.

### B. Atomic Work Units
- **One Logical Change per Commit**: Keep changes small, coherent, and bisectable.
- **Never Add AI Attribution**: Never inject `Co-Authored-By` or AI attribution markers. Use clean conventional messages only.

---

## 2. Branch Synchronization & Interactive Rebase

Keep feature branches aligned with upstream without creating messy merge bubbles.

```bash
# 1. Fetch latest upstream commits
git fetch origin main

# 2. Rebase feature branch on top of main
git rebase origin/main

# 3. Interactive squash or edit of recent WIP commits
git rebase -i HEAD~3

# 4. If conflicts occur:
# Inspect conflicting files
git status
# Edit files to resolve conflicts, then stage them
git add <resolved_files>
# Continue rebase (DO NOT git commit)
git rebase --continue
# To abort if needed:
# git rebase --abort

# 5. Push updated history safely (NEVER use raw --force)
git push --force-with-lease origin <feature_branch>
```

---

## 3. Production Invariants for Agents

1. **Verify Before Commit**: Always run linting or local test suites before committing. A broken commit breaks `git bisect`.
2. **Never Commit Secrets**: Audit `git status` and `git diff --cached` before committing to prevent leaking API keys, `.env` files, or passwords.
3. **Squash Spurious Commits**: Consolidate "fix typo", "wip", "debug" micro-commits into meaningful work units before merging.
