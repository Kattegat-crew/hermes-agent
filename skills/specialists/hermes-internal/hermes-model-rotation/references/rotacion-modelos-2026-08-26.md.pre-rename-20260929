# Rotación de modelos 26/08/2026 — qwen3.8-flash / glm5.3-flash

Bitácora de evidencia de la rotación usada para validar `scripts/rotate_model_yaml.py`.

## Contexto
Dashboard NaN Cloud mostró nuevos modelos (Qwen 3.8 Flash, GLM 5.3) y cuota de DeepSeek
V4-Flash al 1.6B/2.0B (~80%). Jonathan pidió rotar Ragnar/Roshi/Bob a GLM 5.3 y los de
producción a Qwen 3.8.

## Descubrimiento de modelos (GET /v1/models)
Con key + UA de navegador (NaN exige UA o 403/1010). Devuelve SOLO ids:
`deepseek-v4-flash, qwen3.6, qwen3.8-flash, mimo-v2.5, gemma4, glm5.3-flash, flux-2-klein,
kokoro, whisper, qwen3-embedding, rerank`. Sin context_length (los specs vienen del dashboard).

## Smoke de disponibilidad (clave)
`glm5.3-flash` → **401 `{"error":{"message":"Missing Authentication header"}}`** en 3/3 intentos,
con la MISMA key que `qwen3.8-flash`/`qwen3.6`/`deepseek-v4-flash` responden 200. Conclusión:
listado en API ≠ habilitado en el plan. No es problema de key/URL. Acción = habilitar en el
dashboard cloud.nan.builders (mismo fenómeno que GLM "NOT IN YOUR PLAN" que ya se veía).

## Fallo del método naive (lección)
Un primer script editó `config.yaml` por regex/strings y produjo:
`default: qwen3.8-flashdeepseek-v4-flash` (REPLACED sin separador, YAML roto) + catálogo con
indentación rota. Se restauró desde backup. Lección: NUNCA editar YAML de config por strings;
usar dict (safe_load → mutate → safe_dump → validar → backup → write).

## Matriz aplicada (método seguro)
- Local: Ragnar (default) → qwen3.8-flash; Roshi → qwen3.8-flash; especialistas bragi, comms,
  freyja, heimdall, hermodr, sindri, ullr, vili → qwen3.8-flash.
- Mantenidos: brokkr → deepseek-v4-flash (1M ctx para código/repos), vigia → gemma4 (ligero).
- Prod (169.58.189.222): Bob (default), helmer, jacqueline, nancy, neural-admin-test, yulieth → qwen3.8-flash.
- glm5.3-flash registrado en catálogo (ctx 131072) pero NO asignado (no habilitado).

## Estructura de PROD (quirk)
- `/opt/data/` es el home de prod (NO /root/hermes-agent/data).
- `model` usa `provider: custom` + `base_url: http://hermes-llm-proxy:8742/v1` (nginx, no
  filtra modelos) + `fallback_providers` (mimo-v2.5 opencode zen + qwen3.6).
- **NO existe `custom_providers`** en prod → un chequeo `custom=False` es esperado y correcto;
  basta con sync de `providers.NaN-Builders.models` + rotar `model.default`.

## Verificación post-rotación
- Por perfil: `yaml.safe_load` OK + `model.default` exacto + `qwen3.8-flash` presente en
  `providers.NaN-Builders.models` (y en custom donde exista).
- Smoke real: `hermes chat -q "Responde solo: ROTADO"` → leer la respuesta desde **state.db**
  (las sesiones viven en state.db, no en sessions/*.jsonl):
  ```python
  sqlite3.connect('/opt/data/state.db')
  # SELECT id FROM sessions ORDER BY rowid DESC LIMIT 3
  # SELECT role,content FROM messages WHERE session_id=? AND role='assistant' ...
  ```
  Respuesta observada para la sesión del smoke: "ROTADO".

## Backups
Cada config local/prod respaldado antes de rotar (`...-pre-qwen38.yaml` / `config.yaml.bak-<ts>`).