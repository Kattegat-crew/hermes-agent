# Creación de listings por API (Listings Items v2021-08-01) — verificado 18/08/2026

Workflow probado en vivo con cuenta Digital Expressions (Amazon AU). Script: `/opt/data/amazon-spapi-setup/create_listing.py`.

## 1. Región y endpoints
- AU = región **fe**: `https://sellingpartnerapi-fe.amazon.com` (NO eu — verificado en vivo).
- Token: LWA refresh token → access token (1h) → header `x-amz-access-token`.
- PUT `/listings/2021-08-01/items/{sellerId}/{sku}?marketplaceIds=A39IBJ37TRP1C6&preview=true`.

## 2. Preview primero, siempre
`python3 create_listing.py --sku PS-3058 --preview` → HTTP 200 con `status: VALID|INVALID` y `issues[]`. Preview NO crea nada. Solo cuando VALID → crear sin `--preview` (200/202).

## 3. Campos condicionalmente requeridos (PET_TOY, AU)
El schema tiene bloques `allOf/if/then` que exigen más campos que los 6 del top-level:
- `contains_liquid_contents` [{value: false}]
- `directions` [{value: texto, language_tag}]
- `item_length_width_height` [{length:{value,unit}, width:{value,unit}, height:{value,unit}}] — unit obligatoria en cada uno
- `power_plug_type` [{value: "no_plug"}] (existe enum; desactiva accepted_voltage_frequency)
- `specific_uses_for_product` [{value, language_tag}]
- `model_name` / `model_number` (PS-3058)
- `unit_count` [{value: 1, type: {value:"count", language_tag}}]
- `supplier_declared_dg_hz_regulation` [{value:"not_applicable"}] — requerida top-level

## 4. Estructuras que fallan si se mandan mal
- `purchasable_offer` = [{"currency":"AUD","our_price":[{"schedule":[{"value_with_tax":44.99}]}],"audience":"ALL"}] — our_price es ARRAY con schedule.
- `list_price` = [{"currency":"AUD","value_with_tax":44.99}]
- `fulfillment_availability` = [{"fulfillment_channel_code":"DEFAULT","quantity":N}] (FBA = DEFAULT)
- item_sku NO es atributo (va en la URL); feed_product_type NO existe (productType en body).

## 5. GTIN / identificador — EL BLOQUEANTE
- `external_product_id` y `merchant_suggested_asin` NO están en properties del schema pero la ENFORCEMENT los exige (código 90220 MISSING_ATTRIBUTE).
- Sin GTIN (marca propia): la **exención GTIN DEBE estar APROBADA** antes de crear por API. NO se solicita "al crear el listing" — es trámite manual en Seller Central (Inventario → Añadir producto → "No tengo un ID de producto" → marca exacta + categoría + fotos producto/empaque, 24-48h).
- La marca de la exención debe ser IDÉNTICA a `brand` del listing.
- Hasta aprobarse, preview devuelve exactamente 2 errores: External Product ID + Merchant Suggested ASIN.
- No se puede inventar un GTIN ni un ASIN placeholder (validación real).

## 6. Rol requerido
Listings Items + Product Type Definitions (verificados activos). El resto (Sellers completo, Reports, Pricing) no es necesario para crear listings.
