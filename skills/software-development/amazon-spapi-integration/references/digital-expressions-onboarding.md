# Caso: Digital Expressions — onboarding SP-API (2026-08-18)

## Contexto
- Cuenta: J&N Digital Expressions LLC (Wyoming, USA) — tienda Amazon Australia (snuffle mats, plan Professional).
- Objetivo: automatizar inventario, reportes de ventas → NeuralCrew Analytics, y repricing.
- Marketplace ID AU: `A39IBJ37TRP1C6` · Región SP-API: **EU** (`sellingpartnerapi-eu.amazon.com`).

## Estado
- ✅ Paquete de setup creado: `/opt/data/amazon-spapi-setup/`
  - `spapi_token.py` — helper probado (--help OK): obtiene access token vía LWA y llama endpoints; lee `AMAZON_SPAPI_*` de `/opt/data/.env`; flags `--test`, `--endpoint`, `--sandbox`, `--region`.
  - `GUIA-ONBOARDING-SP-API.md` + `.docx` (entrega al humano, preferencia DOCX del usuario).
- ✅ Brain entity `digital_expressions.md` actualizado con sección SP-API.
- ⏳ Pendiente humano (requiere login de Jonathan en Seller Central):
  1. Developer Profile privado en Seller Central AU → Apps and Services → Develop Apps
  2. Esperar aprobación (responder ≤5 días)
  3. App sandbox en SPP → credenciales LWA + refresh token sandbox
  4. App producción → Authorize app → refresh token producción
  5. Entregar credenciales a Ragnar → `.env` (`AMAZON_SPAPI_CLIENT_ID`, `_CLIENT_SECRET`, `_REFRESH_TOKEN`, `_REGION=eu`, `_MARKETPLACE_ID=A39IBJ37TRP1C6`) → smoke test `spapi_token.py --test`

## Automatizaciones previstas (post-credenciales)
1. Sync diario inventario FBA → tabla local/Sheets
2. Reporte `GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_PERIOD` → ventas diarias → NeuralCrew Analytics
3. Repricing contra Buy Box (Product Pricing API)
4. Alta/edición de ASINs (Listings Items API 2021-08-01)

## Docs verificados en esta sesión (fuentes)
- llms.txt index: `https://developer-docs.amazon.com/sp-api/llms.txt`
- Flujo confirmado: onboarding-step-1/4/5/7 + register-as-a-private-developer + self-authorization (páginas .md).
- El flujo 2026 ya NO usa AWS IAM: SPP genera client ID/secret/refresh token internamente.
