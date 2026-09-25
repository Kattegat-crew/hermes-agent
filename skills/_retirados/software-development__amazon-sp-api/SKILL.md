---
name: amazon-sp-api
description: "Usar al conectar Seller Central a Amazon SP-API."
---

# Amazon SP-API

## Cuándo usar
- Conectar una cuenta Seller Central (US / AU / UK / DE...) a SP-API
- Automatizar: sync de inventario, lectura de órdenes, repricing, reportes de ventas, alta de listings
- Cuando pregunten "¿Amazon Seller Central tiene API?" — responder que SÍ, SP-API (sucesor del retirado MWS)

## Flujo vigente (2026) — simplificado, SIN AWS IAM
El nuevo **Solution Provider Portal** (`https://solutionproviderportal.amazon.com`) ya NO requiere cuenta AWS ni rol IAM. Las credenciales se generan desde el portal. Los docs viejos que piden IAM role + LWA security profile están **obsoletos**.

1. **Developer Profile (privado)** en Seller Central → Apps and Services → Develop Apps
   - Data Access: **"Private Developer: I build application(s) that integrate my own company with Amazon Services APIs"**
   - Seleccionar roles, use cases, security controls → aceptar políticas (SPP Agreement, AUP, DPP) → Register
   - Esperar aprobación por email — si piden más info, responder en **máx. 5 días** o el caso se cierra
2. **App sandbox** en SPP: Add new app client → API type: SP-API → Application type: Sandbox
   - LWA credentials → View sandbox credentials → client ID (`amzn1.application-oa2-client.*`) + client secret (`amzn1.oa2-cs.v1.*`)
   - Action → Create Token → refresh token (`Atzr|*`)
3. **App producción** en SPP: Add new app client → SP-API → Production → roles aprobados → Save (draft)
   - LWA credentials → View production credentials
   - Action → **Authorize app** (self-authorization) → genera refresh token de producción
4. **Guardar credenciales** en `/opt/data/.env` como `AMAZON_SPAPI_*`

## Token exchange y endpoints
```bash
# Access token (válido 1 hora)
curl -X POST 'https://api.amazon.com/auth/o2/token' \
  -H 'Content-Type: application/x-www-form-urlencoded;charset=UTF-8' \
  --data-urlencode 'client_id=...' --data-urlencode 'client_secret=...' \
  --data-urlencode 'grant_type=refresh_token' --data-urlencode 'refresh_token=...'
# → {"access_token":"Atza|...","token_type":"bearer","expires_in":3600}

# Smoke test: sellers/v1
curl -X GET 'https://sellingpartnerapi-eu.amazon.com/sellers/v1/marketplaceParticipations' \
  -H 'x-amz-access-token: ...' -H 'Content-Type: application/json'
```

| Región | Producción | Sandbox |
|---|---|---|
| North America | `sellingpartnerapi-na.amazon.com` | `sandbox.sellingpartnerapi-na.amazon.com` |
| **Europa (NO incluye AU)** | `sellingpartnerapi-eu.amazon.com` | `sandbox.sellingpartnerapi-eu.amazon.com` |
| **Far East (incluye AU)** | `sellingpartnerapi-fe.amazon.com` | `sandbox.sellingpartnerapi-fe.amazon.com` |

Marketplace IDs: AU `A39IBJ37TRP1C6` · US `ATVPDKIKX0DER`.

**⚠️ AUSTRALIA = FAR EAST (fe), NO Europa — VERIFICADO 18/08/2026**
Doc oficial (sp-api-endpoints): *Far East (Singapore, Australia, and Amazon Japan stores)*. Un error previo de esta skill decía que AU operaba en Europa; es FALSO — el token AU da 403 contra `sellingpartnerapi-eu` y funciona contra `sellingpartnerapi-fe` (probado en vivo con cuenta Digital Expressions). El sandbox AU es `sandbox.sellingpartnerapi-fe.amazon.com`.

## Roles (mínimo inicial, unrestricted)
Sellers (v1, smoke test) · Orders (v0) · Inventory (v1) · Product Pricing (v0) · Reports (v0) · Listings Items (2021-08-01). Los roles restricted (PII de clientes) requieren Restricted Data Token + revisión de seguridad adicional — agregar después si hace falta.

## Consultar documentación oficial (técnica que funciona)
- Índice completo: `curl -sL https://developer-docs.amazon.com/sp-api/llms.txt`
- Páginas en markdown: `curl -sL "https://developer-docs.amazon.com/sp-api/docs/<slug>.md"` — las URLs `.html` dan 404; la variante `.md` funciona y es limpia.
- Slugs útiles: `onboarding-step-1-prepare-for-registration`, `register-as-a-private-developer`, `self-authorization`, `onboarding-step-4-register-your-first-sandbox-application`, `onboarding-step-5-make-your-first-call-to-the-sp-api-sandbox`, `onboarding-step-7-register-your-first-production-application`.

## Soporte existente
- Paquete de setup: `/opt/data/amazon-spapi-setup/` — `spapi_token.py` (helper: `--test` y `--endpoint`, `--sandbox` para credenciales sandbox, lee `AMAZON_SPAPI_*` o `AMAZON_SPAPI_SANDBOX_*` de `/opt/data/.env`), `GUIA-ONBOARDING-SP-API.md` / `.docx`
- `listing_fields.py` — descarga el esquema vigente del product type (`--product-type PET_PRODUCTS --full`), genera plantilla de payload (`--payload`) — REQUIERE credenciales de producción
- `MAPA-LISTING-PERFECTO.md` / `.docx` — mapa completo de campos por grupo con constraints y tips SEO
- Caso de referencia: `references/digital-expressions-onboarding.md`

