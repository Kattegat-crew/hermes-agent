---
name: testing-best-practices
description: "Use when writing unit or integration tests"
tags: [testing, tests, unit, integration, mocking, cobertura, tdd, calidad]
license: MIT
compatibility: opencode
---

# Testing Best Practices

Comprehensive engineering guidelines for software testing and verification.

## Testing Standards
1. **Test Pyramid**: 70% Unit tests (fast, isolated), 20% Integration tests (database, services), 10% E2E tests (critical paths).
2. **Arrange-Act-Assert (AAA)**: Structure every test clearly into setup, execution, and verification phases.
3. **Test Behavior, Not Implementation**: Verify public API contracts and side-effects, not internal private state.
4. **Deterministic Fixtures**: Never depend on random seeds or external network state. Mock external dependencies.
5. **Edge Cases & Failure Modes**: Always test error paths, timeouts, empty collections, and boundary limits.
