---
name: activepieces-flow-editing
description: Edit AP flows/templates via DB and verify the run used it.
author: Ragnar
version: "1.0"
created: 2026-08-25
category: devops
metadata:
  hermes:
    tags: [activepieces, flows, webhook, email-template, db-editing, run-verification, self-hosted, lead-automation]
    related_skills: [activepieces-selfhost-ops, activepieces-lead-automation, webhook-gateway-multiclient]
---

# ActivePieces Flow Editing & Run Verification (self-hosted, via direct DB)

## When to Use

- Changing a flow's **email HTML/layout**, recipients, or step timing, then confirming the executed run/email output.
- The AP **API/MCP auth returns 401/406** (or hangs) — the reliable route is **direct DB**, not the API.
- Flow runs are missing / templates look stale / an address field overflows — likely a `trigger_source` misalignment.
- You need the **actual emitted output** (email `accepted`, sheet row) from a run, not just `SUCCEEDED`.

## Core rule (the #1 gotcha)

The engine resolves **which flow version a webhook executes from `trigger_source.flowVersionId`**, NOT (only) `flow.publishedVersionId`.
If `trigger_source.flowVersionId` points at a **deleted** version, the webhook runs a **stale/cached template** and runs become unstable (404s, missing fields, wrong layout). Editing `flow_version.trigger` alone does NOT take effect.

So: edit → rewire `trigger_source` → restart BOTH engines → verify version.

## Steps (exact order)

1. **Backup** the trigger: `docker exec ap-db psql -U postgres -d activepieces -tAc "SELECT trigger::text FROM flow_version WHERE id='<vid>'" > backup.json` (back up before every write).
2. **Read** `flow_version.trigger` (JSON). The email HTML lives at step `displayName` → `settings.input.body.html`. Body may be a **dict** `{html, text}` OR a **plain string** — handle both. Walk steps via `nextAction`.
3. **Edit** the HTML. Placeholders are `{{trigger.body.<field>}}` (e.g. `{{trigger.body.sede}}`, `{{trigger.body.bonus_display}}`).
4. **Write back**: `UPDATE flow_version SET trigger='<json>'::jsonb, updated=now() WHERE id='<vid>'`. **Must** escape every `'` as `''` in the JSON (`.replace("'","''")`); a stray `'` silently breaks the literal.
5. **Rewire trigger_source** (every row of the flow): `UPDATE trigger_source SET "flowVersionId"='<published_vid>' WHERE "flowId"='<id>'`. Confirm `flow.publishedVersionId` equals the edited version.
6. **Restart BOTH `ap-app` AND `ap-worker`** (`docker restart ap-app ap-worker`). The **app** resolves webhook→version; the **worker** executes steps and caches the flow version. Restarting only one leaves the stale template in play.

## Verify a run used your edit + its output

```bash
# 1) Which version actually ran
docker exec ap-db psql -U postgres -d activepieces -tAc \
  "SELECT \"flowVersionId\", status FROM flow_run WHERE \"flowId\"='<id>' ORDER BY \"startTime\" DESC LIMIT 1"
# If this != your edited <vid>, trigger_source/publishedVersionId are misaligned.

# 2) The run's REAL output (email recipients, etc.) — stored compressed in `file`
FID=$(... SELECT "logsFileId" FROM flow_run WHERE id='<runId>')
# SELECT encode(data,'base64') FROM file WHERE id='<FID>'  ->  base64 -d  ->  zstd -d > run.json
# run.json: executionState.steps.*.output ; email step output has "accepted": [email]
```

## Timing + query pitfalls

- **El nombre del flow NO está en `flow.name`** — se lee de `flow_version."displayName"` (el que usamos para "probar" que corre un nombre, verificar por la fila de `flow_version` con el `flowId`). En SQL: `SELECT "displayName" FROM flow_version WHERE "flowId"='<id>' ORDER BY created DESC LIMIT 1`.
- **Patrón de prueba de leads (03/09):** nunca mandar un lead real del cliente a un flow que aún se está verificando. Usar el marcador **"PRUEBA INTERNA NO CLIENTE"** en el cuerpo/payload de prueba → verificar el run que se disparó (que llegó al destino esperado, p. ej. el email salió y el `accepted` contiene el correo de prueba) → **borrar el run de prueba** con `DELETE FROM flow_run WHERE id='<runId>'` para no contaminar métricas reales.
- AP returns `200 {}` on the webhook immediately but creates the flow run **~20–30 s later** (sandbox install/build). Do NOT conclude "no run" after 10–15 s.
- `flow_run.startTime` is **UTC**; comparing against a literal timestamp string is a timezone trap. Use `WHERE "startTime" > now() - interval '10 minutes'`.
- Don't pipe a big JSON query through your **local shell** (quoting breaks) — write the query/script to a file and `scp`+run on the host, or pass SQL as a psql **argument** (stdin `-i` was unreliable for large output).

## notifyActivePieces "fetch failed" (webhook server → AP)

The webhook container must reach the AP webhook URL (`http://<AP_IP>:8088/api/v1/webhooks/<flowId>`). Reproduce from inside the container:
`docker exec <webhook> node -e 'fetch(process.env.ACTIVEPIECES_WEBHOOK_URL,...).then(r=>console.log(r.status))'`.
Harden `notifyActivePieces` in `webhook-server.js` / `webhook-server-paradise.js`: raise the per-attempt timeout (8s→15s) and add N retries with backoff (1s,2s,3s). Validate with `node --check`, then restart the webhook container.

## References

- `references/edit-and-verify-recipes.md` — concrete SQL/commands for the whole flow, Google-Maps profile-link extraction, and the exact prod layout (Golden 3oGBil1naEsVErmbBz6KY, Paradise jIrDwFPupZwZJ9Z1y97YT; containers webhook-gateway/webhook-paradise; AP webhook `http://<AP_IP>:8088/api/v1/webhooks/<flowId>`).
