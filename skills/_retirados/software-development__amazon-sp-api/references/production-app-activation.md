# Activación de la app de Producción SP-API (verificado 2026-08-18, Neural-Commerce-dev)

## Campos del formulario (SPP, en español)

- **"Entidades empresariales admitidas"** = campo *User Access*: elegir SOLO **Vendedores**
  para una app privada de seller propio. Certificador / Proveedores / Carga / Envíos son
  otros programas (customs, Vendor Central, freight) — no aplican.
- **Pregunta de Token de datos restringidos (TDR/RDT)**: "¿Vas a delegar el acceso a la IIP
  a una aplicación de otro desarrollador?" → **No** (app privada, sin PII de terceros).
- **OAuth Login URI / OAuth Redirect URI — TRAMPA**: esos campos son **solo para apps
  PÚBLICAS** (redirigen a los vendedores a tu web durante la autorización). Si el formulario
  los pide, la app está configurada como pública. Para desarrollador privado:
  - La doc oficial lo dice explícito: "You can self-authorize your application in draft
    status because there is no reason to publish a private application" — las apps privadas
    se auto-autorizan **en estado Borrador**, sin URIs.
  - Fix: buscar el toggle "User Access / Acceso de usuario" → **Privada**. Si no existe,
    llenar una URI https válida de un dominio propio (localhost NO aceptado).

## Roles = la puerta de los endpoints

- El refresh token se genera igual **sin roles** — la autorización no depende de la
  selección de roles. Pero **sin roles operativos seleccionados en el form de la app, TODOS
  los endpoints devuelven 403** `Unauthorized / Access to requested resource is denied`.
- **Excepción: operaciones GRANTLESS** funcionan sin roles. Verificado:
  `GET /sellers/v1/marketplaceParticipations` respondió con datos reales de la cuenta
  (tienda, marketplaces MX/CA/US/BR) mientras `/sellers/v1` (getSellerAccount, NO grantless)
  daba 403. La sonda grantless es el primer diagnóstico ideal.
- Roles operativos a marcar: Listings Items, Product Type Definitions, Inventory, Reports,
  Orders, Product Pricing, Sellers.
- **Nombres de roles en el form SPP (español) → API** (verificado 18/08):
  - **Listing de producto** → Listings Items + Product Type Definitions + A+ Content (EL más importante para subir listings)
  - **Precios** → Product Pricing
  - **Seguimiento de pedidos e inventario** → Orders + Inventory
  - **Logística de Amazon** → FBA (Fulfillment Inbound/Outbound)
  - **Información sobre el colaborador comercial** → Sellers
  - **Finanzas y contabilidad** → Finances
  - **Comunicación con el comprador** → Messaging (restricted/PII)
  - **Solicitud de comprador** → Solicitations (request reviews)
- **Límite de 8 de 10 roles de vendedor**: si el form limita a 8, dejar FUERA **Análisis de
  marcas** (Brand Analytics — requiere Brand Registry, solo insights) y **Almacenamiento y
  distribución de Amazon** (AWD — no se usa, es FBA lo que importa).

## Tokens por región (cuenta merged/global)

- Una cuenta vendedora global (AU + NA) genera **un refresh token POR REGIÓN**: token de
  Australia se usa contra `sellingpartnerapi-eu.amazon.com`; token de NA contra
  `sellingpartnerapi-na.amazon.com`. Verificado: token NA @ eu → 403.
- El refresh token **congela los roles al momento de generarse**: después de cambiar la
  selección de roles en el formulario, hay que **re-autorizar (Action → Authorize app) por
  CADA región** y usar los tokens nuevos. Generar un token nuevo NO invalida los anteriores
  (docs), así que descartar los viejos es manual.

## Diagnóstico paso a paso

1. `python3 scripts/test_region_tokens.py` — prueba token×región contra la sonda grantless.
   - Token inválido → falla en todas las regiones.
   - Región equivocada → falla en una, funciona en la otra.
   - Sonda OK pero `/sellers/v1` 403 → roles faltantes en el form de la app.
2. Si falta un rol → SPP → editar app → Niveles → marcar rol → Guardar → re-autorizar cada
   región → probar de nuevo.
3. El access token del intercambio LWA puede obtenerse aunque la app no tenga roles — el
   intercambio exitoso NO prueba que la app esté operativa.

## Otros hallazgos (18/08/2026)

- **App Integrations API** = notificaciones en Seller Central (banner: "tienes X productos con
  inventario bajo"). Opcional — NO bloquea la activación de la app ni el uso de SP-API.
  Requiere rol "Notifications in Seller Central" + plantilla (tipo en MAYÚSCULAS_CON_GUIONES,
  contenido ≤250 chars con 1-5 parámetros tipados number/date/ASIN, CTA URL obligatoria,
  topic, granularity) + envío a revisión de Amazon. Leer: `app-integrations.md` y
  `create-an-app-notification-template.md` en developer-docs.
- **Cuenta global en "Tus cuentas" del SPP**: puede aparecer como
  "BR - \<merchant_id\>_\<marketplaceId\>_\<id\>" — es la MISMA cuenta vendedora (representación
  técnica; el prefijo merchant coincide con el CID del portal, ATVPDKIKX0DER = US). No es una
  cuenta separada ni algo que el usuario haya creado.
- **SPP help/portal está detrás de login**: `curl` a `solutionproviderportal.amazon.com/...`
  redirige a `/ap/signin` (HTML de login). Para investigar el portal, usar developer-docs
  (páginas `.md`) o pedir captura al usuario — no hay scraping del portal.
- **Truco de scripting**: NO embebas refresh tokens largos en comandos shell inline (el
  parser hardline bloquea payloads gigantes — error "BLOCKED (hardline)"). Escribir un `.py`
  que cargue `/opt/data/.env` con parser simple (`k, v = line.split("=", 1)`) y haga las
  llamadas desde ahí; nunca `$(grep ...)` con tokens en el comando.
- **Token en captura vs pegado**: la fila "Australia" muestra el token truncado en el input
  (p.ej. `Atzr|lwE...` con ele minúscula visible) — el pegado real empieza `Atzr|IwE...`.
  Si el token pegado falla en todas las regiones y el de otra región funciona, verificar que
  se copió de la fila correcta (botón "Copiar" de ESA fila).
