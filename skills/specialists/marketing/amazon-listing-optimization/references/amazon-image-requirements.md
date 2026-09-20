# Amazon Image Requirements — Checklist de Compliance

Especificaciones técnicas para imágenes de productos en Amazon.
Una imagen principal NO-compliant = supresión del listing en búsquedas.

## Imagen Principal (Obligatorio)

| Requisito | Especificación |
|-----------|---------------|
| Fondo | Blanco puro, RGB 255/255/255 (exacto) |
| Tamaño del producto | 85%+ del frame |
| Resolución mínima | 1,000px en el lado más corto |
| Resolución recomendada | 3,000px (permite zoom integrado) |
| Formato | JPEG, TIFF, PNG (ideal: JPEG) |
| Texto en la imagen | ❌ PROHIBIDO |
| Logos | ❌ PROHIBIDOS |
| Gráficos/ilustraciones | ❌ PROHIBIDOS |
| Otros productos | ❌ PROHIBIDOS |
| Accesorios no incluidos | ❌ PROHIBIDOS |
| Marcas de agua | ❌ PROHIBIDAS |
| Bordes/marcos | ❌ PROHIBIDOS |

**⚠️ La verificación es automática:** Un fondo que "parece blanco"
pero es #F8F8F8 puede ser rechazado por el checker automatizado.
Usar herramienta de recorte con preset exacto RGB 255/255/255.

## Imágenes Secundarias (Opcionales pero Recomendadas)

| Slot | Contenido | Requisitos |
|------|-----------|------------|
| 2 | Vista de ángulo | 1600px+ recomendado, producto completo visible |
| 3 | Lifestyle/uso | Contexto real, mascota/modelo usando el producto |
| 4 | Dimensiones | Diagrama con medidas exactas (no exagerar) |
| 5 | Características/USPs | Infografía con beneficios clave |
| 6 | Detalle/material | Close-up de textura, costura, acabado |
| 7 | Empaque | Caja/envase real (si es ventaja) |
| 8 | Video/3D | Thumbnail de video de producto |
| 9 | Comparación | Tabla comparativa de variantes |

**Regla para secundarias:**
- Texto permitido SOLO en imágenes 4-9 (infografías)
- Las imágenes 2-3 deben ser fotos reales, no renders
- Mantener coherencia visual entre todas las imágenes
- Mostrar el producto en proporción real (no engañar con escala)

## Estándares por Categoría

### Ropa (Apparel)
- Ghost mannequin (maniquí invisible) para prendas
- Fotos con modelo en imágenes lifestyle
- Mostrar todos los ángulos relevantes

### Pet Supplies
- Tamaño relativo con objeto conocido (ej: una mano, una pelota)
- Mostrar el producto con mascota real en imágenes lifestyle
- Dimensiones en cm Y pulgadas (mercados AU/US/UK)

### Electrónica
- Mostrar conectores, puertos, botones
- Incluir cable/adaptador si viene incluido
- Escala relativa con la mano

## Herramientas para Compliance

1. **Verificar RGB:** Python PIL — `Image.open(path).getpixel((0,0))`
2. **Verificar resolución:** `identify image.jpg` (ImageMagick) o PIL
3. **Checklist final antes de subir:**
   - [ ] Fondo RGB 255/255/255 exacto
   - [ ] Producto ocupa 85%+ del frame
   - [ ] Sin texto/logos/marcas de agua
   - [ ] Mínimo 1000px lado corto (ideal 3000px)
   - [ ] JPEG con calidad alta
   - [ ] 7-9 imágenes totales
   - [ ] Coherencia de estilo entre todas

## Costos de Error

| Error | Consecuencia |
|-------|-------------|
| Fondo no blanco | Listing suprimido de búsqueda |
| <1000px | Sin zoom, posible rechazo |
| Texto en principal | Supresión inmediata |
| Logos | Supresión inmediata |
| Escala engañosa | Reviews negativas, retornos, posible suspensión |