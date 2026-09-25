---
name: ai-video-model-costing
description: "Use when choosing or pricing an AI video model."
tags: [video-ia, costos, precios, reels, hailuo, minimax, presupuesto, monid]
---

# AI Video Model Costing & Selection

## Cuándo usar
- El usuario pregunta qué modelo/proveedor de video IA conviene (costo-beneficio) para reels, video-ai-generator o clientes.
- Hay que presupuestar un reel o proyecto de video (costo por clip y por reel 30s).
- Los precios cambiaron o hay que re-verificar la hoja de precios antes de decidir.

## Hoja de precios verificada (18/08/2026)
Detalle completo con fuentes: `references/video-model-pricing-2026-08.md`.

| Ruta | Precio clip 6s | Reel 30s (5 clips) |
|---|---|---|
| **Hailuo-2.3 768P vía Monid — DEFAULT producción** | $0.28 | **$1.40** |
| Hailuo-2.3-Fast 768P (drafts) | $0.19 | $0.95 |
| H3 768P (API MiniMax directa, premium, audio nativo) | $0.48 | $2.40 |
| Seedance 2.0 Mini 720p (fallback) | $0.38 (5s) | $2.29 |

## Decisión por nivel
1. **Producción estándar** → Hailuo-2.3 768P 6s vía Monid ($0.28/clip). Mismo precio que API directa; ya integrado (MONID_API_KEY en el repo).
2. **Drafts/validación** → Hailuo-2.3-Fast 768P ($0.19/clip) o draft Three.js gratis.
3. **Premium / brief que lo pida** → H3 768P API directa ($0.48/clip): última generación, #2 mundial t2v (Elo 1242), audio nativo (SFX gratis). Abrir cuenta MiniMax solo para H3.
4. **Largo plazo** → H3 tiene open weights: cluster local 96GB VRAM ≈ costo eléctrico.

## Re-verificación de precios (los precios cambian)
- Fuente canónica MiniMax paygo: `https://platform.minimax.io/docs/guides/pricing-paygo` vía `curl https://r.jina.ai/<url>` (funciona, es SSR).
- Monid: `https://monid.ai/tools/minimax` (SSR, extraíble con Jina). **app.monid.ai es SPA Nuxt — Jina solo devuelve "Loading"**, no pierdas tiempo ahí.
- Búsqueda: Exa directo por curl (fallback cuando mcporter no está instalado):
  `curl -s https://api.exa.ai/search -H "x-api-key: $EXA_API_KEY" -H "Content-Type: application/json" -d '{"query":"...","numResults":5}'`
  (`EXA_API_KEY` en el `.env` — ruta: /opt/data/.env en gateway, /root/hermes-agent/data/.env en desktop).

## Pitfalls
- **Token plan MiniMax ($20/$50/$120 mes): NO cubre video** — solo texto/imagen/voz/música. Nunca recomendarlo para video.
- **Video packages MiniMax: desde $1,000/mes** y **H3 no está soportado**. Punto de equilibrio ≈ 3,760 clips/mes. Descartados para nuestro volumen.
- **OpenRouter Hailuo-2.3 = $0.0817/s** → 6s = $0.49 = 75% markup vs $0.28 directo. Evitar para video.
- Monid **no agrega markup** en Hailuo-2.3 (mismo precio que API directa) — es pura conveniencia de balance.
- Con Hailuo-2.3, **6s es más barato por segundo que 10s** ($0.047/s vs $0.056/s); con H3 el precio/s es plano ($0.08) — la duración del clip da igual.
- No asumir que H3 existe en Monid: la página pública lista solo Hailuo-2.3; verificar antes de prometer.
- Precios listados por el usuario en chats pueden ser de la API oficial, no de Monid — siempre distinguir la fuente antes de comparar.

## Referencias
- `references/video-model-pricing-2026-08.md` — hoja completa verificada: tablas paygo MiniMax, paquetes, token plan, Monid, OpenRouter, costos por reel y fuentes con fecha.
