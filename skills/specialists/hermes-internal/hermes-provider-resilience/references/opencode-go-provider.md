# OpenCode Go — Provider OpenAI-compatible (integrado y escaneado 26/08/2026)

OpenCode Go es la API de la suscripción OpenCode (`opencode.ai`). Sirve como
provider LLM OpenAI-compatible en Hermes y como capa de fallback de ejecución.
La mayoría de modelos responden con `cost: "0"` (la sub cubre el usage).

## Endpoint / Auth

- **Base URL:** `https://opencode.ai/zen/go/v1`
- **Auth:** `Authorization: Bearer sk-...` (OpenAI-compatible)
- Lista modelos: `GET {base}/models` → `data[].id`
- Chat: `POST {base}/chat/completions` — body OpenAI estándar; respuesta incluye
  campo `cost` (string). `"0"` = cubierto por la sub.

## ⚠️ WAF bloquea urllib (probado 26/08)

- `urllib.request.urlopen(..., headers={"Authorization": ...})` → **HTTP 403 Forbidden**
  (bloqueo por User-Agent de Python).
- `curl` con `User-Agent: Mozilla/5.0` → **200 OK**.
- **Fix:** añadir siempre `User-Agent: Mozilla/5.0`. Aplica a `/models` y a los
  probes de chat. Caso general: skill `ua-spoofing-eval`.

## Catálogo de modelos — escaneado en vivo (24 de 31 con cost=0)

**DeepSeek:** deepseek-v4-flash, deepseek-v4-pro, deepseek-v4-flash-vision-exp
**Qwen:** qwen3.8-max, qwen3.7-max, qwen3.7-plus, qwen3.6-plus, qwen3.5-plus
**GLM:** glm-5.3, glm-5.3-flash, glm-5.2, glm-5.1, glm-5
**Kimi:** kimi-k3, kimi-k2.7-code, kimi-k2.6, kimi-k2.5, longcat-2.0
**MiniMax:** minimax-m3, minimax-m2.5
**MiMo:** mimo-v2.5, mimo-v2.5-pro
**Hy3:** hy3

**No usables / transitorio (26/08), revalidar si cambia la plataforma:**
minimax-m2.7 (500), mimo-v2-pro y mimo-v2-omni (400 Unsupported model),
hy3-preview (Unavailable), gpt-5.6-luna y muse-spark-1.2-contributor (500),
grok-4.5 (endpoint unavailable), grok-4.6 (no soporta formato oa-compat).

## Bloque `providers.OpenCode-Go` (config.yaml de Ragnar/gateway)

```yaml
OpenCode-Go:
    api_key: sk-<KEY_DIRECTO_DE_JONATHAN>
    base_url: https://opencode.ai/zen/go/v1
    models:
      deepseek-v4-flash:            {context_length: 1048576, name: DeepSeek V4 Flash (Go)}
      deepseek-v4-pro:              {context_length: 65536,    name: DeepSeek V4 Pro (Go)}
      deepseek-v4-flash-vision-exp: {context_length: 1048576, name: DeepSeek V4 Flash Vision (Go)}
      mimo-v2.5:                    {context_length: 1048576, name: MiMo V2.5 (Go)}
      mimo-v2.5-pro:                {context_length: 1048576, name: MiMo V2.5 Pro (Go)}
      qwen3.8-max / qwen3.7-max / qwen3.7-plus / qwen3.6-plus / qwen3.5-plus: {context_length: 262144}
      glm-5.3 / glm-5.3-flash / glm-5.2 / glm-5.1 / glm-5: {context_length: 131072}
      kimi-k3 / kimi-k2.7-code / kimi-k2.6 / kimi-k2.5 / longcat-2.0: {context_length: 131072}
      minimax-m3 / minimax-m2.5 / hy3: {context_length: 131072}
```

- La key NUNCA en memoria ni en logs — solo en config.yaml (el usuario la provee).
- El modelo activo de Ragnar quedó intacto (NaN-Builders / deepseek-v4-flash);
  OpenCode-Go queda disponible como provider y como fallback.

## Merge atómico multi-modelo (evita 23 llamadas a manage_provider.py)

`manage_provider.py add` agrega UN modelo por invocación. Para un catálogo grande
usar merge yaml con backup:

```bash
cd /opt/data && python3 - <<'EOF'
import yaml, shutil, time
shutil.copy2("config.yaml", f"config.yaml.bak-provider-{time.strftime('%Y%m%d-%H%M%S')}")
cfg = yaml.safe_load(open("config.yaml")) or {}
cfg.setdefault("providers", {})["OpenCode-Go"] = {
    "api_key": "sk-...", "base_url": "https://opencode.ai/zen/go/v1",
    "models": {mid: {"context_length": ctx, "name": name} for mid, (ctx, name) in MODELS.items()},
}
yaml.dump(cfg, open("config.yaml", "w"), default_flow_style=False, allow_unicode=True, sort_keys=False)
EOF
```

⚠️ `yaml.safe_load` + `yaml.dump` **pierde comentarios** del config. El método
string-replace (documentado en la skill `hermes-provider-configuration`, user-owned)
preserva comentarios; el merge yaml.dump solo se usa aceptando esa pérdida y SIEMPRE
con backup previo.

## Verificación

- `GET /models` con UA → 200 y lista.
- Chat probe `max_tokens:3` → `choices[0].message.content` + `cost: "0"`.
- `python3 -c "import yaml; yaml.safe_load(open('config.yaml'))"` tras editar.
- En config: `providers: ['NaN-Builders', 'B.AI', 'OpenCode-Go']`.

## Relación con el resto del stack

- B.AI: `deepseek-v4-flash` responde SIN saldo (free tier); el resto de modelos
  pide depósito (`access_denied: Deposit required`) o quiebra por
  `insufficient_user_quota` (minimax). NO son "varios gratis" hoy — solo
  deepseek-v4-flash.
- OpenCode Go = capa 3 de fallback de ejecución (modelos fuertes cost=0). Wrapper
  `hermes-fallback-opencode` (Roshi) debe apuntar aquí cuando fallan NaN→B.AI, y
  escribir `estado.json` (exit_code, duración, modelo) para el watchdog de Vigía.
- BLOQUEANTE del wrapper: deduplicar la skill `opencode` (2 copias → Ambiguous).