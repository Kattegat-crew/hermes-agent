---
name: google-oauth-reauth
description: DEPRECATED — Use activepieces-google-access instead. Token local revocado.
version: 1.1.0
author: Ragnar
status: deprecated
deprecated_reason: "Token local google_token.json revocado. Todo acceso a Google ahora via ActivePieces."
replacement: activepieces-google-access
metadata:
  hermes:
    tags: [google, oauth, calendar, gmail, token, reauth, pkce, scopes, deprecated]
---

# ⚠️ DEPRECATED — Google OAuth Re-Auth

**Esta skill está OBSOLETA.** El token local `google_token.json` está revocado.

## Usar en su lugar: `activepieces-google-access`

TODO el acceso a Google ahora se hace vía ActivePieces:
- Secrets materializados en `/opt/data/secrets/{owner}-{service}.json`
- Refrescar access_token con `google.oauth2.credentials.Credentials`
- Llamar a la API de Google directamente

Ver skill `activepieces-google-access` para el procedimiento completo.