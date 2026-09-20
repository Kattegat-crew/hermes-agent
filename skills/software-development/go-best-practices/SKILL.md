---
name: go-best-practices
description: Idiomatic Go code, concurrency patterns with goroutines/channels, small interfaces, and robust error handling.
license: MIT
compatibility: opencode
---

# Go Best Practices

Standards and architectural conventions for writing clean, robust Go software.

## Fundamentals
1. **Explicit Error Handling**: Always check and wrap errors (`fmt.Errorf("action: %w", err)`). Never discard errors with `_`.
2. **Context Propagation**: The first argument in I/O operations must be `ctx context.Context`. Respect cancellation and deadlines.
3. **Small, Focused Interfaces**: Define interfaces where they are consumed, not where they are implemented. Keep interfaces minimal (1-3 methods).
4. **Concurrency Safety**: Protect shared state with `sync.Mutex` or communicate via channels. Always ensure goroutines have a guaranteed exit path.
5. **Package Layout**: Follow `cmd/`, `internal/`, `pkg/` structure. Avoid package name collisions and circular dependencies.
