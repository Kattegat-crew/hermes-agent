---
name: docker-container-optimization
description: Docker container hardening, multi-stage builds, minimal base images, and caching layers.
license: MIT
compatibility: opencode
---

# Docker Container Optimization & Hardening

Best practices for containerizing production applications.

## Standards
1. **Multi-Stage Builds**: Separate build tools and dependencies from runtime artifacts.
2. **Minimal Images**: Use `distroless` or `alpine` for minimal surface area and CVE reduction.
3. **Non-Root User**: Always switch to a non-privileged user (`USER appuser` or `USER node`) in the final image.
4. **Layer Caching**: Copy lockfiles and install dependencies before copying source code.
5. **Healthchecks & Signals**: Define explicit `HEALTHCHECK` and handle `SIGTERM` gracefully for zero-downtime rolling updates.
