# Amazon Backend Keywords — Estrategia Avanzada

Los backend search terms (términos genéricos) son el campo oculto que
Amazon indexa para ampliar la cobertura de búsqueda de tu listing.

## Especificaciones Técnicas

| Parámetro | Valor |
|-----------|-------|
| Límite | 250 **bytes** (NO caracteres) |
| Separador | Espacio simple (sin comas) |
| Indexado | Sí, por A9 y por los modelos de IA (Rufus/COSMO) |
| Visible al comprador | No |
| Idioma | Del marketplace (cada marketplace indexa su idioma) |

**⚠️ Bytes vs Caracteres:** Un carácter ASCII = 1 byte. Caracteres
acentuados o especiales (á, é, ñ, ü) = 2+ bytes. Los emojis pueden
ocupar 4+ bytes. Un campo de 250 caracteres "parece" lleno pero puede
estar sobre el límite real de 250 bytes.

## Qué Incluir

Solo términos que NO aparecen en el título, bullets ni descripción:

1. **Sinónimos** — términos equivalentes usados por otros compradores
2. **Misspellings comunes** — "snufle", "snuffel", "sniffel mat"
3. **Variantes long-tail** — frases de 3-4 palabras más específicas
4. **Singular/plural** — "dog mat" + "dog mats" (solo si no está en título)
5. **Términos de uso/compatibilidad** — "for small dogs", "for puppies"
6. **Traducciones** — para productos que cruzan mercados (solo en listing internacional)
7. **Términos estacionales** — "christmas gift", "birthday gift"
8. **Ortografía local** — "colour" (AU/UK), "center" (US) — cuando aplica

## Qué NO Incluir

- ❌ **Palabras ya en el título** — desperdicia bytes, zero beneficio
- ❌ **Nombre de tu marca** — ya está en el título
- ❌ **Nombres de competidores** — viola políticas de Amazon
- ❌ **ASINs** — no son search terms
- ❌ **Otras marcas** — riesgo de suspensión
- ❌ **Términos irrelevantes** — Amazon penaliza keywords no relacionadas
- ❌ **Comas, puntos, símbolos** — solo espacios
- ❌ **Palabras de más de 50 caracteres** — Amazon las ignora

## Técnica de Maximización

```
Paso 1: Extraer keywords del Search Term Report de PPC
Paso 2: Identificar cuáles generan clics/ventas y NO están en el título
Paso 3: Ordenar por volumen de búsqueda (mayor primero)
Paso 4: Rellenar 250 bytes SIN comas ni repeticiones
Paso 5: Verificar byte count (Python: len(term.encode('utf-8')))
```

## Verificación de Bytes

```python
def check_backend_bytes(keywords_str):
    """Verifica que los backend keywords no excedan 250 bytes."""
    byte_count = len(keywords_str.encode('utf-8'))
    print(f"Bytes usados: {byte_count}/250")
    if byte_count > 250:
        print("⚠️ EXCEDE EL LÍMITE — recortar o eliminar caracteres especiales")
    else:
        print("✅ OK")
    return byte_count
```

## Impacto Actual (2025-2026)

El backend keywords **sigue siendo señal de ranking activa**. Además,
los modelos de IA de Amazon (Rufus) consultan estos campos para
responder preguntas de compradores. Un backend bien trabajado:
- Amplía cobertura en búsquedas long-tail
- Mejora matching en búsquedas por voz y conversacionales
- No afecta la experiencia visual del comprador (es invisible)

**Nota:** Aunque su peso relativo ha bajado vs el CTR/conversión,
sigue siendo la forma más barata de ganar relevancia adicional.