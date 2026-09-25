---
name: amazon-spapi-integration
description: "Use when setting up Amazon SP-API or seller API access."
tags: [amazon, sp-api, seller-central, listings, oauth, fba]
---

# Amazon SP-API Integration

Onboarding, credenciales y operación de la **Selling Partner API** para cuentas vendedor de Amazon (contexto: J&N Digital Expressions LLC / Amazon AU, snuffle mats).

## Cuándo usar
- El usuario quiere conectar una cuenta Seller Central con SP-API (inventario, listings, órdenes, precios, reportes).
- Se está llenando el formulario de registro de desarrollador (Developer Profile) o de app.
- Se necesitan respuestas a los campos del formulario (actividad empresarial, casos de uso, controles de seguridad).
- Hay que obtener/rotar refresh token o hacer llamadas SP-API.

## Hechos clave (flujo 2026 — VERIFICADO contra docs oficiales)
- El nuevo **Solution Provider Portal** (solutionproviderportal.amazon.com) ya **NO requiere cuenta AWS ni rol IAM**. Las credenciales (client ID, client secret, refresh token) se generan desde el portal. El flujo viejo (AWS STS + LWA security profile manual) quedó obsoleto.
- Ruta privada (self-developer): Seller Central → Apps and Services → Develop Apps → Developer Profile → seleccionar **"Private Developer: I build application(s) that integrate my own company"** → esperar aprobación (responder en ≤5 días si piden info).
- App: SPP → **Add new app client** → API type SP-API → Sandbox (para probar) / Production (después de aprobación). Credenciales en **LWA credentials** → refresh token vía **Create Token** (sandbox) o **Authorize app** (producción, self-authorization).
- Token exchange: `POST https://api.amazon.com/auth/o2/token` con `grant_type=refresh_token` + client_id + client_secret + refresh_token → access token válido **1 hora**.
- Regiones: AU pertenece a **Far East** (`sellingpartnerapi-fe.amazon.com`, sandbox `sandbox.sellingpartnerapi-fe.amazon.com`). ⚠️ Verificado 18/08/2026: AU **NO** es Europa (error previo en skills/GUIA); token AU + eu = 403, token AU + fe = OK. Marketplace ID AU: `A39IBJ37TRP1C6`. NA: `sellingpartnerapi-na.amazon.com`, Marketplace `ATVPDKIKX0DER`.
- Para probar sin credenciales reales existe sandbox estático (respuestas mockeadas).

## Pasos
1. Confirmar cuenta Professional del seller (la individual no califica para API).
2. Preparar info: datos empresa, ID, use cases.
3. Developer Profile privado (ver Hechos clave) — roles **unrestricted** primero (Sellers, Orders, Inventory, Product Pricing, Reports, Listings Items); restricted (PII) requieren RDT + revisión de seguridad, agregar después.
4. App sandbox → copiar credenciales → probar con `scripts/spapi_token.py --test`.
5. App producción → Authorize app → refresh token producción → guardar en `/opt/data/.env` como `AMAZON_SPAPI_CLIENT_ID/SECRET/REFRESH_TOKEN/REGION/MARKETPLACE_ID`.

## Respuestas de formulario (patrón que funciona)
- **Actividad empresarial + uso de API:** párrafo único en español, **≤500 caracteres**, coherente con los roles solicitados (Amazon valida coherencia). Ejemplo verificado en `references/onboarding-2026.md`.
- **Casos de uso:** misma regla de 500 caracteres si el campo la pide; listar 4-6 funciones concretas (inventario, listings, órdenes, precios, reportes) + frase de "uso exclusivo interno, sin PII ni datos de terceros".
- **Open Banking orgID — TRAMPA de validación (VERIFICADO 18/08):** el campo es **obligatorio** y NINGÚN texto sirve — "No aplica" falla la validación con `El formato orgID no es válido... debes cancelar la selección de estas funciones`. La solución real es **volver al paso de selección de roles/funciones y DESMARCAR las funciones de Open Banking** (AISP = Proveedor de servicios de información de cuentas, PISP = Proveedor de servicios de iniciación de pagos). Al desmarcarlas, el campo deja de ser obligatorio o desaparece. No inventar un orgID (lo validan).
- **Entidades empresariales admitidas (User Access):** para app privada de propia cuenta, seleccionar **Sellers** (vendedores) — NADA más. Las otras opciones corresponden a otros programas que NO aplican a un private developer: certificadores (validación de cumplimiento/customs), proveedores/vendors (Vendor Central, venta wholesale a Amazon), carga/envíos (freight/carriers de Amazon Global Logistics). Verificado 18/08/2026.
- **TDR / datos restringidos (IIP/PII):** para app privada sin terceros → responder **"No, no voy a delegar el acceso a la IIP a la aplicación de otro desarrollador."** El RDT solo aplica si compartes datos restringidos (PII de clientes) con una app de otro desarrollador.

