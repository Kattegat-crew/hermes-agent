---
name: brain-knowledge-base
description: "Use when setting up or maintaining the brain wiki."
tags: [wiki, brain, knowledge-base, notion, soul, memoria, empresa]
version: 1.0.0
author: Ragnar
license: MIT
metadata:
  hermes:
    tags: [wiki, knowledge-base, brain, business, memory]
    category: research
    related_skills: [llm-wiki, obsidian, dual-knowledge-system]
---

# Brain Knowledge Base Implementation

Practical lessons for implementing a compounding knowledge base in a business context.
Based on real implementation with Nexa Labs.

## When to Use
- Starting a new wiki/knowledge base
- Migrating from ad-hoc memory to structured wiki
- Deciding what goes in system prompt vs wiki
- Adapting wiki structure for business/agency use

## System Prompt vs Wiki: Know the Boundary

The system prompt (injected at session start) has a ~2200 char budget. The wiki has no such limit.

**System prompt** (critical, always-needed):
- Who you are (identity, role)
- Who the user is (name, role, preferences)
- Key IDs (Discord, Notion, GitHub)
- Current status (active systems, pending items)
- Hard rules (escalation protocol, communication style)

**Wiki** (deep, expandable, grows over time):
- Full profiles (detailed person/company pages)
- Architecture docs
- Decision history (ADRs)
- Research and comparisons
- Project status and history

**Rule:** If a fact is needed every session → system prompt. If referenced occasionally → wiki.

## Seeding a Wiki from Existing Knowledge

Don't wait for new sources. Seed immediately with what you already know:

1. Read your system prompt and extract key entities (people, companies, tools)
2. Read recent session summaries (via `session_search`) for decisions and context
3. Read any existing docs (SOUL.md, config files, TASKS.md)
4. Create entity/concept pages from this existing knowledge
5. This gives the wiki immediate utility instead of being empty

Example: When Nexa Labs' Brain was created, it was seeded with Jonathan's profile, Chucho's profile, company overview, infrastructure status, and operational rules — all pulled from system prompt and session history.

## Naming and Path Choice

The wiki path is just a configuration value. Pick a name that resonates with the user (`Brain`, `Wiki`, `Knowledge`).

**Key insight:** Changing the name later is a one-line config edit — no refactoring needed. There's no hardcoded reference to the wiki name anywhere.

**Docker environments:** Use absolute paths for stability: `/opt/data/brain/`

## Human vs Agent Knowledge Layers

Not all knowledge should live in the same place:

| Layer | Format | Audience | Example |
|---|---|---|---|
| Human-facing | Notion, visual docs | Jonathan, Chucho | Task boards, planning docs |
| Agent-facing | Markdown wiki | Ragnar | Research, technical docs, decisions |
| Shared | GitHub repos | Both | Code, architecture docs |

The wiki is the agent's "second brain" — it doesn't need to be pretty, it needs to be structured and searchable.

## Business Context Wiki Structure

For a business/agency context, adapt the directory structure:

```
brain/
├── tasks/             # **MANDATORY** — pending.md: cross-session task tracking
├── entities/          # People (Jonathan, Chucho), Companies (Nexa), Tools (Notion)
├── concepts/          # Methodologies, infrastructure, strategies
├── projects/          # Active workstreams with status
├── decisions/         # ADRs — why we chose X over Y
└── queries/           # Archived answers worth keeping
```

### Why `tasks/` Is Mandatory

The user has explicitly demanded persistent task tracking between sessions. Without it, tasks disappear on context compaction and the user has to repeat requests. See the `task-tracking` skill for the full implementation.

**Rule:** Every multi-step task MUST be tracked in `brain/tasks/pending.md`. Never rely on the `todo` tool for cross-session tracking.

### Why `decisions/` Matters
ADRs (Architecture Decision Records) prevent repeating debates that were already settled. When someone asks "why did we use Notion instead of Trello?", the answer is in `decisions/notion-vs-trello.md` with context, alternatives considered, and rationale.

### Entity Pages for Business
Each entity page should include:
- Overview / what it is
- Key facts and dates
- Relationships to other entities ([[wikilinks]])
- Current status (for tools/projects)
- Source references

## Implementation Steps

1. **Create directory structure** (`mkdir -p brain/{raw,entities,concepts,projects,decisions,queries}`)
2. **Write SCHEMA.md** — conventions, frontmatter format, tag taxonomy
3. **Write index.md** — sectioned catalog (will be populated as pages are created)
4. **Write log.md** — append-only action log
5. **Seed with existing knowledge** — create entity/concept pages from system prompt and session history
6. **Update index.md** — add all seeded pages
7. **Confirm ready** — suggest first sources to ingest

## Syncing Brain Wiki with Notion

When the user has Notion set up with databases that mirror the Brain Wiki structure:

