---
name: git-worktree-tidy
description: Clean up and maintain Git worktrees, pruning stale branches and freeing disk resources.
license: MIT
compatibility: opencode
---

# Git Worktree Tidy

Guidelines for managing multiple Git worktrees cleanly.

## Commands
1. List active worktrees: `git worktree list`.
2. Remove completed worktree: `git worktree remove <path>`.
3. Prune dangling references: `git worktree prune`.
