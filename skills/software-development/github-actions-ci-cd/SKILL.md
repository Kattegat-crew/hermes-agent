---
name: github-actions-ci-cd
description: "Use when authoring a GitHub Actions CI/CD pipeline."
tags: [github-actions, ci-cd, workflows, matrix-builds, secrets]
license: MIT
compatibility: opencode
---

# GitHub Actions CI/CD Mastery

Production CI/CD workflow architecture.

## Principles
1. **Speed**: Use native caching (`actions/cache`, `actions/setup-node` with `cache: 'npm'`).
2. **Security**: Pin actions to full SHA commits. Restrict `GITHUB_TOKEN` permissions with the least-privilege `permissions:` block.
3. **Matrix Testing**: Run unit and integration tests across target Node/Python/Go versions and OS platforms concurrently.
4. **Automated Releases**: Automate semantic version tagging and release notes generation on main branch merge.
