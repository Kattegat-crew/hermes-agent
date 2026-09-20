# OpenCode-Go API — endpoint, modelos, escaneo gratuito (verificado 26/08/2026)

Provider OpenAI-compatible de OpenCode Go, añadido como tercer fallback de API.

## Datos clave

- **Endpoint base**: `https://opencode.ai/zen/go/v1`
- **Listar modelos**: `GET /zen/go/v1/models` (bearer key)
- **Chat**: `POST /zen/go/v1/chat/completions`
- **Auth**: `Authorization: Bearer <key>`
- **User-Agent**: algunas rutas devuelven 403 con urllib/python por defecto; usar
  `User-Agent: Mozilla/5.0`.

## ⚠️ IDs de modelo: SIN prefijo en la API

El wrapper de la CLI usa tags tipo `opencode/mimo-v2.5`, pero la **API** exige el
ID pelado:

- ✅ `"model": "mimo-v2.5"` → responde
- ❌ `"model": "opencode/mimo-v2.5"` → `401 Model ... is not supported`

Lección (costo real): el wrapper de fallback se creó con `DEFAULT_MODEL =
"opencode/mimo-v2.5"` y falló 401; corregido a `mimo-v2.5`. Al añadir un provider
OpenAI-compatible, usar el `id` del GET /models, no el tag "humano".

## Escaneo de modelos gratuitos (cost=0)

El GET /models lista muchos (`minimax-m3`, `kimi-k3`, `kimi-k2.7-code`, `qwen3.8-max`,
`glm-5.3`, `deepseek-v4-flash`, `hy3`, etc.). No todos responden vía chat/completions.
Probar cada id con `max_tokens: 3` y leer el campo `cost`:

```bash
curl -s -H "Authorization: Bearer $KEY" -H "User-Agent: Mozilla/5.0" -H "Content-Type: application/json" \
  -d '{"model":"mimo-v2.5","messages":[{"role":"user","content":"hola"}],"max_tokens":3}' \
  https://opencode.ai/zen/go/v1/chat/completions
```

- `"cost": "0"` → gratis (cubre la sub OpenCode Go).
- Errores típicos por modelo: `Unsupported model`, `Model is unavailable`,
  `Endpoint is unavailable`, `not supported for format oa-compat` (grok), 500
  transitorios. Un modelo que da 500/unsupported hoy puede no estar aún en el
  bucket de chat o requerir otro formato — no marcar el proveedor como roto.

## Notas de operación

- Key en texto plano en un chat de grupo NO es seguro → rotar; guardar solo en
  `.env`/config del perfil, nunca en scripts/wrapper.
- Como tercer fallback (después de NaN y B.AI), darle un solo modelo útil
  (mimo-v2.5, context 1M, 30‑100 llamadas/mes gratis, cost=0) para no ampliar
  el catálogo innecesariamente.