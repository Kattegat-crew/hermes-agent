---
name: electrobun-best-practices
description: Electrobun desktop app development, native webview configurations, CEF bundling, and IPC bridges.
license: MIT
compatibility: opencode
---

# Electrobun Best Practices

Guidelines for building lightweight, fast desktop applications with Electrobun.

## Standards
1. **Configuration**: Define entry points and bundle settings in `electrobun.config.ts`.
2. **Linux CEF Bundling**: Enable `bundleCEF: true` for Linux builds to guarantee consistent rendering across distributions.
3. **Type-Safe IPC**: Define clear request-response schemas for communication between the Bun main process and the WebView UI.
