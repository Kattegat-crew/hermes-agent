# Despliegue CAPI + Pixel Meta — Golden (07/09/2026)

## Resumen
Se integró a goldengame.com.co el pixel de Meta (browser) y la Conversions API (server-side), para que la campaña "Golden Septiembre. Amor y Amistad" (Bingo Millonario) mida el funnel completo: ads → web → Lead.

## Datos clave
- **Pixel ID:** `989823497477559` (dataset "Golden Game Web")
- **Ad Account:** `act_1581421999562187` (Golden Game)
- **Server CAPI:** contenedor `webhook-gateway` en .222, `/opt/docker/webhook-gateway/webhook-server.js`
- **Dominio:** `https://goldengame.com.co`
- **Región Events Manager:** Europe (server Contabo en Francia — verificado con `curl -s ipinfo.io`)

## Cambios aplicados

### 1) webhook-server.js (.env + código)
- Env vars: `META_PIXEL_ID` + `META_CAPI_ACCESS_TOKEN`.
- `import crypto from 'crypto'`.
- Helper `sha256()` y `sendCapiEvent()` → POST a `https://graph.facebook.com/v21.0/{PIXEL_ID}/events`.
- Disparo en `/webhook/golden-vip-signup` tras el INSERT, fire-and-forget.

### 2) index.html (frontend)
- Snippet base en `<head>` (script del pixel).
- `<noscript>` fallback en `<body>` (NUNCA en head — rompe Vite/parse5).
- Canonical + OG + Twitter URLs corregidos de `goldengameweb.netlify.app` → `goldengame.com.co`.

### 3) nginx.conf (CSP)
- `script-src` += `https://connect.facebook.net`
- `connect-src` += `https://connect.facebook.net` + `https://graph.facebook.com`

### 4) src/App.jsx + src/utils/metaPixel.js
- `RouteWatcher` dispara `PageView` + `ViewContent` en cada navegación SPA.
- Helper seguro (no-op si fbq no cargó).

## Verificación end-to-end
```
[WEBHOOK RESP] {"success":true,"leadId":89}
[BONO] Lead inserted: id=89
[CAPI] Lead enviado. events_received=1
```
Flujo confirmado: form → Postgres → Meta.

## Stape — por qué NO se usa
Meta ofrece un "Conversions API Gateway" que usa internamente **Stape** (servicio de pago con prueba de 7 días). Los avisos en Events Manager ("Claim account", "Conversions API Gateway", "Automatic Meta pixel connection") llevan a crear cuenta en Stape. **NO es necesario**: nuestra CAPI envía directo al Graph API con el access token, sin intermediarios y sin costo. Ignorar/borrar esas conexiones.

## Pitfalls encontrados (importantes)
1. `docker restart` NO re-lee `env_file:` del docker-compose → usar `docker compose up -d --no-deps <service>` para recrear.
2. `<noscript>` en `<head>` → `npm run build` falla (parse5 `disallowed-content-in-noscript-in-head`).
3. CSP en nginx bloquea el pixel si no se whitelistea connect.facebook.net.
4. Token CAPI puede dar `(#100) Missing Permission` en GET pero funcionar en POST (scope solo de escritura).
5. Canonical/OG apuntando a dominio viejo (netlify.app) ensucia atribución y SEO → corregir.
6. "0 eventos / 28 días" en dashboard = normal hasta que haya tráfico real (pixel recién instalado).
