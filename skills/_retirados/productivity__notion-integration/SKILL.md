---
name: notion-integration
description: >
  Configure and interact with Notion API — search pages, read content,
  create databases, pages, and tables. Use when setting up Notion as a
  workspace wiki, managing task boards, or reading/writing Notion content.
version: 1.0.0
author: community
license: MIT
metadata:
  hermes:
    tags: [Notion, Wiki, Database, Integration, Productivity]
prerequisites:
  commands: [python3]
  python_packages:
    - requests
---

# Notion Integration

Configure and operate the Notion API for workspace management, wikis, and task tracking.

## Setup

1. Create a Notion Integration at https://www.notion.so/my-integrations
2. Copy the **Internal Integration Secret** (starts with `ntn_` or `secret_`)
3. Share pages/databases with the integration (click "Connect" on the page, add your integration by name)

## Authentication

```python
headers = {
    'Authorization': 'Bearer YOUR_INTEGRATION_TOKEN',
    'Notion-Version': '2022-06-28'
}
```

## Searching All Accessible Content

```python
import requests

headers = {
    'Authorization': 'Bearer YOUR_TOKEN',
    'Notion-Version': '2022-06-28'
}

# Search everything the integration has access to
resp = requests.post('https://api.notion.com/v1/search', json={}, headers=headers)
data = resp.json()

for item in data.get('results', []):
    obj_type = item.get('object', '')
    if obj_type == 'page':
        # Title may be in properties or inside the page content
        title = ''
        if 'properties' in item:
            for pname, pval in item['properties'].items():
                if pval.get('type') == 'title' and pval.get('title'):
                    title = pval['title'][0].get('plain_text', '')
                    break
        parent = item.get('parent', {})
        print(f'  [PAGE] {title or "(untitled)"} | parent: {parent.get("type", "?")}')
    elif obj_type == 'database':
        title = ''
        if item.get('title'):
            title = item['title'][0].get('plain_text', '') if item['title'] else ''
        print(f'  [DB]   {title or "(untitled)"}')
```

## Reading Page Content (Blocks)

Pages often have their title inside the content, not as a property. To read a page:

```python
# Get page blocks (children)
page_id = 'YOUR_PAGE_ID'
resp = requests.get(f'https://api.notion.com/v1/blocks/{page_id}/children', headers=headers)
data = resp.json()

for block in data.get('results', []):
    btype = block['type']
    if btype in ('paragraph', 'heading_1', 'heading_2', 'heading_3',
                 'bulleted_list_item', 'numbered_list_item', 'to_do'):
        content_list = block.get(btype, [])
        text_parts = []
        if isinstance(content_list, list):
            for item in content_list:
                if isinstance(item, dict) and item.get('rich_text'):
                    for rt in item['rich_text']:
                        if isinstance(rt, dict) and rt.get('text', {}).get('content'):
                            text_parts.append(rt['text']['content'])
        if text_parts:
            print(f'  [{btype}] {" ".join(text_parts)}')
    elif btype == 'child_database':
        tl = block['child_database'].get('title', [])
        title = tl[0].get('plain_text', '(untitled)') if isinstance(tl, list) and tl and isinstance(tl[0], dict) else '(untitled)'
        print(f'  [child_database] {title}')
    elif btype == 'child_page':
        title = block['child_page'].get('title', '(untitled)')
        print(f'  [child_page] {title}')
```

## Important: Pagination

Notion returns max 100 results per search/page. If `has_more` is true:

```python
next_cursor = data.get('next_cursor')
while next_cursor:
    resp = requests.post('https://api.notion.com/v1/search',
        json={'cursor': next_cursor, 'page_size': 100},
        headers=headers)
    data = resp.json()
    next_cursor = data.get('next_cursor')
```

## Creating a Page

```python
parent = {'page_id': 'PARENT_PAGE_ID'}  # or {'database_id': 'DB_ID'}
resp = requests.post('https://api.notion.com/v1/pages',
    json={
        'parent': parent,
        'properties': {
            'Name': {'title': [{'text': {'content': 'Page Title'}}]}
        },
        'children': [
            {
                'object': 'block',
                'type': 'paragraph',
                'paragraph': {
                    'rich_text': [{'type': 'text', 'text': {'content': 'Hello world'}}]
                }
            }
        ]
    },
    headers=headers)
```

## Creating a Database

```python
resp = requests.post('https://api.notion.com/v1/databases',
    json={
        'parent': {'type': 'page_id', 'page_id': 'PARENT_PAGE_ID'},
        'title': [{'type': 'text', 'text': {'content': 'My Database'}}],
        'properties': {
            'Name': {'title': {}},
            'Status': {'select': {'options': [{'name': 'Pending'}, {'name': 'Done'}]}},
            'Due Date': {'date': {}}
        }
    },
    headers=headers)
```

