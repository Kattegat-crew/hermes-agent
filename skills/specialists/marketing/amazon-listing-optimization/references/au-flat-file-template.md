# Amazon AU Flat File Template (2026)

## Estructura General

La plantilla oficial descargada de Seller Central AU tiene las siguientes características:

- **feedType:** `256` (cambia según la categoría)
- **Marketplace ID AU:** `A39IBJ37TRP1C6`
- **Idioma:** `en_AU` (inglés australiano)
- **Total columnas:** ~286
- **Filas clave:**
  - Fila 3: Nombres de sección (Listing Identity, Variations, Product Identity, Images, Product Details, Offer, Offer (AU), Shipping, Safety & Compliance)
  - Fila 4: Nombres visibles en inglés (ej: "Bullet Point", "Item Name")
  - Fila 5: **API names** (ej: `bullet_point[marketplace_id=A39IBJ37TRP1C6][language_tag=en_AU]#1.value`)
  - Fila 6+: Datos del producto

## Columnas Esenciales para un Listing

| Col | API Name | Descripción |
|-----|----------|-------------|
| 1 | `contribution_sku#1.value` | SKU del producto |
| 2 | `product_type#1.value` | Tipo de producto (ej: PET_TOY) |
| 3 | `::record_action` | Update / Delete |
| 4 | `parentage_level...1.value` | Parent (standalone) / Child (variation) |
| 7 | `item_name...1.value` | Título del producto |
| 9 | `brand...1.value` | Marca |
| 10-11 | `amzn1...product_id_type/value` | GTIN/UPC/EAN (optional con exención) |
| 12-16 | `recommended_browse_nodes...value` | Browse Node IDs para categorización |
| 20-24 | `target_audience_keyword...value` | Público objetivo (Dogs, Cats, Rabbits) |
| 25 | `model_number...1.value` | Número de modelo |
| 27 | `manufacturer...1.value` | Fabricante |
| 38 | `product_description...1.value` | Descripción larga del producto |
| 39-43 | `bullet_point...#1-5.value` | 5 bullet points |
| 44 | `generic_keyword...1.value` | Backend search terms (250 bytes) |
| 51-55 | `material...#1-5.value` | Materiales |
| 56 | `number_of_items...1.value` | Cantidad de items |
| 60 | `color...1.value` | Color |
| 61 | `size...1.value` | Tamaño |
| 62 | `part_number...1.value` | Número de parte |
| 118 | `pet_toy_type...1.value` | Tipo de juguete mascota |
| 123-127 | `pet_type...#1-5.value` | Tipo de mascota (Dog, Cat, Rabbit, etc) |
| 129-130 | `item_weight...value/unit` | Peso y unidad |
| 132 | `condition_type...1.value` | Condición (New) |
| 134 | `list_price...value_with_tax` | Precio lista con impuesto |
| 157 | `fulfillment_availability#1...channel_code` | DEFAULT = canal por defecto de la cuenta (para sellers FBA = FBA) |
| 158 | `fulfillment_availability#1.quantity` | Cantidad en stock |
| 162 | `purchasable_offer...#1.schedule#1.value_with_tax` | Precio de venta AUD |
| 183 | `country_of_origin...1.value` | País de origen |

## Proceso de Llenado (Python + openpyxl)

```python
import openpyxl, shutil

# 1. Copiar plantilla original
shutil.copy2('template.xlsm', 'filled.xlsx')

# 2. Abrir con openpyxl
wb = openpyxl.load_workbook('filled.xlsx')
ws = wb['Template']

# 3. Mapear API names a columnas
api_cols = {}
for cell in ws[5]:  # Fila 5 = API names
    if cell.value:
        api_cols[cell.value] = cell.column

# 4. Llenar datos en fila 6
data = {
    'contribution_sku#1.value': 'MI-SKU',
    'item_name...1.value': 'Mi Título',
    # ...
}
for api_name, value in data.items():
    if api_name in api_cols:
        ws.cell(row=6, column=api_cols[api_name], value=value)

wb.save('filled.xlsx')
```

## Mapeo de cabeceras CSV (plantilla descargada, PET_TOY — verificado 2026-08-18)

Cuando el usuario sube la plantilla descargada de Seller Central AU y se exporta como CSV,
la cabecera usa nombres simples (NO los API names con marketplace_id). Verificado en
`PS3058_Grande_Snuffle_Mat_Filled.csv`:

```
feed_product_type, item_sku, brand_name, update_delete, external_product_id,
external_product_id_type, item_name, manufacturer, product_description, item_type,
part_number, care_instructions1..3, bullet_point1..5, breed_recommendation,
generic_keywords, target_audience_keywords, material_type1..2, color_name, size_name,
item_type_name, target_species1..3, included_components, country_of_origin, item_weight,
item_weight_unit_of_measure, warranty_description, list_price, condition_type,
number_of_items, merchant_shipping_group_name,
fulfillment_availability#1.fulfillment_channel_code, fulfillment_availability#1.quantity,
purchasable_offer[marketplace_id=...]#1.our_price
```

Notas:
- `feed_product_type` = PET_TOY (categoría) — define qué columnas aplican.
- **`item_package_dimensions` (largo/ancho/alto/unidad) NO viene en el CSV por defecto** — es
  crítico para fees FBA y hay que añadirlo/rellenarlo (o preguntar al proveedor).
- `external_product_id` vacío + marca propia → exención de GTIN (ver au-listing-validation).
- `merchant_shipping_group_name` es SOLO para FBM — con FBA (fulfillment_channel_code=DEFAULT)
  debe quedar VACÍO (poner "FBA" ahí genera warning; verificado en sesión snuffle mats).

## Pitfalls

- ❌ **NO crear CSV desde cero** — Amazon lo rechaza con "template version outdated". Siempre usar el XLSM descargado de Seller Central.
- ❌ **NO usar plantilla vieja** — Si el usuario te pasa una plantilla descargada antes, puede estar desactualizada. Pedir que descargue una nueva.
- ❌ **NO usar openpyxl en read_only=True para llenar** — Usar modo normal para poder escribir.
- ❌ **NO confundir filas** — En la plantilla 2026 los API names están en fila 5 (no fila 3 como versiones anteriores).
- ✅ **Siempre verificar que los API names coincidan exactamente** — openpyxl no avisa si no encuentra el nombre.
- ✅ **Siempre guardar como XLSX** (no XLSM) — Amazon acepta XLSX.
- ✅ **Browse Nodes dejar que Amazon los asigne automáticamente** o poner el ID numérico en las columnas 12-16.