---
name: tailwind-design-system
description: Scalable Tailwind CSS systems, design tokens, component architecture, and accessibility compliance.
license: MIT
compatibility: opencode
---

# Tailwind CSS & Design System Architecture

Standards for building accessible, maintainable design systems with Tailwind CSS.

## Best Practices
1. **Semantic Color Tokens**: Define theme colors semantically (`bg-surface`, `text-primary`, `border-muted`) rather than hardcoded hex values.
2. **Component Abstractions**: Use `cva` (Class Variance Authority) or `tailwind-merge` + `clsx` for variant management.
3. **Accessibility (a11y)**: Integrate Radix UI / Headless UI primitives for ARIA roles, focus trapping, and keyboard navigation.
4. **Responsive & Dark Mode**: Always design mobile-first and verify dark mode contrast ratios (WCAG AA standard).
