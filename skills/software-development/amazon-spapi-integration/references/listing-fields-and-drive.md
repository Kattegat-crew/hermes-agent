# Listing fields + fuente de verdad Drive (SP-API) — sesión 2026-08-18

## Fuente de verdad: carpeta Drive del listing
**Carpeta:** `16PJ2lsiT4CC1Zmq_-WtrsNsKd3S0aM8S` (22 archivos)
- `Listing_Completo_Snuffle_Mats_AU_v2.docx` — LISTING COMPLETO DEFINITIVO (3 ASINs independientes; v1 con variaciones quedó superada)
- `PS3058_Grande_Snuffle_Mat_Filled.xlsx/.csv` — plantilla oficial Amazon (feed PET_TOY) LLENADA para PS-3058
- `QS_Digital_Expresions_LLC.pdf`, `pre_forma_invoice_pedido_amazon.pdf` / `QH20260812.pdf` — cotización + proforma (397 pcs, $2,395.84, Hangzhou Queenhe)
- `TA_CONTRACT_1786594723225.pdf`, `NEW_PACKING_LIST_GI_TIXXI.xlsx`, recibos de pago
- `producto_imagen.jpg` — foto del proveedor (candidata a imagen principal)
- Copias locales en `brain/raw/digital_expressions/` están INCOMPLETAS (Listing.docx = smoking kit US, Technical_Data_Sheet vacío) → **siempre leer la carpeta Drive antes de concluir que no existe contenido**

**Acceso Drive:** `python3 /opt/data/scripts/drive_list.py <folder_id>` y `python3 /opt/data/scripts/drive_download.py <outdir> '<json>'` (token `/opt/data/google_token.json`, scope drive.readonly). Para nativos de Google (GAPP:spreadsheet) usar modo `export` con mime xlsx; archivos subidos (.docx/.pdf/.xlsx) modo `file`.

## Datos del producto — 3 ASINs (confirmados por listing v2 + proforma)

| | PS-3058 GRANDE | PS-3052 MEDIANO | PS-3095 PEQUEÑO |
|---|---|---|---|
| Tamaño | 70×50cm | 50×80cm | 40×60cm |
| Material | Fieltro sintético | Polar fleece | ⚠️ Cotton+wool (riesgo DAFF) |
| Incluye | 5 zanahorias | 2 zanahorias + 1 bola | base antideslizante |
| Precio AU | $44.99 | $34.99 | $29.99 |
| Costo EXW | $6.34 | $5.55 | $5.47 |
| Pedido | 175 pcs (7 cajas) | 150 pcs (5 cajas) | 72 pcs (2 cajas) |
| Peso | 0.3 kg | no declarado | no declarado |

Compartido: Brand `Digital Expressions` · Manufacturer `Hangzhou Queenhe Import & Export Co., Ltd.` · item_type `dog-puzzle-toy` · FBA DEFAULT · New · Pet Supplies > Dogs > Dog Toys > Puzzle Toys · vacuum-sealed + cartón 60×40×50 · 100% Money Back · Care: máquina/suave/aire.

Template PS-3058 lleno incluye: título, 5 bullets, descripción, backend keywords, material (Polyester felt/fleece), color Grey Beige, tamaño, componentes, origen China, peso 0.3 kg, list_price 44.99, quantity 175, care, garantía, breed recommendation.

## Mapa de campos — PET_PRODUCTS / PET_TOY (por grupo)

1. **Identidad:** `item_name` (≤200), `brand`, `item_type_keyword`, `recommended_browse_nodes`
2. **Identificadores:** `gtin` (8-14 dígitos, requerido salvo Brand Registry), `external_product_id(+type)`, `part_number`
3. **Contenido SEO:** `bullet_point` (5 × ≤500), `product_description` (≤2000), `main_product_image_locator` (blanca 1000px+), `product_images` (≤9), `search_terms` backend
4. **Atributos:** `material`, `color`, `target_species`, `item_package_weight`/`item_weight`, `item_dimensions`/`item_package_dimensions` (críticos fees FBA), `condition_type` (New), `safety_and_compliance`
5. **Precio:** `purchasable_offer.list_price` (+`our_price` si promoción), currency explícita (AUD)
6. **Cumplimiento:** `fulfillment_availability.fulfillment_channel_code` (DEFAULT=FBA) + `quantity`; FBM usa `merchant_shipping_group_name` (no aplicar a FBA)

**Flujo:** Product Type Definitions (schema vigente, dinámico) → `PUT /listings/2021-08-01/items/{sellerId}/{sku}` → respuesta = issues. `preview=true` valida sin publicar. PUT reemplaza TODO; PATCH solo fulfillment_availability/purchasable_offer.

## Preguntas pendientes (18/08 — sin resolver aún)
1. **GTIN/UPC:** `external_product_id` VACÍO en template → sin UPC/EAN no se crea ASIN (o falta Brand Registry)
2. **PS-3095 riesgo DAFF:** proforma dice "Primalog cotton + wool" vs listing "100% sintético" → confirmar con proveedor (algodón/lana = orgánicos, rechazo aduana AU)
3. Imágenes: sin Main Image URL (usar `producto_imagen.jpg` Fase 1)
4. Dimensiones paquete unitario faltantes (fees FBA)
5. `merchant_shipping_group_name="FBA"` con fulfillment FBA → probable warning, quitar
6. Templates PS-3052/PS-3095 no existen (solo PS-3058)
7. Pesos PS-3052/PS-3095 no declarados

## Errores típicos de validación (mapeo)
| Error | Causa |
|---|---|
| InvalidAttributeValue | Valor fuera de constraint del schema |
| MissingAttribute | Requerido omitido |
| InvalidProductType | productType mal escrito |
| InvalidImage | URL inaccesible o fondo no blanco |
| InvalidGtin | GTIN inválido/duplicado |
