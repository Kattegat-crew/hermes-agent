---
name: meta-ads-operations
description: "Run Meta Ads: campaigns, geo, insights, pixel via Composio."
version: 1.0.0
---

# Meta Ads Operations (Composio metaads toolkit + pixel)

Clase de trabajo: operar campañas de Meta Ads (Facebook/Instagram) desde el agente — crear campañas/ad sets/anuncios, leer métricas, geolocalizar, y conectar el funnel con el **pixel de Meta**. Todo se hace vía el toolkit `metaads` de **Composio** (managed OAuth, sin crear app de Meta).

## 1. Conexión (por cliente: 1 conexión = 1 Ad Account)

```bash
export PATH="/opt/data/home/.composio:$PATH"   # binario ejecutable real (el de /opt/data/composio-linux-x64/ da Permission denied)
composio whoami                                   # email + org
composio connections list | jq '.metaads[]'       # status + word_id + alias por cliente
composio link metaads --no-browser --no-wait      # → redirect_url, el usuario autoriza
composio connections list                          # confirmar status ACTIVE
```

- **Managed auth** (default): no creas app, Composio maneja el OAuth. **Cada cliente/business debe conectar su propio Ad Account** con `composio link metaads`.
- ⚠️ **Las conexiones EXPIRAN.** Si status = `EXPIRED`, re-vincular con `composio link metaads` y que el usuario complete la autorización. Una sesión EXPIRED NUNCA ejecuta tools; y el link expira si no se autoriza a tiempo.
- Verificadas 07/09: Golden = `metaads_tactic-vison` (`act_1581421999562187`), Lucky/Paradise = `metaads_moly-ponent` (`act_1525564931963110`).

## 2. Tools (lectura + creación)

- **Lectura**: `METAADS_GET_AD_ACCOUNTS`, `METAADS_GET_INSIGHTS`, `METAADS_GET_OBJECT`, `METAADS_READ_ADSETS`, `METAADS_LIST_TARGETING_SEARCH`, `METAADS_GET_PAGE_ACCOUNTS`, `METAADS_LIST_ADS`, `METAADS_LIST_AD_CREATIVES`.
- **Creación**: `METAADS_CREATE_CAMPAIGN`, `METAADS_CREATE_AD_SET`, `METAADS_CREATE_AD`, `METAADS_CREATE_AD_CREATIVE`, `METAADS_UPDATE_CAMPAIGN`.
- Listar herramientas disponibles de verdad con `composio execute <SLUG> --get-schema` (devuelve el inputSchema) o `ls /opt/data/home/.composio/tool_definitions/ | grep -i metaad`.

## 3. Lecturas de diagnóstico

- **Ad accounts accesibles**: `METAADS_GET_AD_ACCOUNTS -d '{}'` → `data.data[]` con `id`/`account_id`/`name`.
- **Métricas**: `METAADS_GET_INSIGHTS -d '{"object_id":"act_...","level":"account|campaign|adset|ad","time_range":{"since":"2026-06-01","until":"2026-09-07"}}'`. ⚠️ `date_preset` solo acepta enum cerrado (`today|yesterday|last_7d|last_30d|this_month|last_month|this_quarter`) — para rangos arbitrarios usar `time_range`. El `level` debe coincidir con el tipo del `object_id` (campaign→campaña id, act_→account).
- **Ad sets por cuenta**: `METAADS_READ_ADSETS -d '{"ad_account_id":"act_...","fields":["name","id","status","effective_status","campaign_id"]}'`.

## 4. 🔑 Geomarketing: leer geolocalización de un ad set

**GOTCHA central**: `METAADS_READ_ADSETS` NO devuelve el `targeting` (geo) aunque lo pidas en `fields` — los ad sets vienen con `targeting: null`. Para leer/auditar el geo de un ad set:

```bash
composio execute METAADS_GET_OBJECT --account <word_id> -d '{"object_id":"<ID_adset>","fields":["name","targeting"]}'
# → data.targeting.geo_locations.cities[].name  (municipios)
```

Se hace **por adset** (loop sobre los IDs). También trae `age_min`/`age_max` y `flexible_spec` (intereses). Útil para auditar si un ad set "por sede" realmente está geo-localizado o solo segmenta por interés.

Pitfalls de parámetros:
- `fields` en `READ_ADSETS` debe ser un **enum válido** (p.ej. NO existe `location` → 'Instance does not match any of ...'; existe `targeting`). 
- En `GET_OBJECT`, `fields` DEBE ser **array** (no string separado por comas) y `object_id` sin path.

## 5. Crear campaña (flujo)

`CREATE_CAMPAIGN` → `CREATE_AD_SET` (link campaña, budget/targeting) → `CREATE_AD_CREATIVE` (assets) → `CREATE_AD`. Recomendado: crear **todo en pausado** (estado no-delivering) y presentar el pack (nombre, geo, presupuesto, pieza) al Admin antes de activar con `UPDATE_CAMPAIGN`. Los anuncios consumen presupuesto real — nunca activar sin OK.

Según la estrategia del equipo (07/09): **una campaña general + ad sets separados por sede** (geo por municipio). El ad set "general" lleva las ubicaciones de las sedes (radio ~5-8 km por municipio, no 17 km) para no desperdiciar; los ad sets "por sede" usan radio quirúrgico (~5 km). Presupuesto típico: 30% general / 70% ad sets de sede.

