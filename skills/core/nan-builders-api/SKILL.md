---
name: nan-builders-api
description: "NaN Builders API: base URL, auth, Cloudflare UA, images."
tags: [nan-builders, api, llm, imagen, cloudflare, glm, flux, provider]

---

# NaN Builders API

Proveedor de modelos (LLM + imágenes) usado por NeuralCrew. OpenAI-compatible.

## Base URL — CORRECTO vs docs

| | URL |
|---|---|
| ✅ **CORRECTO** | `https://api.nan.builders/v1` |
| ❌ INCORRECTO | `https://api.nan-builders.com/v1` (con guion) |

**El guion rompe todo:** `api.nan-builders.com` NO resuelve DNS. Los docs
(`docs/research/nan-builders-models.md`) tienen la URL equivocada. Fuente de
verdad: `scripts/nan_client.py` (`DEFAULT_BASE_URL = "https://api.nan.builders/v1"`).

## Auth

- Header: `Authorization: Bearer $NAN_API_KEY`
- Key vive en `/opt/data/.env` de Hermes y en `/root/marketing-campaign-generator/.env`.
- Leer en el host: `grep "^NAN_API_KEY=" /root/marketing-campaign-generator/.env | cut -d= -f2`

## Cloudflare — User-Agent obligatorio (PITFALL)

Sin User-Agent de navegador, la API responde **HTTP 403 error code 1010**:

**Fix:**
```python
req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode(),
    headers={
        "Authorization": f"Bearer {nan_key}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
    },
)
```

## Chat: glm5.3-flash (modelo de RAZONAMIENTO) — receta verificada 11-sep-2026

`POST /v1/chat/completions` con `model: "glm5.3-flash"`. **Tres trampas reales:**

1. **Emite su cadena de pensamiento en `delta.reasoning_content`** (no en `content`) y **consume el presupuesto de `max_tokens` razonando antes de escribir la respuesta**.
   - Con `max_tokens: 20` o `8000` en una tarea pesada → `finish_reason: "length"` y **respuesta VACÍA** (todo se fue en razonamiento). Para una revisión/análisis usa `max_tokens: 40000`.
2. **Sin streaming, Cloudflare corta a los 120 s** → `HTTP 524 (Proxy Read Timeout)`. Usa `"stream": true` y `Accept: text/event-stream`: mantiene la conexión viva (178 s sin problema).
3. Acumula **los dos canales por separado** (`reasoning_content` y `content`); guarda el razonamiento aparte para auditoría y quédate con `content` como respuesta.

Error típico: pasar solo stdlib `urllib` con `timeout=900` no evita el 524 — el corte es del proxy, no del socket. **Streaming sí.**

Script de referencia que funcionó (revisor de documentos largos):
`python3 nan_review_stream.py <doc.md> <out.md> 40000` → escribe la respuesta en `out.md` y el razonamiento en `out.reasoning.md`.

**Modelos de chat disponibles (catálogo 11-sep-2026):** `deepseek-v4-flash`, `glm5.3-flash`, `qwen3.6`, `qwen3.8-flash`, `mimo-v2.5`, `minimax-h3`, `gemma4`.

## Imagen: flux-2-klein (text-to-image)

`POST /v1/images/generations` (OpenAI-compatible):

```python
payload = {
    "model": "flux-2-klein",
    "prompt": "<descripción detallada>",
    "n": 1,
    "size": "720x1280",
    "response_format": "b64_json",
}
```

Response: `data[0].b64_json` → base64 → bytes → PNG.

## Ejecución: contenedor Hermes vs contenedores efímeros

| Contenedor | DNS | Funciona |
|---|---|---|
| Hermes (este) | ✅ sí | Llamadas Python directas OK |
| python:3.12-slim | ❌ no | Preferir `--network host` |
| Debian efímero | ❌ no | Usar Hermes container |

## Patron: revision independiente en 3 tajadas paralelas (verificado 11-sep-2026)

Para auditar un repo/trabajo propio con `glm5.3-flash`, no mandes todo en un solo prompt: **divide en 3 revisores que corren en paralelo** (40-50 KB de material cada uno). El modelo NO ejecuta comandos: juzga solo lo que le pegas.

1. **Codigo nuevo**: archivos completos + su contrato + sus tests. Pide bugs reales, FALSOS VERDES (¿puede decir OK con algo malo?), falsos rojos, casos limite y que falta para produccion.
2. **Cadena de gasto / seguridad**: el diff + el modulo del gate completo. Pide "vias de gasto: via -> ¿gate? -> evidencia en el codigo", combinaciones de flags que producen gasto real y tests que faltan.
3. **Claims vs evidencia**: pega la LISTA DE AFIRMACIONES hechas al humano + la EVIDENCIA CRUDA (salidas de comandos, tests, logs). Pide veredicto por afirmacion (sostenida / exagerada / no sostenida / insuficiente) y condiciones para firmar un OK. **Es la tajada que mas incomoda: detecta contradicciones entre lo reportado y la evidencia.**

Runner generico (streaming obligatorio): `python3 /opt/data/scripts/nan_reviewer.py <prompt_con_material.md> <out.md> [max_tokens]`; separa `delta.reasoning_content`, usa `max_tokens >= 20000` y `temperature 0.2`.

**Medido 11-sep-2026:** 3 revisiones en 218/250/112 s con veredictos **5/10, 6/10 y 6,5/10** -> 1 bug CRITICO, 5 ALTO y 13 MEDIO/BAJO que el autor no habia visto. Corregirlos subio la suite de 656 a 660 tests sin fallos reales. Leccion: un revisor sin herramientas encuentra bugs reales por LECTURA si le das el codigo y las afirmaciones.

## Modelos disponibles

- **Chat:** deepseek-v4-flash, qwen3.6, mimo-v2.5, gemma4
- **Imagen:** flux-2-klein, flux
- **TTS:** kokoro (⚠️ 500 en español — usar edge-tts)
- **STT:** whisper
- **Embeddings:** qwen3-embedding, rerank