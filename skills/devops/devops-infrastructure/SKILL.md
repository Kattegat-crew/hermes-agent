---
name: devops-infrastructure
description: "Use when auditing servers, containers or health monitors."
tags: [devops, infraestructura, monitoreo, contenedores, oom, salud, crons, conexiones]
---
# DevOps & Infrastructure Monitoring

Use when configuring, auditing, or maintaining server-side services, containers, or automated monitoring workflows.

## Core Philosophy
- **Stability First.** High-availability (HA) and resource limits (OOM prevention) are prioritized over rapid feature deployment.
- **Observability is non-negotiable.** Every service must have a health check, and every critical job must have logs that are accessible and actionable.
- **Identity-Aware Infrastructure.** Infrastructure is managed per tenant or per user profile (e.g., `helmer-gmail`, `jonathan-canva`).

## Monitoring & Health Checks
- **The Vigía Pattern:** Regular (e.g., every 2h) automated health checks for webhooks, ActivePieces, DBs, and critical flows.
- **OOM Prevention:** Always set `mem_limit` on containers. Use the "Measure → Limit" approach: observe normal usage, then set the limit to `usage * 2` to provide a safety ceiling without causing unnecessary kills.
- **Reporting:** Use Discord/Telegram for alerts. Maintain a distinction between "System Health" (technical uptime) and "Business/Marketing QA" (content quality).

## Identity & Connection Governance
- **Multi-Tenant Management:** When managing OAuth or sensitive connections, use a naming convention `{tenant}-{service}` to prevent cross-account leakage.
- **The 5 Layers of Connection Security:**
  1. **SOUL:** Agent identity defines allowed connections.
  2. **Engram Map:** A persistent mapping of `tenant -> connection_id` used for lookup.
  3. **Project Isolation:** Use separate AP Projects/Workspaces when scaling (Premium tier).
  4. **Auditor:** Continuous monitoring of connection usage (Vigía).
  5. **Technical Enforcement (The Law):** A wrapper (e.g., `ap_call`) that validates the caller's identity against the Engram map before executing the tool call.

## Troubleshooting & Maintenance
- **Log-First approach:** Before guessing a cause, check `docker logs`, `nginx` error logs, or specialized service logs.
- **_OOMKilled_ detection:** If a service dies, check if it was an Out-Of-Memory event.
- **Permission Fixes:** When encountering `Permission denied` on config files, ensure ownership is set to the service user (e.g., `chown hermes:hermes`).

## Automation & Cron Jobs
- **Job Ownership:** Distinguish between *System/Maintenance Crons* (Vigía/Infra) and *User/Personal Crons* (Ragnar/Roshi).
- **Continuous Learning:** Use memory-saving crons to ensure agents maintain their context and history.
- **Error Handling:** Ensure crons are non-interactive and deliver status via designated channels.

## Reference Files
- `references/connection-governance-layers.md`: Detailed breakdown of the 5-layer security model for multi-tenant integrations.
- `references/vigia-prod-audit-checks.md`: Vigía's verified prod checks (Golden/Paradise webhooks, ActivePieces flows, nightly email `accepted` via `file.FLOW_RUN_LOG`, `ap-db` vs `nca-postgres`, Discord delivery pitfalls).
