---
name: github-actions-ci-cd
description: GitHub Actions pipelines, workflow optimization, matrix builds, automated testing, and secure secret deployments.
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
