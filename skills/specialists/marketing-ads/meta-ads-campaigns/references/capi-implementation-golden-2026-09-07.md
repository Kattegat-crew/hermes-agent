# CAPI Implementation — Golden Game (07/09/2026)

## Pixel y CAPI configurados
- **Pixel ID**: `989823497477559`
- **Región Events Manager**: Europa (server prod .222 = Contabo Francia/Lauterbourg)
- **Token CAPI**: system user token from Events Manager → Settings → Conversions API
- **Secrets file**: `/opt/data/secrets/golden_meta_capi.env` (dev, permissions 600)
- **Prod .env**: `/opt/docker/webhook-gateway/.env` (contenedor webhook-gateway)

## Server-side CAPI integrado en
- **Archivo**: `/opt/docker/webhook-gateway/webhook-server.js` (producción .222)
- **Handler**: `/webhook/golden-vip-signup` → INSERT PostgreSQL → `sendCapiEvent('Lead')` fire-and-forget
- **Env vars**: `META_PIXEL_ID`, `META_CAPI_ACCESS_TOKEN` (via env_file en docker-compose.yml)
- **Contenedor**: `webhook-gateway` (node:22-alpine, Coolify, puerto 3099)
- **Backup**: `.bak-capi-20260907-150758` en el host prod

## Test result
```
Pixel: 989823497477559
EventID: capi-test-1788812101310
RESP: {"events_received":1,"messages":[],"fbtrace_id":"Aee_LzWrmcx1qop_WArSZqw"}
OK - Lead enviado a Events Manager
```

## Lead data sent (CAPI)
- `em`: SHA-256 of email (lowercase, trimmed)
- `ph`: SHA-256 of phone (digits only, trimmed)
- `fn`: SHA-256 of first name (from lead.name.split(' ')[0])
- `cn`: SHA-256 of cédula
- `content_name`: 'Bono VIP 20K'
- `value`: lead.bonus_amount, `currency`: 'COP'

## Pending: browser pixel (frontend SPA)
- Snippet base en `<head>` de index.html (fbevents.js + fbq init + PageView)
- Helper `metaPixel.js` para eventos SPA
- `RouteWatcher` en App.jsx → PageView + ViewContent por ruta
- `Bono.jsx` → Lead event tras submit OK (para dedup con CAPI)
- Fix canonical/OG: goldengameweb.netlify.app → goldengame.com.co
- Repo: `/opt/data/ggl-repo` (Vite/React SPA)

## Notas de deploy
- `docker restart` NO re-read env_file → usar `docker compose up -d --no-deps webhook-gateway`
- Verificar env vars: `docker exec webhook-gateway node -e 'require("dotenv/config"); console.log(process.env.META_PIXEL_ID)'`
- `node:22-alpine` no tiene curl → usar node para tests HTTP
- `diff` repo local vs prod: archivos divergieron (prod tiene templatesRouter + KNOWLEDGE imports). Editar siempre el prod, no el repo.