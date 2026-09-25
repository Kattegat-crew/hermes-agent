---
name: react-best-practices
description: "Use when building React 18/19 apps"
tags: [react, componentes, hooks, frontend, ssr, state, performance]
license: MIT
compatibility: opencode
---

# React Best Practices

Master guidelines for building scalable, maintainable React applications (React 18/19+).

## Architectural Principles
1. **Container / Presentational Separation**: Keep business logic, data fetching, and state management isolated from visual dumb components.
2. **Server vs Client Components**: Default to Server Components for data fetching and static markup; isolate `'use client'` to interactive leaves.
3. **Hook Architecture**: Encapsulate complex state machines and API interactions in custom hooks (`useFeatureWorkflow`).
4. **Clean Effect Usage**: Avoid `useEffect` for derived state. Calculate values during render or use `useMemo`.
5. **Component Composition over Prop Drilling**: Use children composition and Context/Zustand when sharing state across deep subtrees.
6. **Suspense & Error Boundaries**: Wrap asynchronous boundaries with meaningful fallback states and localized error recovery.
