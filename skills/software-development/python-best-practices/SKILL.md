---
name: python-best-practices
description: "Use when writing idiomatic Python 3.12+ code"
tags: [python, asyncio, pydantic, typing, tipado, ruff, uv, backend]
license: MIT
compatibility: opencode
---

# Python Best Practices

Guidelines for production-grade Python services, scripts, and libraries.

## Core Tenets
1. **Type Annotations & Validation**: Type all function signatures. Use Pydantic v2 for data parsing and validation.
2. **Modern Concurrency**: Use `asyncio` with `asyncio.TaskGroup` for structured async execution. Never block the event loop with synchronous I/O.
3. **Explicit Error Handling**: Define custom domain exception hierarchies. Avoid bare `except:`.
4. **Modern Tooling**: Prefer `uv` or `poetry` for dependency management; use `ruff` for linting and formatting.
5. **Context Managers**: Always manage resources (files, DB connections, HTTP clients) with `with` or `async with`.
6. **Dataclasses & Pydantic**: Use `@dataclass(slots=True, frozen=True)` for pure data transfer objects.