Pitfalls de creación (documentados por composio):
- `CREATE_AD_SET` puede rechazar edades automáticas (error 1870189 / code 100 subcode 2490487 → simplificar targeting o quitar campos de expansión).
- code 100 subcode 1815857 → ajustar bid/budget vía `UPDATE_CAMPAIGN`.
- subcode 1815430 en setups de conversión → simplificar campos.

## 6. Pixel de Meta (funnel — ejecutado y verificado 07/09 para Golden)

✅ Implementado end-to-end para goldengame.com.co (Vite/React SPA, repo `ggl-repo`, deploy Docker/Coolify :9001). El **pixel se crea en Meta Events Manager** (NO hay tool composio para crear pixels). Es **1 pixel por dominio/cliente** (la segmentación por sede va en el ad set, no en el pixel).

### 6a. Browser pixel en SPA (React Router / Vite)
- Snippet base `fbevents.js` + `fbq('init', PIXEL_ID)` en el `<head>` del `index.html` (después de `</title>`).
- ⚠️ **`<noscript>` NO va en `<head>`**: Vite/parse5 falla al build con `[vite:build-html] disallowed-content-in-noscript-in-head`. Mover el `<noscript><img .../></noscript>` a **justo después de `<body>`**.
- Como la SPA no recarga, el `PageView` base solo dispara 1 vez → **disparar por navegación cliente** en el watcher de ruta (helper `metaPixel.js`: `trackPageView(pathname)` + `trackViewContent(pathname)` en el `useEffect` del `RouteWatcher`, que ya existe y ve `location.pathname`) y **por acción** (`trackLead()` en el onSubmit, SOLO en éxito).
- Envolver en helper seguro: `if (typeof window !== 'undefined' && window.fbq) ...` (no rompe si adblock lo bloqueó).
- Verificar con **navegador real** (`window.fbq` definido + `_fbq` queue con eventos) + **Meta Events Manager → Test Events**.
- **Auditar el dominio**: si canonical/OG apuntan a URL vieja (ej. `goldengameweb.netlify.app`) en vez del dominio servido real (`goldengame.com.co`), se ensucia la atribución — corregir en el mismo deploy.

### 6b. Conversions API (CAPI) server-side — fuente de verdad del Lead
En el webhook server (Express, `webhook-gateway`), disparar **`Lead` al Graph API** después del INSERT, fire-and-forget (si falla, el lead ya está en Postgres). Un solo POST:
```
POST https://graph.facebook.com/v21.0/{PIXEL_ID}/events
access_token + data[].event_name/event_time/event_id/action_source/user_data/custom_data
```
- **user_data HASHEADO** (SHA-256, lowercase): `em`=email, `ph`=teléfono (solo dígitos), `fn`/`ln`=nombre/apellidos, `cn`=cédula.
- `action_source: 'website'`, Cursos con `event_id` = uuid. Acepta `custom_data.value`+`currency`.
- Env vars en el contenedor: `META_PIXEL_ID`, `META_CAPI_ACCESS_TOKEN` (secreto — en `.env`, nunca en repo/chat).
- Conexión de ejemplo (validada): `sha256(s)` helper + `fetch(graph.facebook.com/v21.0/{PIXEL_ID}/events, {access_token})`.

### 6c. GOTCHAS de verificación y mentalidad (críticos)
- **El CAPI token es correcto aunque `GET /{pixel}` devuelva "(#100) Missing Permission"**. Los tokens de CAPI van scoped a ENVIAR, no a LEER metadata del pixel. Para validar, haz un POST (no un GET).
- **🚫 TRAMPA DE STAPE**: Meta Events Manager te sugiere "Conversions API Gateway" / "Activate automatic Meta pixel connection" / "Claim your Stape account". **Eso es un servicio de pago de terceros (Stape)** y te lleva a un login/registro. **NO lo hagas** — la CAPI directa al Graph API es estándar y gratis. Estos avisos del asistente son opcionales.
- **"0 eventos" en el dashboard NO es un fallo.** Cuenta eventos de USUARIOS REALES en los últimos 28 días; no cuenta las llamadas de prueba de la API (que sí responden `events_received:1`). Si el pixel se acaba de instalar y no hay tráfico real, marca 0 — es normal. Los `events_received:1` de pruebas no llenan esa vista. Los eventos se llenan cuando llega tráfico real.
- **`events_received: 1` = Meta aceptó el evento** (API del servidor), es la señal de éxito server-side.

### 6d. Deploy del frontend (específico del entorno Golden, aplicable a Coolify)
- **`docker restart` NO recarga variables del `env_file`**. `env_file` inyecta env al CREAR el contenedor. Para aplicar nuevas env vars: `docker compose up -d` (recrea). Este mismo principio aplica a cualquier `.env`/compose.
- El contenedor Coolify del sitio es una **imagen nginx pre-buildada** (no volumen). El source está en el host (ej. `/opt/app-golden`). Flujo: sincronizar archivos → `docker build -t <name>:latest .` → `docker stop && docker rm` del contenedor viejo → `docker run -d --name ... -p ... golden-...:latest`.
- **CSP de nginx bloquea el pixel** si `script-src 'self'` — hay que añadir `'unsafe-inline' https://connect.facebook.net` a `script-src` y `https://connect.facebook.net https://graph.facebook.com` a `connect-src`. Sin esto, el snippet carga pero la CSP lo bloquea.
- Verificar SIEMPRE que el index servido (curl al dominio público) tiene el pixel y el canonical — NO confiar solo en el build local.

## Referencias

- `references/session-2026-09-07-meta-ads-golden.md` — diagnóstico de campañas Golden/Paradise (inversión, ad sets, geo faltante), conexiones expiradas y re-vinculación, plan del pixel Golden.
