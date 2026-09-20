---
name: amazon-spapi-integration
description: Use when setting up Amazon SP-API or seller API access.
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