## Diagnóstico: 403 Unauthorized en producción (app recién creada)
**Síntoma:** el token exchange funciona (access token obtenido OK, `expires_in:3600`) pero **TODOS** los endpoints devuelven `HTTP 403 {"code":"Unauthorized","message":"Access to requested resource is denied."}` — a veces con `details: "The marketplaces you provided are not valid for region."` (no confundir con el error del sandbox; en producción con la app mal configurada da lo mismo).

**Causa (casi siempre):** el refresh token de producción se generó **ANTES de habilitar los roles** en la app. El refresh token "congela" los roles que la app tenía al momento de la autorización; cambiar roles después NO actualiza un token ya emitido.

**⚠️ IMPORTANTE — el estado Borrador NO es el problema:** para apps privadas, el draft es el estado FINAL por diseño. Doc oficial (Authorize Private Applications): *"You can self-authorize your application in draft status because there is no reason to publish a private application."* No existe botón "Publicar/Activar" para apps privadas; se auto-autorizan y funcionan desde borrador. La app NO se puede salir de draft, y no hace falta.

**Si el formulario pide "URI de inicio de sesión de OAuth" + "URI de redirección de OAuth":** eso significa que la app está configurada como **pública** — esos campos son SOLO para apps públicas (redirigen vendedores a tu web durante la autorización). Para app privada: buscar "User Access/Acceso de usuario" y ponerlo en **Privada** (los campos dejan de ser obligatorios). Si el formulario los exige de todos modos, llenar con un dominio https real que el usuario controle (nunca localhost, nunca un dominio inventado).

**Fix (en Solution Provider Portal):**
1. Editar la app de producción → sección "Niveles" → marcar los roles operativos. Mapeo de nombres en la UI española del SPP → rol SP-API:
   - **Listing de producto** = Listings Items + Product Type Definitions (el más importante para subir listings)
   - **Precios** = Product Pricing
   - **Seguimiento de pedidos e inventario** = Orders + Inventory
   - **Información sobre el colaborador comercial** = Sellers (cuenta + rendimiento)
   - **Finanzas y contabilidad** = Finances · **Logística de Amazon** = FBA · **Comunicación con el comprador** = Messaging · **Solicitud de comprador** = Solicitation
   - Los 2 que NO hacen falta: **Análisis de marcas** (Brand Analytics, requiere Brand Registry) y **Almacenamiento y distribución de Amazon** (AWD). Eso deja exactamente 8/10 roles aprobados.
2. Guardar la app (el draft está bien — ver nota arriba).
3. Regenerar el refresh token (**Action → Authorize app** → una por cuenta/región: "Webs de Amazon: Australia" genera el token FE, la sección US/NA genera el token NA) → nuevo `Atzr|...`.
4. Re-probar con el nuevo token. El token viejo no se invalida, pero no lleva los roles nuevos.

**Roles efectivos — endpoints grantless vs con rol (VERIFICADO 18/08/2026):** `GET /sellers/v1/marketplaceParticipations` es **grantless** — responde aunque la app no tenga roles (por eso "funcionaba" antes de configurar roles). `GET /sellers/v1` (getSellerAccount), `reports/v1/reportTypes`, etc. requieren su rol; si no está marcado → 403 genérico aunque el token sea válido.

Verificado 18/08/2026 con Neural-Commerce-dev (Digital Expressions): token exchange OK en 3 regiones, 403 en sellers/reports/productTypes → roles faltantes. Probar también con `--region na` ayuda a confirmar que el problema es de roles y no de región (da el mismo 403 genérico).

