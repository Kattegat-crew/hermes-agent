---
name: vendor-pricing-research
description: Use when comparing live API/model pricing across providers.
---

# Vendor Pricing Research (APIs / modelos / brokers)

## Cuándo usar
- Necesitas precios REALES actualizados de proveedores de API (video, imagen, LLM, brokers) para comparar costos por clip, por token o por segundo.
- No hay base de precios interna o la hoja quedó vieja y hay que re-verificar contra las páginas oficiales.
- Los típicos `web_search` / `web_extract` no están configurados (falta FIRECRAWL key) y hay que llegar por otra vía.

## Método (de preferido a fallback)
1. **curl directo con UA de navegador** a la página de precios. Funciona si la página es SSR/HTML plano:
   `curl -sL --max-time 25 "<url>" -H "User-Agent: Mozilla/5.0 ... Chrome/120.0"`
   Limpiar HTML con `sed 's/<[^>]*>//g'` y filtrar por regex del precio.
2. **Browser CDP para páginas JS** (Next.js/SPA tipo `siliconflow.cn/pricing`, `volcengine`, `alibabacloud.com`): `browser_navigate` y extraer con `browser_console` → leer `document.body.innerText` y recortar con `.slice()` en torno a la sección buscada, o clicar pestañas (p.ej. Together: pricing divide en tabs CHAT/VISION/IMAGE/AUDIO/VIDEO/…).
   - No vuelques toda la página: las páginas de precio son gigantes (miles de elementos); extrae solo el slice del nombre de modelo buscado.
3. **Buscadores**: Bing y DuckDuckGo por `curl` bloquean con CAPTCHA/vacío. DDG **funciona vía browser_navigate** (`https://duckduckgo.com/?q=...`). Útil para localizar el doc canónico (p.ej. `wan 计费 元/秒`).
4. **Aliyun**: los enlaces `help.aliyun.com/zh/...` dan 404/redirigen. La web **internacional** `www.alibabacloud.com/help/en/model-studio/model-pricing` SÍ carga y tiene tabla completa. Generaliza: ante páginas chinas rotas, probar el canto internacional.

## Trampa de modelo de facturación (CRÍTICO)
Los proveedores cobran el video/inferencia de formas distintas — SIEMPRE normaliza antes de comparar:
- **Flat por generación**: p.ej. SiliconFlow Wan2.2 = ¥2.00/video, sin importar duración. Para clips más largos que una generación, multiplica (¿2 generaciones + unión?).
- **Por segundo de salida**: p.ej. Alibaba Model Studio `wan` = $/s de video generado, `Coste = precio/s × duración`.
- **Por token**: p.ej. Volcengine seedance, `precio = token单价 × tokens` con `tokens = (duración) × W × H × fps / 1024`.
- **"Lowest setting" trampa**: varias páginas (Together) muestran el ajuste mínimo (resolución/duración mínima) y el real para 720p/6s puede subir.

## Entrega
- Tabla Markdown `Proveedor | Modelo | $/clip | Audio nativo | Verificado/Estimado | Notas`.
- Cerrar con el proveedor más barato del grupo y una estimación para el volumen pedido (p.ej. ×5 clips).
- Marcar **✅ Verificado** (precio de tabla oficial) vs **⚠️ Estimado** (lowest setting, promo, GPU/sec, no encontrado). Nunca inventar el número.

## Referencias
- `references/ai-video-asian-brokers-2026-08.md` — precios verificados 19/08/2026 de SiliconFlow, Kluster (FUERA), Together, Volcengine seedance, Alibaba Model Studio wan. Datos por $/clip 6s 720p I2V.
- `references/fal-models-discovery-2026-08.md` — catálogo de modelos **audio/TTS y video de fal.ai** (ElevenLabs, MiniMax, Qwen3-TTS, etc.) + patrón de PROBE de endpoint a costo CERO sin key ni saldo.

## Catálogo y probe sin gastar (fal.ai, 19/08/2026)
- **La página de un modelo de fal es una SPA (JS)** — el schema NO está en el HTML plano (no saquees la página del modelo con curl). Pero el **catálogo** SÍ expone los IDs en HTML: `curl "https://fal.ai/models?view=audio"` y `re.findall(r'href="(/models/[^"#]+?)"')` devuelve todos los endpoints de la categoría.
- **Probe de existencia del endpoint SIN costo ni key**: haz `POST https://queue.fal.run/<model-id>` con header `Authorization: Key invalid_test_only` y cuerpo mínimo. **401 = el endpoint existe** (la ruta es válida, solo falla la auth → cero gasto, cero generación). **404 = no existe** (o el ID está mal). Esto permite confirmar el modelo correcto antes de gastar.
- **Elegir voz TTS sin créditos**: los demos web propios del proveedor (MiniMax speech demo, ElevenLabs https://elevenlabs.io/text-to-speech) aceptan texto libre gratis — para validar pronunciación (nombres propios, ciudades) pegar el guión completo del reel; no genera en fal ni toca la key del broker. ElevenLabs expone voces premade vía `GET https://api.elevenlabs.io/v1/voices`.
- **No confiar en el precio listado de fal para TTS**: fal cobra por tokens; la tarifa por 6s de una generación NO es directamente el $/clip de voz. Validar contra el dashboard del usuario tras 1 run real (regla dura: los costos de subagente se confirman con el proveedor, no se estiman).

## Pitfalls
- **Verifica que el servicio siga vivo**: los brokers del segmento desaparecen rápido. p.ej. Kluster.ai fue adquirido por MITO y suspendió servicios el 9/jun/2026. No propongas un broker sin confirmar status (title/meta "joined X" o redirect).
- **Moneda**: sé explícito con el tipo de cambio USD↔CNY (≈7.1) al convertir ¥ a $.
- No asumas que un modelo existe en un proveedor; verifica en la lista pública (p.ej. no todo broker hostea Wan2.7; algunos solo Wan2.2).
- Un 404 en el sitio china de precios no significa que no exista el modelo/percio; usa el doc canónico internacional + buscador.