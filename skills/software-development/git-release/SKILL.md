---
name: git-release
description: Create consistent tagged releases, changelogs, and version bumps with gh release create.
license: MIT
compatibility: opencode
---

# Git Release Workflow

Automated workflow for generating changelogs, tagging releases, and publishing GitHub releases.

## Workflow Steps
1. Inspect merged pull requests and commit history since the previous git tag.
2. Determine semantic version bump (Major, Minor, Patch).
3. Generate structured release notes categorized by Features, Bug Fixes, and Breaking Changes.
4. Provide and execute `gh release create vX.Y.Z --title "vX.Y.Z" --notes "..."`.
