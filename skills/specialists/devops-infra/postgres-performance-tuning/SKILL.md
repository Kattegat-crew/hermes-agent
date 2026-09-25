---
name: postgres-performance-tuning
description: "Use when tuning PostgreSQL queries, indexes or pooling"
tags: [postgresql, explain-analyze, indexing, gin, pgbouncer, query-tuning, database]
license: MIT
compatibility: opencode
---

# PostgreSQL Performance Tuning

Production guidelines for database indexing, query optimization, and scalability.

## Optimization Rules
1. **Query Inspection**: Always run `EXPLAIN (ANALYZE, BUFFERS)` to detect sequential scans on large tables.
2. **Index Strategy**:
   - B-Tree for equality and range queries.
   - GIN for JSONB and Full-Text Search.
   - Partial indexes for filtered subsets (`WHERE status = 'active'`).
   - Composite indexes following left-to-right query patterns.
3. **Connection Pooling**: Use PgBouncer or Supabase pooler to prevent backend connection saturation.
4. **N+1 Prevention**: Eager-load relations or use `JOIN` / `json_agg` subqueries.