## Pitfalls
- NO seguir el flujo viejo con rol IAM + LWA security profile separado — el SPP nuevo genera las credenciales internamente.
- Access token dura **1 hora**; siempre usar refresh token para regenerar. El refresh token es de larga duración y regenerarlo NO invalida el anterior.
- Para apps privadas la autorización es automática con "Authorize app" en SPP — no hay redirect manual.
- `web_extract` puede no estar configurado (Firecrawl) — para docs SP-API usar curl a las páginas `.md`.
- **Australia pertenece a la región Far East (fe)** — `sellingpartnerapi-fe.amazon.com`, sandbox `sandbox.sellingpartnerapi-fe.amazon.com`. Verificado 18/08/2026 en vivo: token AU + eu = 403; token AU + fe = OK. Marketplace AU `A39IBJ37TRP1C6`.
- Requisito de cuenta: plan **Professional** de Seller Central (la cuenta individual no califica para API).

## Pitfall CRÍTICO: campo orgID / Open Banking (trampa del formulario)
El formulario tiene un campo **obligatorio** "orgID para Open Banking". Si no eres TPP regulado (UE/UK), **NO se llena**: hay que **DESMARCAR las funciones Open Banking** — AISP (información de cuentas) y PISP (iniciación de pagos) — en el paso de selección de funciones. El error de validación lo dice explícito: "debes cancelar la selección de estas funciones para seguir adelante". Escribir "No aplica" NO pasa la validación; escribir un orgID falso es peor (lo validan). Lección de 18/08/2026.

## Sandbox vs Producción (límites reales)
- El sandbox devuelve **SOLO data simulada estática** (`BestSellerStore`, marketplace US de mentira `ATVPDKIKX0DER`). NO permite escanear la cuenta real (tiendas, perfil, inventario, listings).
- Muchos endpoints sandbox rechazan el marketplace AU con `Unauthorized: marketplaces not valid for region` (p.ej. `/definitions/2020-09-01/...`). El de sellers/v1 sí responde con el mock US.
- **Datos reales requieren app de Producción + refresh token de producción** — avisar al usuario antes de prometer un "escaneo de la cuenta" con sandbox.

## Listings por API (campo por campo)
Los requisitos de campos son **dinámicos**: Amazon los sirve por product type vía **Product Type Definitions API**:
`GET /definitions/2020-09-01/productTypes/{productType}?marketplaceIds=...&requirements=LISTING` → JSON schema con `properties` + `required` + constraints (maxLength, maxItems, pattern).

Crear/actualizar con **Listings Items API**:
- `PUT /listings/2021-08-01/items/{sellerId}/{sku}` — reemplaza TODO el contenido; campos omitidos se BORRAN (peligro con put repetidos)
- `PATCH` solo para `fulfillment_availability` (stock) y `purchasable_offer` (precio)
- `?preview=true` valida SIN publicar — **SIEMPRE preview antes del PUT real**
- Respuesta: array `issues` — códigos: `MissingAttribute`, `InvalidAttributeValue`, `InvalidGtin`, `InvalidImage`, `InvalidProductType`

Grupos de campos PET_PRODUCTS: identidad (item_name ≤200, brand, item_type_keyword), identificadores (gtin 8-14 dígitos), contenido SEO (5 bullet_point ≤500 c/u, product_description ≤2000, main_product_image_locator blanca 1000px+, search_terms backend), atributos físicos (item_weight/item_dimensions — CRÍTICOS para FBA tier y fees), precio (purchasable_offer.list_price en AUD con currency), cumplimiento (fulfillment_availability.fulfillment_channel_code=DEFAULT para FBA + quantity; FBM: merchant_shipping_group_name).

## App de Producción: activación y diagnóstico (verificado 18/08/2026)
- **Entidades admitidas** → `Vendedores` (app privada de seller propio; Certificador/Proveedores/Carga/Envíos = otros programas).
- **TDR/RDT "¿delegar IIP?"** → **No** (app privada).
- **OAuth Login/Redirect URI = solo apps públicas.** Si el form los pide, la app está como pública; las apps privadas se auto-autorizan en estado **Borrador** (docs oficiales). Buscar toggle User Access → Privada; si no existe, URI https propia (localhost NO).
- **Sin roles operativos seleccionados → 403 en TODO** excepto operaciones **grantless** (`GET /sellers/v1/marketplaceParticipations` funciona sin roles — sonda de diagnóstico ideal; `/sellers/v1` NO es grantless).
- **Tokens por región**: cuenta global = un refresh token POR REGIÓN (AU→eu, NA→na; token NA @ eu → 403, verificado). Re-autorizar CADA región después de cambiar roles (el token congela los roles al generarse).
- **Roles en el form SPP (español → API)**: Listing de producto (= Listings+PTD+A+), Precios (= Pricing), Seguimiento de pedidos e inventario (= Orders+Inventory), Logística de Amazon (= FBA), Información sobre el colaborador comercial (= Sellers). Si limita a 8 de 10, dejar fuera Análisis de marcas y AWD.
- **App Integrations API** (notificaciones Seller Central) es OPCIONAL — no bloquea la activación de la app. El help/portal del SPP está detrás de login (no se puede curl).
- Detalle + diagnóstico: `references/production-app-activation.md` · probe: `scripts/test_region_tokens.py`.

## Atestación de seguridad (Security Controls del formulario)
Es una **atestación legal** — antes de dejar que el usuario marque "Sí" a todo, **auditar el estado real del VPS** (ufw/iptables, IDS/IPS, antivirus, plan IR, política de contraseñas, secrets en repos) y armar plan por fases para cerrar brechas. Nunca inventar cumplimiento. Auditoría de referencia 18/08/2026: firewalls y plan IR NO existían; Postgres/Redis/Qdrant expuestos en 0.0.0.0.
