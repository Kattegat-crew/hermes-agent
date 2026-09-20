---
name: amazon-listing-optimization
description: >-
  Use when creating Amazon listings. Title, images, bullets.
version: 1.0.0
author: Ragnar
license: MIT
metadata:
  hermes:
    tags: [amazon, listing, optimization, seo, conversion, ecommerce, marketplace]
    category: ecommerce
    related_skills: [amazon-fba-profitability, document-reader]
---

# Amazon Listing Optimization

Flujo completo para crear y optimizar listings en Amazon Seller Central.
Cubre tanto visibilidad (SEO/A9) como conversión (CRO). Diseñado para
productos nuevos y existentes.

## Cuándo Usar

- **ALWAYS** al crear un listing nuevo en cualquier marketplace Amazon
- **ALWAYS** al optimizar un listing existente con bajo rendimiento
- **ALWAYS** al expandir a un nuevo marketplace (US → AU → UK)
- **NUNCA** antes de tener los datos del producto (peso, dimensiones, costo)
- **NUNCA** usar como sustituto del análisis de rentabilidad (usar amazon-fba-profitability)

## Estructura del Listing (Orden de Prioridad)

### 1. Título del Producto

El elemento de mayor peso en el algoritmo A9.

| Elemento | Especificación |
|----------|---------------|
| Longitud | 150-200 caracteres según categoría |
| Posición keyword principal | Primeros 80 caracteres (crítico para móvil) |
| Estructura | Marca + Keyword principal + Keywords secundarias + Tamaño/Cantidad + Diferenciadores |
| Idioma | Lenguaje de búsqueda del comprador, NO descripción del producto |

**Estructura recomendada:**
```
[Marca] [Keyword Principal] - [Keyword Secundaria] [Atributo] [Tamaño/Cantidad] [Diferenciador Clave]
```

**Ejemplo (snuffle mat AU):**
```
PetSniff™ Snuffle Mat for Dogs - Interactive Feeding Mat, Slow Feeder for Boredom Relief, Washable Sniffle Mat with Non-Slip Backing - 50x80cm
```

### 2. Imágenes (Máximo 9 Slots)

| Slot | Tipo | Requisito Técnico |
|------|------|-------------------|
| #1 Principal | Fondo blanco puro | RGB 255/255/255, producto 85%+ del frame, SIN texto/logos/gráficos, mínimo 1000px (ideal 3000x3000px para zoom) |
| #2-3 Lifestyle | Producto en uso real | Contexto de uso, preferiblemente con mascotas/modelos |
| #4-5 Infografías | Dimensiones y USPs | Medidas, materiales, características clave destacadas |
| #6-7 Ángulos/Detalles | Perspectivas alternativas | Close-ups de materiales, costuras, textura |
| #8-9 Confianza | Video demo + prueba social | Video de producto, empaque, certificaciones |

**Regla de oro:** Usa TODOS los slots. Cada imagen adicional responde una pregunta del comprador.

### 3. Bullet Points (5 Puntos)

```
[ANCLA VISUAL - 2-4 palabras en mayúscula] + [Beneficio principal] + [Feature] + [Prueba/Dato]
```

**Estructura por bullet:**
1. **Beneficio primario** — el problema que resuelve
2. **Diferenciador** — qué lo hace único vs competencia
3. **Caso de uso / Especificaciones** — dimensiones, materiales, cuidado
4. **Prueba social / Calidad** — certificaciones, garantía, lavable, duradero
5. **Confianza / Post-venta** — satisfacción garantizada, soporte, devolución

**⚠️ Pitfall:** En móvil los bullets se cortan. Primera oración = lo más importante. Primeros 70-80 caracteres críticos.

### 4. Descripción / A+ Content

| Tipo | Cuándo Usar |
|------|------------|
| A+ Content (Brand Registry) | SIEMPRE si estás registrado — mejora conversión 5-15% |
| Descripción estándar (2,000 chars) | Solo si NO tienes Brand Registry |

**A+ Content debe incluir:**
- Módulo de encabezado con imagen hero
- Tabla comparativa de características
- Diagrama de dimensiones
- Módulo de beneficios con iconos
- Sección de FAQ que prevenga objeciones
- Bloque de historia de marca

### 5. Backend Search Terms

