---
name: zig-best-practices
description: "Use when writing Zig systems code"
tags: [zig, sistemas, allocators, comptime, memoria, low-level]
license: MIT
compatibility: opencode
---

# Zig Best Practices

Guidelines for systems programming in Zig (0.13+).

## Rules
1. **Explicit Allocators**: Pass `std.mem.Allocator` explicitly to functions that allocate. Use `defer allocator.free(slice)` or ArenaAllocators.
2. **Comptime**: Use `comptime` for generic data structures and compile-time validation instead of macros or runtime reflection.
3. **Error Sets**: Use specific error sets and `try` / `catch` for explicit error propagation.
4. **Safety & Undefined**: Use `undefined` only when memory is immediately initialized. Verify bounds and pointer alignments.
