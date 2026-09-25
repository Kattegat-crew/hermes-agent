---
name: redis-caching-patterns
description: "Use when adding Redis caching, locks or rate limiting"
tags: [redis, caching, cache-aside, redlock, rate-limiting, ttl, distributed-locks]
license: MIT
compatibility: opencode
---

# Redis Caching & In-Memory Patterns

Guidelines for using Redis effectively as a cache, message broker, and distributed lock.

## Key Patterns
1. **Cache-Aside Pattern**: Read from cache; on miss, query database, write to cache with TTL, and return.
2. **Cache Invalidation & TTL**: Always set realistic TTLs (Time-To-Live) and use jitter to prevent cache stampedes.
3. **Distributed Locking**: Use Redlock or atomic `SET resource_key token NX PX 30000` with Lua script unlock for safe concurrency.
4. **Sliding-Window Rate Limiting**: Implement rate limiters using Redis sorted sets (`ZADD`, `ZREMRANGEBYSCORE`).