| Campo | Límite | Reglas |
|-------|--------|--------|
| Términos genéricos | 250 **bytes** (no caracteres) | Sinónimos, misspellings, variantes long-tail que NO están en el título |
| | | NO repetir palabras del título |
| | | NO incluir marca, ASIN, ni nombres de competidores |

**Técnica:** Para marketplace AU, incluir términos en inglés australiano (colour vs color, tyre vs tire, centre vs center).

### 6. Precio y Posicionamiento

- Amazon usa el precio como señal de ranking en búsquedas por categoría
- Si estás sobre el promedio, el listing debe justificarlo visualmente
- **Comisiones por categoría (referencia 2025-2026):**
  - AU Pet Supplies: 15% (mín $4.00 AUD)
  - US Pet Supplies: 15% (mín $0.75)
  - UK Pet Supplies: 15% (mín £2.00)
- + tarifas FBA (varían por peso/dimensiones y marketplace)
- + PPC recomendado: 10-20% del precio

### 7. Reseñas y Prueba Social

| # Reviews | Impacto |
|-----------|---------|
| 0 | Conversión extremadamente baja — sin confianza |
| 1-10 | Conversión significativamente reducida |
| 10-50 | Conversión promedio |
| 50+ | Conversión óptima — prueba social sólida |

**Métodos legítimos para conseguir reseñas:**
- Amazon Request a Review button (en Seller Central, 30 días post-entrega)
- Amazon Vine (Brand Registry, productos nuevos)
- Superar expectativas de calidad vs precio

### 8. Variaciones (Parent-Child)

**Beneficios:**
- Consolidación de reseñas (todos los variantes bajo un mismo listing)
- Mejora conversión: el comprador elige talla/color sin salir de la página
- Mayor densidad de keywords en el listing padre

**⚠️ Pitfall:** NO crear variaciones para productos que no son realmente variantes del mismo diseño — Amazon puede eliminar el listing.

## Orden de Optimización Recomendado

Siempre en este orden — los elementos se componen:

1. **Keywords en título** — sin keywords correctas, nada importa
2. **Imagen principal compliant** — decide el CTR, y CTR es input del ranking
3. **Precio vs competidores** — la otra mitad del click
4. **Set completo de imágenes + bullets** — dueños de la conversión
5. **Backend keywords + A+ Content** — capa de refinamiento
6. **Estrategia de reseñas** — acelerador de conversión
7. **Variaciones** — consolidación de prueba social

> **⚠️ Regla crítica:** Audit scoring antes de cambiar. NO cambiar múltiples elementos simultáneamente. Identificar el cuello de botella, arreglarlo, medir, siguiente.

## Consideraciones por Marketplace

### Amazon Australia (AU) — Específico
- **Idioma:** Inglés australiano (colour, centre, tyre, organise, favourite, behaviour)
- **Temporada:** Invierno AU = Jun-Ago, Verano = Dic-Feb (inverso al hemisferio norte)
- **Feriados clave:** Australia Day (26 Ene), ANZAC Day (25 Abr), Boxing Day (26 Dic), EOFY (30 Jun)
- **Moneda:** AUD — tasa de conversión fluctuante vs USD
- **Competencia:** Menor que US pero buyers más sensibles al precio
- **Envío:** FBA AU tiene cobertura limitada vs US — verificar si tu producto califica
- **GST:** 10% sobre el precio de venta (incluido en el precio mostrado)

### Amazon UK
- **Idioma:** Inglés británico (colour, centre, tyre, analyse, behaviour)
- **Moneda:** GBP
- **VAT:** 20%

### Amazon US
- **Idioma:** Inglés americano (color, center, tire, analyze, behavior)
- **Moneda:** USD
- **Competencia:** Máxima — diferenciación crítica

## Auditoría de Listing

Antes de optimizar, ejecutar scored audit:

```python
audit_criteria = {
    "titulo_keywords": "¿La keyword principal está en primeros 80 caracteres?",
    "titulo_longitud": "¿Usa 150-200 caracteres?",
    "imagen_principal_compliance": "¿Fondo blanco puro, 1000px+, sin texto?",
    "cantidad_imagenes": "¿Usa 7+ slots de imagen?",
    "bullets_beneficio": "¿Cada bullet empieza con beneficio, no feature?",
    "backend_keywords": "¿250 bytes usados con términos únicos?",
    "a_plus_content": "¿Tiene A+ Content si es Brand Registry?",
    "precio_competitivo": "¿Está en rango de mercado?",
    "reseñas_suficientes": "¿20+ reseñas?",
}
```

