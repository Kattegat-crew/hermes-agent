---
name: locate-shared-resource
description: "Use when locating a repo or tweet shared to the team."
tags: [session-search, sqlite, state-db, notion, telegram, retrieval]
---

# Locate Shared Resource

Workflow for tracking down a resource the team shared, before assuming it is a file. Used when a user remembers a repo/tweet/session by a fuzzy name but not its location.

## Order of attack (cheapest → broadest)

1. **`session_search`** tool first — searches the session DB by content.
2. **Direct SQLite on `/opt/data/state.db`** — the reliable fallback when `session_search` misses channel-specific or title-only hits.
3. **Notion DBs** for the curated channel dumps.
4. **`search_files` on `/opt/data/brain/`** for saved analyses (`raw/`, `entities/`, `concepts/`).
5. **Filesystem `find`** only as a last resort — see pitfall below.

## Searching channel history via state.db

The canonical Hermes session DB is `/opt/data/state.db` (same file as `/root/hermes-agent/data/state.db` on the host). Two tables matter:

- `sessions(id, session_key, chat_id, chat_type, display_name, title, source, ...)`
- `messages(id, session_id, role, content, tool_name, timestamp, ...)`
- FTS mirror: `messages_fts(rowid→messages.id, content)` + `messages_fts_trigram`.

Known Telegram group channel IDs:
- **Links de X**: `-1003820724234`
- **Repos Git**: `-1003572354527`
- **TikToks**: `-1003869738224`

### Find sessions from a channel
```sql
SELECT id, title, message_count, last_activity_at
FROM sessions WHERE chat_id LIKE '%1003820724234' ORDER BY last_activity_at DESC;
```

### Find messages matching a term across channel sessions
```sql
SELECT m.session_id, m.role, substr(m.content,1,400)
FROM messages m JOIN sessions s ON m.session_id = s.id
WHERE s.chat_id LIKE '%1003572354527' AND m.content LIKE '%term%';
```
Prefer `messages_fts MATCH` (accent/word aware) for fuzzy terms; fall back to `LIKE %term%` for raw substrings.

### Critical pitfall — the resource may be a SESSION TITLE, not a file
Hermes Desktop conversations get auto-titled and live in `sessions.title`. A user saying "me dejó un archivo con un nombre como configbotchucho" almost certainly means a **Desktop session titled that**, not a file on disk.

Query before touching `find`:
```sql
SELECT id, title, source, chat_id, started_at, last_activity_at
FROM sessions WHERE title LIKE '%chucho%' OR title LIKE '%config%';
```
Do NOT run `find / -name '*name*'` first — named sessions that are not files cost you a wasted filesystem sweep.

### Pitfall — processed-in-DM/desktop items may have chat_id NULL
Some resources get analyzed in direct messages or Hermes Desktop, so `sessions.chat_id` is NULL even though the analysis is in the DB. If a channel-only search comes up empty, widen to all sessions (`WHERE chat_id IS NULL OR source IN ('desktop','telegram')`).

### Pitfall — JSON session files don't reliably carry chat_id
The `.json` session dumps frequently omit `chat_id`/`session_key`, so grepping them by channel ID is unreliable. **Trust `state.db`, not the JSON dumps**, when you must scope a search to a specific channel.

## Notion DBs (curated channel dumps)

The channel ingestion flow saves analyzed links to Notion. Look these up before reinventing:
- "Links de X" DB and "Repos" DB both accept `POST .../v1/databases/{id}/query` with a filter; check `Tema`/`Resumen`/`Name` for the resource.
- Known-good "Links de X" DB id: `3ae853a7-3369-81f4-9581-fcc41b5c5ea4` (verified; other on-disk IDs were stale).
- Notion token lives in `/opt/data/.env` as `NOTION_TOKEN`/`NOTION_API_KEY` (parse the file manually; not exported to env).

## Reusable script

`scripts/scan_channel_history.py` — scans `state.db` channel sessions for a keyword and prints hits. Run with `python3`.

## Related
- `twitter-telegram-ingestion` — the ingestion side (how links get INTO these channels/Notion).
- `notion-integration` — general Notion API usage.
- When the "resource" is an external URL the user wants analyzed, hand off to `agent-reach` / `x-tweet-scrape`.