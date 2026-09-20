---
name: activepieces-google-access
description: "Use when accessing Google services via ActivePieces."
version: 1.0.0
author: Ragnar
created: 2026-09-11
metadata:
  hermes:
    tags: [google, gmail, drive, calendar, sheets, activepieces, composio, oauth, integraciones]
    related_skills: [activepieces-selfhost-ops, activepieces-connection-api, gdrive-via-activepieces, oauth-connection-health-audit]
---

# ActivePieces Google Access — Protocolo Canónico

## When to Use

- Cualquier tarea que necesite leer/escribir Gmail, Drive, Calendar, o Sheets.
- Configurar acceso a Google para un agente nuevo.
- Diagnosticar por qué un acceso a Google falla.

## Regla Fundamental

> **TODO el acceso a Google se hace EXCLUSIVAMENTE vía ActivePieces.**
> El token local (`google_token.json`) está REVOCADO y NO se usa.
> Composio complementa para redes sociales y Meta Ads.

## Arquitectura de credenciales

```
Agente Hermes
  ├── ncl_google_mcp.py (MCP server custom)
  │     ├── lee connections-map.json (metadata)
  │     ├── lee secrets/{slug}-{svc}.json (credenciales materializadas)
  │     └── llama Google APIs directo con refresh_token
  │
  └── ActivePieces (:8088)
        ├── Conexiones OAuth en Postgres (refresh automático)
        ├── MCP nativo (requiere OAuth propio — pendiente)
        └── REST API /api/v1/ (JWT con AP_JWT_SECRET)
```

## Fuentes de credenciales (orden de preferencia)

### 1. Secrets materializados (primaria)

Ruta: `/opt/data/secrets/{slug}-{svc}.json`

```json
{"connection":"jonathan-gmail","account":"jonathaun124@gmail.com",
 "refresh_token":"1//0...","client_id":"288239405432-...",
 "client_secret":"GOCSPX...","scope":"..."}
```

**Si no existen:** `verify_connection.py <slug>-<svc>` (lee AP DB, descifra, escribe chmod 600).

### 2. Connections-map.json (metadata)

Ruta: `/opt/data/connections-map.json` — campos: `owner`, `service`, `status`, `ap_project_id`. NO contiene credenciales.

### 3. ActivePieces DB (raw)

Tabla `app_connection`, columna `value` (AES-256-CBC HEX). Key: `AP_ENCRYPTION_KEY`. Lib: `cryptography`.

## Código de ejemplo

```python
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import google.auth.transport.requests

d = json.loads(open('/opt/data/secrets/jonathan-gmail.json').read())
creds = Credentials(token=None, refresh_token=d['refresh_token'],
    client_id=d['client_id'], client_secret=d['client_secret'],
    token_uri='https://oauth2.googleapis.com/token',
    scopes=d['scope'].split(','))
creds.refresh(google.auth.transport.requests.Request())

# Gmail
svc = build('gmail', 'v1', credentials=creds, cache_discovery=False)
# Drive
svc = build('drive', 'v3', credentials=creds, cache_discovery=False)
# Calendar
svc = build('calendar', 'v3', credentials=creds, cache_discovery=False)
# Sheets
svc = build('sheets', 'v4', credentials=creds, cache_discovery=False)
```

## Configurar agente nuevo

1. Verificar conexión ACTIVE en AP (Settings → Connections).
2. `verify_connection.py <slug>-<svc>` para materializar secret.
3. Registrar MCP:
   ```bash
   hermes config set mcp_servers.ncl_google.command python3 --force
   hermes config set mcp_servers.ncl_google.args '["/opt/data/scripts/ncl_google_mcp.py","--profile","<perfil>"]' --force
   ```
4. Reiniciar gateway: cron one-shot `no_agent` (NUNCA en propio turno).
5. Verificar handshake MCP.

## Conexiones activas

| Owner | Gmail | Drive | Calendar | Sheets |
|-------|-------|-------|----------|--------|
| jonathan | ✅ | ✅ | ✅ | — |
| neuralcrew | ✅ | ✅ | ✅ | — |
| golden | ✅ | ✅ | ✅ | ✅ |
| lucky | ✅ | ✅ | ✅ | — |
| helmer | ✅ | ✅ | ✅ | — |
| jacqueline | ✅ | ✅ | ✅ | — |
| nancy | ✅ | ✅ | ✅ | — |
| chucho | ✅ | ✅ | ✅ | — |

**26 secrets materializados en `/opt/data/secrets/`.**
Re-materializar con `python3 /tmp/materialize_v4.py` si AP rota tokens.

## MCP nativo de AP (pendiente)

Endpoint `/mcp` requiere **MCP OAuth** (no API key ni JWT regular). Tabla `mcp` en DB vacía.
`AP_API_KEY` sirve para REST API (`/api/v1/`), NO para `/mcp`.

## Fallback si AP cae

1. `ssh prod 'docker ps | grep ap-app'`
2. `ssh prod 'cd /root/activepieces && docker compose up -d'`
3. **NUNCA** usar `google_token.json`.

## Pitfalls

- `google_token.json` REVOCADO → `invalid_grant` siempre.
- `googleapiclient` NO thread-safe → descargas secuenciales.
- MCP nativo AP NO acepta API key.

## Referencias

- `activepieces-selfhost-ops` — operación stack AP
- `activepieces-connection-api` — crear conexiones REST
- `gdrive-via-activepieces` — patrón Drive
- `oauth-connection-health-audit` — diagnosticar tokens