## Referencias

- `references/amazon-image-requirements.md` — Especificaciones técnicas detalladas de imágenes
- `references/a-plus-video-best-practices.md` — A+ Content módulos, video recomendaciones y secuencia de imágenes
- `references/backend-keywords-guide.md` — Estrategia avanzada de backend search terms
- `references/australia-marketplace-tips.md` — Consideraciones específicas para Amazon AU
- `references/au-flat-file-template.md` — Estructura y API names de la plantilla flat file AU 2026 + mapeo de cabeceras CSV (PET_TOY) verificado
- `references/au-listing-validation.md` — Fuentes de verdad (Drive/proforma), constraints de campos, riesgo DAFF, análisis de imágenes de catálogo, playbook para próximo producto
- `scripts/validate_listing_limits.py` — valida item_name ≤200, bullets ≤500, descripción ≤2000, generic_keywords ≤250 bytes en cualquier sheet de listings

## Pitfalls Comunes

- ❌ **Concluir que el listing no existe sin listar la carpeta Drive** — el contenido local (brain/raw) puede ser de un producto previo; la carpeta Drive del listing es la fuente de verdad. Listarla con `drive_list.py` antes de afirmar que falta contenido.
- ❌ **Confiar en títulos/bullets del doc fuente sin validar longitud** — títulos sobre 200 (221/227/216 en el Listing v2 real) y **backend keywords sobre 250 bytes** (313/293/314). Validar SIEMPRE con `scripts/validate_listing_limits.py` aunque vengan de un doc "completo".
- ❌ **No cruzar el listing contra la proforma invoice** — accesorios y materiales se confirman en la proforma, no en el copy. Material orgánico (cotton/wool) en AU = riesgo DAFF/BICON aunque el listing diga "100% sintético".
- ❌ **Aceptar accesorios del copy sin ver imagen/proforma** — la bola squeaky del PS-3052 NO se veía en el catálogo; el PS-3058 mostraba tema jardín (4 maceteros) vs "5 zanahorias" del título. Confirmar con proveedor antes de publicar claims.
- ❌ **Dejar logos del proveedor en la imagen principal** — PS-3052 tenía "B13" cosido en la rosa. Amazon rechaza logos ajenos (conflicto con la brand propia); retirarlos en edición.
- ❌ **No actualizar claims cuando el proveedor mejora el producto** — base antideslizante mejorada por quejas de clientes → actualizar bullets a "ENHANCED NON-SLIP" en todos los ASINs.
- ❌ **Leer el tab Template del xlsx flat-file** — contiene blobs base64 de settings; preferir la exportación CSV.
- ❌ **Buscar specs de imágenes en PDFs de auditoría estratégica** — PDFs como *Busqueda_Producto_Ganador_Amazon_Australia.pdf* cubren viabilidad de producto, logística, y rentabilidad. NO contienen specs de imágenes de listing. Las image requirements están en `references/amazon-image-requirements.md` y en la sección 2 de este SKILL.md.
- ❌ **No verificar compliance de imagen principal** — La causa #1 de supresión de listings. Una imagen no-compliant hace invisibles todas las demás optimizaciones.
- ❌ **Copiar listings entre marketplaces sin localizar** — Un listing en AU necesita inglés australiano, no copia de US.
- ❌ **Poner keywords de backend que ya están en el título** — Desperdicia los 250 bytes.
- ❌ **No tener estrategia de reseñas antes de lanzar** — Zero reviews mata cualquier conversión.
- ❌ **Cambiar título, imágenes y precio todo a la vez** — No sabrás qué funcionó.
- ❌ **Ignorar el factor móvil** — Más del 70% del tráfico de Amazon es mobile. Los primeros 70-80 caracteres de cada elemento son los únicos asegurados.
- ✅ **Siempre verificar el listing en mobile antes de publicar.**
- ✅ **Siempre calcular break-even con FBA fees actualizados del marketplace destino.**
- ✅ **Siempre incluir palabras clave de temporada/localización en backend.**