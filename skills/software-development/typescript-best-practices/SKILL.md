---
name: typescript-best-practices
description: TypeScript strict guidelines, advanced generics, utility types, and type-safe patterns.
license: MIT
compatibility: opencode
---

# TypeScript Best Practices

Guidelines for writing robust, type-safe, and idiomatic TypeScript code.

## Core Rules
1. **Strict Mode Always**: Ensure `strict: true` in `tsconfig.json`. Avoid `any`; use `unknown` with type narrowing.
2. **Discriminated Unions**: Model state transitions and domain entities with explicit `type` or `kind` discriminators.
3. **Immutability by Default**: Use `readonly` arrays and properties for domain invariants.
4. **Branded Types**: Use nominal/branded typing for IDs and critical primitives (e.g., `type UserId = string & { __brand: "UserId" }`).
5. **No Type Assertions without Proof**: Never use `as Type` unless interacting with non-typed external boundaries. Validate with Zod or Typebox.
6. **Utility Types**: Leverage `ReturnType`, `Parameters`, `Pick`, `Omit`, `Record`, and `Extract` rather than duplicating types.