**Rule:** Do NOT manually duplicate content. Create a sync script instead.

### Approach: Brain Wiki → Notion Bridge

1. **Verify Notion structure first** — search Notion API to see if equivalent DBs/pages exist
2. **If Notion already has the structure** → create a Python sync script that reads Brain Wiki files and updates Notion DBs automatically
3. **If Notion is empty** → create the DB structure first, then sync

### Sync Script Pattern

```python
# /opt/data/scripts/brain-to-notion-sync.py
import requests, json, os, glob

# Read all .md files from Brain Wiki
for md_file in glob.glob('/opt/data/brain/**/*.md', recursive=True):
    with open(md_file) as f:
        content = f.read()
    
    # Parse frontmatter to determine target Notion DB
    # Create/update page in Notion based on category
    # entities/ → entities DB
    # concepts/ → concepts DB
    # tasks/ → tasks DB
    # projects/ → projects DB
```

### Pitfalls

- **Don't seed an empty wiki** — use existing knowledge immediately
- **Don't put everything in system prompt** — reserve it for critical facts only
- **Don't forget decisions/** — ADRs are invaluable for business context
- **Don't make the wiki pretty** — it's for the agent, not humans. Humans use Notion.
- **Don't hardcode the path** — always read from config/env var
- **Don't duplicate what already exists in Notion** — always search first, then sync

## Deploying SOUL.md as System Prompt

When the user provides a SOUL.md (identity document), deploy it so it loads automatically on every session:

### Steps

1. **Save to Brain Wiki:** `write_file` to `/opt/data/brain/SOUL.md`
2. **Adjust infra reality:** Update any placeholders (model name, communication channel, infrastructure) with actual values from `config.yaml` and memory
3. **Wire into Hermes:** Set `prefill_messages_file: /opt/data/brain/SOUL.md` in `/opt/data/config.yaml`
4. **Verify:** Check that `config.yaml` has the line — it loads on next session start
5. **Update memory:** Add the path to memory so future sessions know about it

### Pitfalls

- **SOUL.md is not a skill** — it's the system prompt. Don't create a skill for it, load it via `prefill_messages_file`
- **The old SOUL might be hardcoded** — there may not be a file yet. Create one from scratch based on what the user describes
- **Always adjust infrastructure details** — the user's SOUL may have placeholder model/channel info. Replace with actuals from `config.yaml` and memory
- **After updating config, the change takes effect on NEXT session** — don't expect it to apply mid-session

## Renaming / Refactoring an Entity Page

When an entity's name is corrected (e.g. file was `jonathan_mendoza.md` but the
person is Jonathan Parra), renaming the file is NOT enough — wikilinks break.

### Steps (verified 31/07/2026)

1. **Rename the file:** `mv entities/old_name.md entities/new_name.md`
2. **Fix the content frontmatter/header** — write the corrected full content
3. **Search for ALL stale references:** `search_files(pattern='old_name', path='/opt/data/brain')`
   - Check `index.md` (catalog), other `entities/*.md` (Relations sections), `log.md`, `SCHEMA.md`
4. **Update every wikilink** `[[old_name]]` → `[[new_name]]` in the files that matter
   (index + related entities). `log.md` entries are historical — leave them.
5. **Watch for adjacent broken links** — while fixing one entity, grep the same
   files for other stale names (e.g. `[[jesus_chucho]]` pointing to a file that's
   actually `jesus_diaz.md`). Fix those too in the same pass.
6. **Verify:** `search_files(pattern='old_name', path='/opt/data/brain')` returns
   only historical log/SCHEMA mentions, no active broken links.

### Section-by-Section Voice Updates (informe ↔ brain workflow)

When the user reviews the Informe Maestro section by section via voice notes:

1. Read the current Google Doc to map its sections (plain-text headings `## ` / `### `)
2. For each section: update the corresponding brain entity file(s)
3. Also update the Hermes memory (`memory` tool) if the section changes user
   preferences/facts — memory is injected every session, brain is on-demand
4. Regenerate the informe from brain at the end (script), keeping brain as the
   single source of truth

## Downloading Files from Cloud Services

When browser is unavailable (Camofox not running) and `curl` is not installed, use Python `urllib.request`:

### Google Drive Download

```python
import urllib.request
import os

url = 'https://drive.google.com/uc?export=download&id=FILE_ID'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

with urllib.request.urlopen(req) as response:
    data = response.read()
    with open('/tmp/filename.md', 'wb') as f:
        f.write(data)
```

### Pitfalls

- **Google Drive returns HTML for large files** — if the downloaded file is HTML, the file may need browser rendering
- **Check file size** — if it's < 1KB, it's likely an error page, not the actual file
- **Always check first 500 chars** to confirm it's the expected content type
- **Use `urllib.request` as fallback** — if `curl` is not available (no `/usr/bin/curl`), use Python
