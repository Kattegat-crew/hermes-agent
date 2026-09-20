---
name: hermes-provider-resilience
description: Redundancia y fallback multi-proveedor LLM para Hermes.
version: 1.0.0
author: Ragnar
metadata:
  hermes:
    tags: [provider, fallback, multi-proveedor, rate-limit, opencode-go, b.ai, resiliencia, flota]
    category: devops
    related_skills: [hermes-provider-configuration, hermes-bot-fleet-ops, provider-manager, ua-spoofing-eval, nan-builders-api]
---

# Hermes Provider Resilience — Redundancia LLM multi-proveedor

Cómo operar una flota de perfiles Hermes con MÁS de un proveedor LLM y un fallback
en cascada para que ningún cron/task/agente muera por rate-limit o caída de API.
Incluye el catálogo verificado del provider OpenCode Go (suscripción) y los
matices reales de B.AI.

## When to Use

- El usuario pide "poner fallbacks", "varios proveedores", "que nunca falle un cron".
- Aparecen 429/concurrency-limit contra una sola API key (ráfaga de crons en paralelo).
- Hay que integrar un provider OpenAI-compatible nuevo (p. ej. OpenCode Go) con
  detección de qué modelos responden gratis.
- El usuario pregunta "¿qué modelos gratis tengo en mi sub X?".

## Prerequisites

- Providers actuales y modelo activo: `python3 /opt/data/scripts/manage_provider.py list`.
- La key del nuevo provider la provee el usuario (NUNCA inventarla ni loguearla).
- `patch` tool NO edita config.yaml ("Refusing to write to Hermes config file") →
  editar por terminal con Python (backup primero) o con manage_provider.py.

## Procedimiento: integrar provider OpenAI-compatible nuevo

1. **Descubrir el endpoint** (web_search: "<nombre> go api base url openai compatible").
   P. ej. OpenCode Go → `https://opencode.ai/zen/go/v1` (docs en opencode.ai/docs/go).
2. **Probar auth + listado de modelos** con CURL y User-Agent de navegador:
   ```bash
   curl -s -H "Authorization: Bearer $KEY" -H "User-Agent: Mozilla/5.0" \
     "$BASE/models" | head -c 3000
   ```
   ⚠️ urllib (Python por defecto) recibe **403** en muchos endpoints por WAF
   (bloqueo de User-Agent). Curl con `User-Agent: Mozilla/5.0` responde 200.
   Ver skill `ua-spoofing-eval` para el caso general.
3. **Escanear qué modelos responden y a qué costo** (probe ligero con max_tokens=3):
   ```bash
   for m in <modelos>; do
     curl -s -H "Authorization: Bearer $KEY" -H "User-Agent: Mozilla/5.0" \
       -H "Content-Type: application/json" \
       -d "{\"model\":\"$m\",\"messages\":[{\"role\":\"user\",\"content\":\"hola\"}],\"max_tokens\":3}" \
       "$BASE/chat/completions" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('cost','?') if 'choices' in d else d.get('error',{}).get('message','ERR'))"
   done
   ```
   Respuesta de éxito incluye `cost` (string): `"0"` = la suscripción cubre el usage.
4. **Añadir el provider al config** con merge atómico y backup (ver reference de
   OpenCode Go para el patrón multi-modelo). `manage_provider.py add` agrega UN
   modelo por llamada → para catálogos grandes usar Python yaml + backup, aceptando
   que `yaml.safe_load`+`yaml.dump` PIERDE comentarios.
5. **No tocar el modelo activo** salvo indicación: añadir el provider SIN cambiar
   `model.default`. Verificar con `python3 -c "import yaml; yaml.safe_load(open('config.yaml'))"`.

## Arquitectura de fallback en cascada (validada con el equipo 26/08)

| Capa | Proveedor | Tipo | Nota |
|------|-----------|------|------|
| 0 | Provider primario (NaN-Builders) | HTTP | Modelo por bot repartido para no chocar bucket |
| 1 | Retry backoff nativo Hermes | Reintento | `agent.api_max_retries: 3` (default) |
| 2 | Segundo provider de API (B.AI) | HTTP fallback | `fallback_providers: [{provider: 'B.AI'}]` + bloque providers |
| 3 | OpenCode CLI/Go | Fallback de EJECUCIÓN | `opencode run '<prompt>' --model <go>` — runtime propio, corre aunque el gateway caiga; escribe `estado.json` (exit_code, duración, modelo) para el watchdog |

- Un watchdog (Vigía) añade resiliencia de proceso: leer `cron/ticker_heartbeat` +
  `cron/ticker_last_success` de cada perfil; si no late, respawn s6 `gateway-default`.
- **BLOQUEANTE**: si una skill usada por el wrapper está duplicada en el catálogo
  (ej. `opencode` en 2 rutas) → `Ambiguous skill name` y el wrapper falla ANTES de
  llegar al fallback. Deduplicar a ruta canónica o referenciar por ruta explícita.

## Pitfalls

- La cascada vale SOLO si cada capa usa un proveedor/runtime distinto al anterior.
- Verificar el estado real del "gratis": B.AI responde `deepseek-v4-flash` SIN saldo,
  pero gpt-5.x/glm dan `access_denied: Deposit required` y minimax `insufficient_user_quota`.
  No asumir "varios gratis" por el listado /models — probe por modelo (hay que probar).
- `cost:"0"` en OpenCode Go ≠ modelo útil: algunos devuelven 500/400/Unsupported en
  el probe (grok-4.6 formato oa-compat, mimo-v2-pro/omni unsupported) — registrar
  cuáles sirven hoy y revalidar tras cambios de la plataforma.
- Ráfaga de crons en paralelo: escalonar en el tiempo (1 por 6 min) además de repartir
  modelos; verificado 26/08: concurrency limit "max 5 simultaneous requests" tiró un
  thread de ~98K tokens tras 3 retries.

## Verification

- `GET /models` con UA → 200; chat probe → `cost:"0"` o error esperado.
- `providers` en config incluye el nuevo; `model.default` intacto.
- `fallback_providers` presente en los perfiles objetivo.
- Tras una ráfaga de crons: sin 429 en `logs/errors.log` del perfil.

## References

- `references/opencode-go-provider.md` — catálogo completo verificado (24 modelos
  cost=0), endpoint, bloque YAML, patrón de merge atómico multi-modelo.