## Creación/llenado de listings (Listings Items API)
- Los requisitos de campos son **dinámicos por product type** — nunca hardcodear el esquema. Obtenerlo de Product Type Definitions API: `GET /definitions/2020-09-01/productTypes/{productType}?marketplaceIds={mkt}&requirements=LISTING` (solo disponible con credenciales de PRODUCCIÓN; el sandbox estático lo rechaza).
- **⚠️ Estructura real del response (VERIFICADO 18/08/2026):** `requirements` es un **string** (p. ej. `"LISTING"`), NO un dict de propiedades. El JSON Schema completo está en **`schema.link.resource`** (URL pre-firmada de S3, válida ~7 días) — hay que hacer un segundo GET para descargarlo. `scripts/listing_fields.py` tiene un bug: lee `requirements.properties` (vacío) en vez de descargar `schema.link.resource` → arreglarlo antes de usarlo en producción.
- Requeridas de PET_TOY AU (verificado): `brand`, `bullet_point`, `country_of_origin`, `item_name`, `product_description`, `supplier_declared_dg_hz_regulation` (mercancía peligrosa → `NOT_APPLICABLE`; NO existe en la plantilla flat file, hay que añadirla en la API).
- **`item_sku` NO es atributo** (va en la URL del PUT) y `external_product_id`/GTIN **no existe** como propiedad de PET_TOY — consistente con usar exención de GTIN. Cuidado con nombres de atributos que parecen obvios: `color_name`/`size_name`/`material_type`/`target_species` NO existen como tal en PET_TOY — consultar los 128 properties reales del schema.
- Flujo: buscar product type → descargar schema (desde `schema.link.resource`) → generar payload → `PUT /listings/2021-08-01/items/{sellerId}/{sku}` con `preview=true` (validar sin publicar) → si 0 issues, PUT real.
- **sellerId = Merchant Token** de Seller Central → Configuración → Información de cuenta → **Token de vendedor** (formato `A2XXXXXXXXXXXXX`). El CID del Solution Provider Portal (p. ej. `A1985DH23XBDSKG`) **NO** es el sellerId — la Listings API responde 400 `Invalid 'accountId' provided`.
- `PUT` reemplaza TODO el contenido (campos omitidos se borran); cambios parciales solo vía PATCH en `fulfillment_availability` y `purchasable_offer`.
- Helper: `scripts/listing_fields.py` — descarga schema, lista requeridos con constraints, genera plantilla de payload. Requiere credenciales producción en `.env`.
- **Fuente de verdad del listing de Digital Expressions:** carpeta Drive `16PJ2lsiT4CC1Zmq_-WtrsNsKd3S0aM8S` — contiene el listing COMPLETO ya hecho (`Listing_Completo_Snuffle_Mats_AU_v2.docx`, template Amazon PS-3058 lleno, proforma QH20260812, cotización). Las copias locales en `brain/raw/digital_expressions/` están **incompletas/obsoletas** (solo smoking kit + plantillas vacías). Antes de afirmar que "no existe contenido del listing", **listar y leer la carpeta Drive primero** — ver `scripts/drive_list.py` + `scripts/drive_download.py` (ambos en `/opt/data/scripts/`, token `/opt/data/google_token.json`).

## Atestación de seguridad (NO marcar "Sí" sin auditar)
Antes de declarar cumplimiento de controles (firewall, IR plan, MFA, cifrado, etc.), **auditar el estado real del VPS** (ufw/iptables, fail2ban/clamav, puertos Docker expuestos, docs de IR, permisos de .env). Patrón completo (8 controles + plan de implementación en 3 fases) en `references/security-controls-spapi.md`.

## Support files
- `references/onboarding-2026.md` — pasos detallados verificados de docs oficiales + respuestas de formulario listas.
- `references/security-controls-spapi.md` — los 8 controles de seguridad, auditoría real vs declarado, plan por fases.
- `references/listing-fields-and-drive.md` — mapa de campos por grupo (PET_PRODUCTS), estructura del payload PUT, contenido de la carpeta Drive (fuente de verdad), datos de los 3 ASINs (PS-3058/3052/3095) y preguntas pendientes (GTIN, riesgo DAFF).
- `scripts/spapi_token.py` — helper: obtiene access token y hace llamadas SP-API (lee credenciales de `/opt/data/.env`; con `--sandbox` lee `AMAZON_SPAPI_SANDBOX_*`).
- `scripts/listing_fields.py` — descarga el schema vigente de un product type, lista campos requeridos con constraints y genera plantilla de payload PUT.

## Pitfalls
- ❌ No ofrecer el flujo viejo (AWS IAM role + LWA security profile) — el SPP actual no lo pide.
- ❌ No llenar el campo orgID de Open Banking con texto ("No aplica" falla validación) — hay que DESMARCAR las funciones AISP/PISP en el paso de roles.
- ❌ No afirmar que "el listing no existe" sin leer primero la carpeta Drive `16PJ2lsiT4CC1Zmq_-WtrsNsKd3S0aM8S` — el contenido completo ya está ahí; las copias locales de brain/raw pueden estar obsoletas.
- ❌ No declarar controles de seguridad cumplidos sin verificar en el VPS (ufw, puertos expuestos, CRISIS.md).
- ❌ No usar localhost como redirect URI para apps públicas (no aceptado).
- ❌ No asumir que el refresh token de producción funciona apenas se genera — si se generó antes de habilitar roles en la app, dará 403 en TODOS los endpoints aunque el token exchange funcione. Regenerar (Authorize app) tras configurar roles.
- ❌ No marcar "Vendors"/"proveedores" ni "certificadores" en "Entidades empresariales admitidas" para una app privada de vendedor — seleccionar solo **Sellers**.
- ✅ Los `.md` de docs SP-API (llms.txt) se pueden leer con curl directo — `https://developer-docs.amazon.com/sp-api/docs/<pagina>.md` — más confiable que el HTML.


<!-- absorbido de software-development/amazon-sp-api (censo 2026-09-24) -->
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

# Access token (válido 1 hora)

curl -X POST 'https://api.amazon.com/auth/o2/token' \
  -H 'Content-Type: application/x-www-form-urlencoded;charset=UTF-8' \
  --data-urlencode 'client_id=...' --data-urlencode 'client_secret=...' \
  --data-urlencode 'grant_type=refresh_token' --data-urlencode 'refresh_token=...'
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