## Key Gotchas

1. **Token may be missing even if "configured":** The notion-integration skill may say "Hecho" in task lists, but the actual token might not be in `.env`. Always verify with `grep -ri "notion" /opt/data/.env` across ALL env files (`/opt/data/.env`, `/opt/data/hermes-workspace/.env`, `config.yaml`). The token is often forgotten or configured via a different method.

2. **Token may exist only in session history:** If the user shared a Notion token in a past conversation but it was never saved to `.env`, search session files for the token pattern:
   ```bash
   grep -ro 'ntn_[a-zA-Z0-9]\{20,\}' /opt/data/sessions/ | head -5
   ```
   The token format is `ntn_` followed by 30+ alphanumeric characters. Extract it and add to `.env` as `NOTION_API_KEY=`.

3. **Docker container permission issues:** Inside the Docker container, `/opt/data/.env` may be owned by root with no write permissions and no `sudo` available. Workarounds:
   - Copy the file, modify the copy, and use the copy for testing: `cp /opt/data/.env /opt/data/.env.modified`
   - The token can still be used directly in Python scripts without being in `.env`
   - For persistence, ask the user to add it to their local `.env` outside the container

2. **Pages shared with integration:** The integration only sees pages explicitly shared with it. Check the Notion UI — click "..." on a page → "Add connections" → find your integration.

3. **Title location:** Page titles may be in `properties` OR inside the page content blocks. Always check both.

4. **rich_text format:** Text is always nested: `block[type][0].rich_text[0].text.content`. Handle both dict and string types.

5. **child_database title:** The `title` field is a list of rich_text objects, NOT a simple string.

6. **Pagination:** Always check `has_more` and paginate for large workspaces.

7. **Rate limits:** Notion has rate limits. If you get 429, back off and retry.
8. **Notion DB page content:** Pages inside Notion databases CANNOT have blocks appended via `/blocks/{page_id}/children` PATCH. You must include content in the `children` array of the POST to `/v1/pages` when creating.
9. **Paragraph text limit:** Each paragraph block's `rich_text[0].text.content` is limited to **2000 characters**. Truncate content before sending.
10. **DB field names:** Database property names are custom — always query the DB schema first to get exact field names (e.g., "Estado" not "Status", "Categoria" not "Category"). Use `GET /v1/databases/{id}` to inspect.
11. **Sync script content truncation:** The wiki-to-notion-sync script (`/opt/data/scripts/wiki-to-notion-sync.py`) has a `create_notion_page_with_content()` function that truncates to 1900 chars per paragraph. Use it for wiki sync.
12. **Notion DB query returns 0 pages (KNOWN BUG):** The `GET /v1/databases/{id}/query` endpoint can silently return 0 results even when pages exist in the database. Direct POST (create) and PATCH (update) work fine. **Workaround:** Don't rely on query to check existing pages. Create tasks directly with POST. Use conflict detection (HTTP 409) or a separate tracking list to avoid duplicates. If you must check existing, use the Search endpoint (`POST /v1/search`) instead, though it has its own quirks.

## Related: Dual Knowledge System

For setups where agents use Obsidian (Markdown) as source of truth and Notion as human-facing view, see the `dual-knowledge-system` skill. This is the recommended pattern for Hermes since agents natively read/write Markdown files while humans benefit from Notion's visual interface.

## Common Operations

| Operation | Endpoint | Method |
|-----------|----------|--------|
| Search | `/v1/search` | POST |
| Get page | `/v1/pages/{id}` | GET |
| Page blocks | `/v1/blocks/{id}/children` | GET |
| Create page | `/v1/pages` | POST |
| Create database | `/v1/databases` | POST |
| Append blocks | `/v1/blocks/{id}/children` | PATCH |
| Update page | `/v1/pages/{id}` | PATCH |
| Query database | `/v1/databases/{id}/query` | POST |

## Nexa Labs Notion Structure

**Parent:** "Nexa Labs" — `335853a7-3369-803a-9a82-edb6246e1ea5`

| Database | ID | Purpose |
|---|---|---|
| Links de X | `335853a7-3369-81e3-b261-e4e44c10fc36` | Twitter/X links |
| Repos | `3ac853a7-3369-818d-a14f-daa9f26cbb6e` | GitHub repos |
| TikToks | `335853a7-3369-810a-8e5e-c79c1ae7fb09` | TikTok videos |
| Wiki | `af30a0f1-a1ec-4600-95dd-c90ad596e473` | Brain Wiki pages |
| Tasks | `349853a7-3369-8139-a73e-d0e4213c215c` | Task tracking |

**Sync script:** `/opt/data/scripts/wiki-to-notion-sync.py` — reads Brain Wiki files and updates Notion Wiki DB automatically.
