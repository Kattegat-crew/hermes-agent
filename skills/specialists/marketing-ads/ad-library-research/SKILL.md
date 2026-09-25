---
name: ad-library-research
description: "Use when researching Meta Ad Library competitor ads."
tags: [ads, meta, ad-library, scraping, competencia, creativos, research]
metadata:
  hermes:
    tags: [research, ads, meta, competencia, creativos]
    category: marketing
---

# Meta Ad Library Research (sin API, sin login)

La interfaz web de facebook.com/ads/library es pública y scrapeable; la Marketing API
solo cubre ads sociales/políticos/UE — los ads comerciales (casinos, retail) NO están
en la API. Este skill cubre la mina de estructuras para story-ads: un copy activo hace
500 días = estructura probada.

## Cuándo usar

- Armar el corto-lista F1 de la metodología story-ad (antes de escribir spines).
- Benchmark de creativos de competencia directa o análoga (online/local).
- Sembrar una vault/KB de referencias publicitarias (marketing-campaign-generator: `scripts/ad_kb.py`).

## Cómo

1. URL directa con params (funciona sin sesión):
   `https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=CO&q=<termino>&search_type=keyword_unordered`
2. Cosechar con `browser_exec` (ver `scripts/harvest_ad_library.py` — pegar su cuerpo
   como código): scroll progresivo ×10 con `window.scrollBy` (lazy-load), leer
   `document.body.innerText` por chunk y parsear bloques separados por `Activo\n`:
   - `Identificador de la biblioteca: (\d+)` → lib_id (clave de dedupe)
   - `En circulación desde el ([^\n]+)` → fecha → días activo (señal #1)
   - `\n([^\n]{2,60})\nPublicidad\n` → anunciante
   - copy: lo que sigue a 'Publicidad' hasta la primera URL/dominio en mayúsculas
3. Ordenar por días activo descendente; filtrar por relevancia (dict anunciante→por-qué);
   dedupe por lib_id.
4. Semáforo: longevo (>=90d) o >=5 variantes = estructura probada; ads jóvenes
   (9-15d) = rotación agresiva de creativos (leer patrones, no longevidad).
5. Sembrar la KB con `source_url = .../ads/library/?id=<lib_id>` (enlace permanente verificable).

## Pitfalls

- **browser_exec `session`**: pasar un nombre de sesión a la primera llamada navega la
  pestaña a un daemon distinto y las llamadas siguientes fallan con 'Session with given
  id not found'. Abrir en la default, o reusar SIEMPRE el mismo nombre; `ensure_real_tab()`
  recupera una pestaña huérfana.
- innerText tiene duplicados por scroll (chunks solapados) — dedupe por lib_id, no por texto.
- 'Publicidad' aparece también en UI chrome; exigir el patrón línea-adjacente del paso 2.
- `country=CO` filtra por audiencia dirigida, no por empresa — salen casinos US
  (DraftKings/Choctaw) que pujan por hispanos; filtrar por anunciante con criterio explícito.
- Fechas en español ('31 ago 2026') → mapear meses ES; `days_running` calculado contra
  la fecha de hoy (no hardcodear).

## Verificación

El conteo de ads únicos parseados debe cuadrar con lo visible en página; abrir 2-3
lib_ids al azar y confirmar que el copy coincide.

## Soporte

- `scripts/harvest_ad_library.py` — cuerpo listo para pegar en browser_exec (scroll + parse + dedupe + ranking).
