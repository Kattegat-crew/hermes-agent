---
name: skill-navigator
description: Navigate, query, and compose skills and execution pipelines using the skills knowledge graph and index.
license: MIT
compatibility: opencode
---

# Skill Navigator: Graph & Pipeline Resolution

Use this skill when you need to identify the exact constellation of skills and sequential execution pipelines required to solve a complex engineering task.

## When to use me
- When facing a multi-phase or cross-domain project (e.g., Full Stack SaaS, Complex AI Pipeline, Security Hardening + DevOps).
- When unsure which of the 312 skills are best suited for the current task.
- To discover pipeline sequences without context bloat.

## 1. Quick Category Lookup
Inspect `/root/.config/opencode/skills/SKILLS_INDEX.md` to identify the relevant technical domain:
- `1. Metodología & Loops Autónomos (Superpowers & SDD)`
- `2. Arquitectura, Clean Design & Refactoring`
- `3. Frontend, UI/UX, Mobile & Desktop`
- `4. Backend, APIs, Concurrencia & Bases de Datos`
- `5. Testing, QA & E2E Automation`
- `6. Git, GitHub & Code Review`
- `7. DevOps, Cloud, Contenedores & Linux`
- `8. IA, LLMs, Vector DBs & MLOps`
- `9. Seguridad, Pentesting & Hardening`
- `10. Investigación, Scraping & OSINT`
- `11. Productividad & SaaS Integrations`
- `12. Multimedia, Video & Arte Generativo`
- `13. Web3/Blockchain & Ciencia de Datos`

## 2. Graph Navigation Commands (Graphify)
Query the knowledge graph in `/root/.config/opencode/skills/graphify-out/`:

- **Query Domain Clusters**:
  ```bash
  graphify query "nextjs frontend performance" --graph /root/.config/opencode/skills/graphify-out/graph.json
  ```
- **Find Pipeline Execution Path**:
  ```bash
  graphify path "brainstorming" "playwright-best-practices" --graph /root/.config/opencode/skills/graphify-out/graph.json
  ```
- **Inspect Specific Skill Nodes**:
  ```bash
  graphify explain "clean-architecture-patterns" --graph /root/.config/opencode/skills/graphify-out/graph.json
  ```

## 3. Standard Execution Pipelines
- **Full-Stack Feature**: `brainstorming` ➔ `writing-plans` ➔ `clean-architecture-patterns` ➔ `test-driven-development` ➔ `playwright-best-practices` ➔ `verification-before-completion` ➔ `git-release`
- **Backend High-Load**: `domain-driven-design` ➔ `postgres-performance-tuning` ➔ `redis-caching-patterns` ➔ `websockets-realtime-ops` ➔ `docker-container-optimization`
- **AI / LLM Application**: `instructor` ➔ `outlines` ➔ `rag-architecture-expert` ➔ `qdrant` / `pinecone` ➔ `unsloth`
