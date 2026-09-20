---
name: ai-video-pricing-research
description: Video clip (6s) prices on fal.ai and Replicate via curl.
---

# AI Video Pricing Research (fal.ai + Replicate + más)

## Cuándo usar
- El usuario pregunta/cuestiona CUÁNTO cuesta un clip de video IA (image-to-video, 6s, 720p, 9:16) en fal.ai, Replicate u otros agregadores, para comparar rutas o presupuestar reels (5 clips / 30s).
- Hay que re-verificar precios que cambian (han cambiado varias veces en 2026).

## Regla de oro: sacar el precio del sitio, no de memoria
Los precios públicos cambian y cada proveedor cotiza distinto (por **video**, por **segundo de salida**, por **segundo de runtime**). NO usar cifras recordadas ni adivinadas como "verificadas": obtener el chip/billing de la página oficial con curl y marcar en la tabla qué es VERIFICADO vs ESTIMADO. Distinguir SIEMPRE el `billing_unit` del modelo que cotiza.

## Método fal.ai (curl, sin token)
1. Catálogo de slugs reales: `curl -s "https://fal.ai/api/models?page=N"` → JSON `items[].id` + `category`. Filtra `category=="image-to-video"`. **NO adivinar slugs**: los tipo `fal-ai/wan/v2.1-14b/image-to-video` suelen 404; el real puede ser `fal-ai/wan-i2v`, `fal-ai/veo3.1/image-to-video`, etc.
2. Página `https://fal.ai/models/<slug>` → blob `endpointBilling` en __NEXT_DATA__: `"billing_unit":"seconds"|"videos"` + `"price":N`. El chip "[...]will cost $X per [video|second]" es autoritativo.
3. Pitfall scraping: __NEXT_DATA__ llega con `\\\"` anidado. Normalizar con `h=h.replace("\\","")` y luego
   `re.findall(r'"billing_unit":"([a-z]+)","price":(\d+\.?\d*)', d)` y `re.findall(r'will cost.*?\$(\d+\.?\d*)', d, re.S)`.

## Método Replicate (verificado, sin token)
- Slugs: `curl -s https://replicate.com/collections/image-to-video` y `.../text-to-video` → grep `href="/owner/model"` (SSR, sale con curl).
- Por página `https://replicate.com/<slug>`: el chip autoritativo es el unit-output tipo `"description": "N seconds for $X"` / `"N videos for $X"`, o los `"title":"per second of output video","price":"$X"`.
- PITFALL: `"p50price"` es LEGACY (precio por segundo de cómputo interno) — **NO es lo que se factura**. Basarse en los chips por-unidad, no en p50.
  Replicate 2026 factura por segundo de salida (wan/kling/seedance) y algunos por video (minimax/video-01 = "20 videos por $10").

## Cómo calcular clip 6s
- Por-video → precio directo.
- Por-segundo → multiplicar por 6 (menos si el modelo cap duración distinta).
- Por-runtime (p. ej. tencent/hunyuan-video en Replicate) → coste depende de latencia; marcar ESTIMADO.
- Verificar audio nativo por modelo (Seedance soporta voz/diálogo; Wan/Hunyuan/LTX mudos; Veo 3.1 lleva audio).

## Datos de precios verificados (19/08/2026)
Hoja completa + números reales: `references/fal-replicate-pricing-2026-08.md`.
Destacados: fal.ai `wan-i2v` $0.40/clip 6s; `wan/v2.2-a14b` $0.48; `ltx-2.3/fast` $0.36;
Replicate `wan-2.1-i2v-720p` $1.50 (caro), `wan-2.1-i2v-480p` $0.54.
Insight clave: fal.ai `seedance-2.0/mini` ≈ $0.067/clip, ~7× más barato que Monid ($0.45675). **VERIFICAR con run de prueba antes de reemplazar un pipeline** (precio sospechosamente bajo).

## Entrega
- Tabla: | Proveedor+Modelo | $/clip 6s | Audio nativo | Verificado/Estimado | Notas |
- Terminar: más barato de calidad decente + total estimado para 5 clips.

## Referencias
- `references/fal-replicate-pricing-2026-08.md` — snapshot completo de precios fal.ai + Replicate con método de extracción y tablas.