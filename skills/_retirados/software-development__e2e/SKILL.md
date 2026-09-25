---
name: e2e
description: End-to-End testing architecture, multi-service orchestration, test database isolation, and reporting.
license: MIT
compatibility: opencode
---

# End-to-End (E2E) Testing Architecture

Guidelines for orchestrating complete integration and E2E testing pipelines.

## Principles
1. **Environment Setup**: Spin up isolated test containers for DB, Redis, and backend services before running tests.
2. **Seed Data Management**: Use idempotent database seed scripts and reset hooks between test runs.
3. **Flakiness Elimination**: Replace arbitrary timers with explicit condition polling and event triggers.
