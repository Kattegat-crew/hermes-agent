---
name: tamagui-best-practices
description: Tamagui UI framework best practices, compiler optimization, multiplatform design tokens, and theme configuration.
license: MIT
compatibility: opencode
---

# Tamagui Best Practices

Standards for building fast cross-platform applications with Tamagui.

## Rules
1. **Compiler Optimization**: Ensure the Tamagui compiler is enabled to extract static CSS and optimize styled components.
2. **Theme Configuration**: Centralize palettes, themes, and design tokens in `tamagui.config.ts`.
3. **Adaptive UI**: Use the `Adapt` primitive to render native sheets on mobile and popovers/modals on web.
4. **Performance**: Prefer `styled()` components over inline style objects to maximize compile-time CSS extraction.
