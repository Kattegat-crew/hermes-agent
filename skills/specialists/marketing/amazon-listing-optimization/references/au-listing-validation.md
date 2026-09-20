# Validación de Listings Amazon AU — Fuentes, Constraints y Trampas (2026-08-18)

Validado en la sesión de snuffle mats (Digital Expressions, 3 ASINs PS-3058/PS-3052/PS-3095).

## 1. Fuente de verdad: carpeta Drive del listing

- **SIEMPRE listar la carpeta Google Drive del listing ANTES de concluir que falta contenido.**
  - Carpeta Digital Expressions: `16PJ2lsiT4CC1Zmq_-WtrsNsKd3S0aM8S` (22 archivos: Listing_Completo_*.docx, plantilla Amazon llenada, proforma, cotización, contratos).
  - `brain/raw/digital_expressions/` local SOLO tiene el producto previo (Smoking Kit). Los `Listing.docx` locales NO son del producto actual.
- Scripts reutilizables:
  - `python3 /opt/data/scripts/drive_list.py <FOLDER_ID>` — lista archivos (id, nombre, mime, tamaño).
  - `python3 /opt/data/scripts/drive_download.py <OUTDIR> '<json [[id,nombre,mode,mime],...]>'` — descarga binarios (`file`) o exporta nativos Google (`export`).
  - Token: `/opt/data/google_token.json` (scope drive.readonly).

## 2. Constraints de campos (validar SIEMPRE antes de subir)

| Campo | Límite | Fuente |
|---|---|---|
| `item_name` (título) | ≤ 200 caracteres | Amazon |
| `bullet_point` (5) | ≤ 500 c/u | Amazon |
| `product_description` | ≤ 2,000 | Amazon |
| `generic_keywords` (backend) | 250 bytes | Amazon |

**⚠️ Hallazgo real:** el doc "Listing Completo" v2 tenía los 3 títulos SOBRE el límite
(PS-3058=221, PS-3052=227, PS-3095=216). Los docs fuente pueden traer títulos inválidos.
Siempre medir con `len(titulo)` y recortar la frase de menor valor SEO (ej. "Interactive
Feeding Mat") sin perder la keyword principal.

## 3. Validación cruzada: listing vs proforma invoice

La **proforma invoice del proveedor es la fuente de verdad** para:
- **Accesorios incluidos** (PS-3052: "2 carrots and 1 ball" — el usuario dijo primero 1, la proforma tenía razón).
- **Materiales/composición** — CRÍTICO para bioseguridad.

**⚠️ Riesgo DAFF (AU):** el listing afirmaba "100% synthetic, biosecurity compliant" pero la
proforma QH20260812 decía "Primalog cotton + wool" para el PS-3095. Algodón y lana son
materiales ORGÁNICOS → riesgo de rechazo en aduana australiana (BICON/DAFF).
Regla: si la proforma menciona cotton/wool/hemp/organic, el claim "100% sintético" es FALSO
hasta que el proveedor confirme. No subir el ASIN hasta resolver.

## 4. Leer plantillas flat-file de Amazon (xlsx)

- El tab **Template** del xlsx contiene blobs base64 de settings (~290KB de ruido).
- **Preferir la exportación CSV** (limpia, header en fila 1, datos en fila 2).
- El string `settings=` del xlsx revela `labelRow`/`attributeRow`/`dataRow` si hay que leer el xlsx.
- `external_product_id` VACÍO + marca propia → se necesita **exención de GTIN**
  (Seller Central → Add a Product → "I don't have a product ID") con fotos producto+empaque
  mostrando la marca. Aprobación 24-48h.

## 5. Estructura de entrega útil (patrón "sheet de listings")

- Un xlsx con hoja LISTINGS (1 fila por ASIN, columnas = nombres de la plantilla Amazon/API)
  + hoja PENDIENTES (items abiertos con detalle).
- Celdas amarillas = provisional/pendiente (GTIN, imágenes, pesos, dimensiones).
- Verificar al final: `len()` de títulos y bullets contra límites; precio/cantidad por ASIN.
- **Script reutilizable:** `scripts/validate_listing_limits.py <sheet.xlsx>` — valida
  item_name ≤200, bullets ≤500, descripción ≤2000, generic_keywords ≤250 **bytes**. Úsalo
  SIEMPRE al final del llenado (atrapó 3 títulos sobre 200 y 3 keywords sobre 250 bytes).

**⚠️ Hallazgo real #2:** los `generic_keywords` del Listing v2 también excedían el límite
(313/293/314 bytes vs 250). Al recortar, quitar del FINAL (menor valor SEO: "pet gift birthday
christmas", "cabin fever", "reward feeder") — nunca las keywords core del inicio.

## 6. Análisis de imágenes del catálogo del proveedor

El proveedor envía catálogos (fondos beige/blanco, 3 paneles: lifestyle + diagrama + macro).
Extraer por ASIN y CRUZAR contra la proforma (sesión snuffle mats, 2026-08-18):

- **Colores reales** — casi nunca coinciden con el template ("Grey Beige" del sheet era
  incorrecto: PS-3058 = base amarilla tema jardín, PS-3052 = base teal, PS-3095 = flores
  rosa/amarillo/rojo borde amarillo). Actualizar `color_name` con lo que muestra la imagen.
- **Accesorios visibles** — PS-3058 mostraba 4 maceteros + zanahoria + fresa (tema jardín),
  NO "5 zanahorias" del título; PS-3052 NO mostraba la bola squeaky del copy. Confirmar con
  proveedor antes de dejar claims en título/bullets.
- **Base antideslizante** — PS-3095 la confirmaba en vista inferior (gris con puntos negros).
  Si el proveedor mejora la base por quejas de clientes → actualizar bullets con
  "ENHANCED NON-SLIP" en los 3 ASINs.
- **Logos del proveedor** — PS-3052 tenía "B13" cosido en la rosa central. Retirar de la
  imagen principal (Amazon rechaza logos ajenos / conflicto con brand propia).
- Guardar imágenes como `<SKU>_catalogo.jpg` en `listing-sources/`; actualizar color_name,
  NOTAS y URLs en el sheet. Imágenes finales: editar fondo blanco 3000px + 9 slots.

## 7. Playbook reutilizable — próximo producto (checklist)

1. Listar carpeta Drive del listing (`drive_list.py <FOLDER_ID>`) — SIEMPRE primero; no
   concluir que falta contenido sin listar.
2. Descargar todo (`drive_download.py`) y leer proforma + cotización (accesorios, materiales,
   cantidades, precios EXW) y el listing doc si existe.
3. Validar títulos ≤200 y bullets ≤500 del doc fuente (pueden venir EXCEDIDOS).
4. Analizar imágenes de catálogo → colores, accesorios, base, logos (sección 6).
5. Cross-verificar: proforma vs listing vs imágenes (accesorios, DAFF, claims).
6. Construir sheet: LISTINGS (columnas plantilla Amazon) + PENDIENTES; celdas amarillas
   para provisional/pendiente.
7. Validar límites con `scripts/validate_listing_limits.py`.
8. GTIN: exención si marca propia sin código de barras (fotos producto+empaque con marca).
9. DAFF: si la proforma menciona cotton/wool/hemp/organic → NO subir hasta confirmar 100%
   sintético (riesgo BICON en aduana AU).
10. FBA: fulfillment_channel_code=DEFAULT + quantity; merchant_shipping_group_name VACÍO.
11. Imágenes: fondo blanco 3000px, sin logos proveedor, 9 slots.
12. SP-API: `listing_fields.py --product-type <TIPO> --full` para schema vigente y
    `preview=true` antes del PUT real.
