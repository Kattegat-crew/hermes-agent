---
name: oauth-connection-health-audit
description: Audit expired OAuth refresh tokens in ActivePieces; re-auth only the dead.
author: Ragnar
version: "2.0"
created: 2026-09-06
updated: 2026-09-12
category: devops
metadata:
  hermes:
    tags: [oauth, token, activepieces, google, refresh, diagnostico]
    related_skills: [activepieces-connection-api, activepieces-google-access, oauth-connection-gateway]
---

# OAuth Connection Health Audit — ActivePieces tokens

## When to Use

- Un servicio (calendar/gmail/drive) falla por auth. Se quiere saber QUÉ conexión de AP falla.
- Revisar qué tokens de AP ya caducaron.
- Antes de re-autenticar: confirmar cuáles tokens están realmente muertos.

## 🔑 Regla #1: NO existe token local

El token local `google_token.json` está REVOCADO. **NO re-autenticar token local.**
Todo acceso a Google es vía ActivePieces.

## Fuentes de credenciales (en orden)

1. **Secrets materializados:** `/opt/data/secrets/{owner}-{service}.json` → `{refresh_token, client_id, client_secret}`
2. **AP DB directa:** descifrar `app_connection.value` (AES-256-CBC, `AP_ENCRYPTION_KEY`)

## Auditoría: probar refresh contra Google

POST `oauth2.googleapis.com/token` con `grant_type=refresh_token&client_id&client_secret&refresh_token`:
- `OK` + scopes = token VIVO.
- `invalid_grant` = expirado/revocado → reconnect en AP UI.
- `invalid_client` = credenciales rotas.

## Re-auth: reconnect en AP UI

Si un token está muerto: AP UI → Settings → Connections → *Reconnect* (2 min/cuenta).
O re-materializar secrets con el script `materialize_v4.py`.

## Pitfall: SQL a AP DB

Columnas con mayúsculas: `"displayName"`, `"pieceName"`. Usar pipe por stdin, no comillas anidadas.

## Scripts

- `scripts/verify_ap_refresh_tokens.py` — prueba refresh de TODAS las conexiones Google de AP.