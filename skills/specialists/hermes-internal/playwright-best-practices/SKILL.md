---
name: playwright-best-practices
description: Reliable E2E browser automation, Page Object Model, semantic locators, and resilient test fixtures.
license: MIT
compatibility: opencode
---

# Playwright Best Practices

Guidelines for writing robust, non-flaky End-to-End tests.

## Rules
1. **User-Facing Locators**: Prioritize `getByRole`, `getByText`, `getByLabel` over fragile CSS/XPath selectors.
2. **Auto-Waiting**: Rely on Playwright built-in web-first assertions (`await expect(locator).toBeVisible()`). Avoid hardcoded sleeps (`page.waitForTimeout`).
3. **Page Object Models (POM)**: Encapsulate UI interactions and page selectors inside dedicated Page Classes.
4. **Isolated Test State**: Each test must run in a clean BrowserContext with its own authentication state or seeded data.
5. **Network Mocking & Interception**: Mock third-party APIs with `page.route()` to make tests deterministic and fast.
