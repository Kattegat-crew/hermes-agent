<!-- Caso absorbido por F6 lote 4 el 2026-09-23 desde `specialists/hermes-internal/hermes-provider-fallback`.
     Contenido íntegro; original en
     `data/archive/F6_lote4_20260923-161107/absorbidas/`. -->

---
name: hermes-provider-fallback
description: Cascada de fallback multi-proveedor para bots Hermes.
version: 1.0.0
author: Ragnar
metadata:
  hermes:
    tags: [providers, fallback, rate-limit, opencode-go, b.ai, nan-builders, cascada]
    category: devops
    related_skills: [provider-manager, nan-builders-api, hermes-team-ops, hermes-multiprofile-cron-ops]
---

# Hermes Provider Fallback — cascada resiliente NaN → B.AI → OpenCode-Go

Cómo configurar un perfil/bot de Hermes con 3 proveedores en cascada para que ningún
cron/task/agente muera por rate-limit (429) o caída del proveedor primario. Patrón
validado en producción 26/08/2026 con los 9 bots del equipo marketing.

## When to Use

- Se configura un perfil/bot nuevo y hay que darle fallback de modelo.
- Un bot muere con 429 (`max 5 simultaneous requests` en NaN-Builders) y hay que repartir.
- Se añade un provider nuevo (B.AI, OpenCode-Go, otro compat OpenAI) a la cascada.
- Antes de asignar un modelo default hay que verificar que exista en el catálogo.

## Arquitectura en cascada

```yaml
model:
  provider: NaN-Builders
  default: deepseek-v4-flash
providers:
  NaN-Builders: { api_key: ..., base_url: https://api.nan.builders/v1, models: {...} }
  B.AI: { api_key: ..., base_url: https://api.b.ai/v1, models: {...} }
  OpenCode-Go: { api_key: ..., base_url: https://opencode.ai/zen/go/v1, models: {mimo-v2.5: {context_length: 1048576}} }
fallback_providers:
  - provider: NaN-Builders
  - provider: B.AI
  - provider: OpenCode-Go
```

Orden de resolución de Hermes: si el provider primario falla (429/timeout/error HTTP),
intenta el siguiente en `fallback_providers`. Además hay retry nativo (`api_max_retries: 3`).

## Procedure

1. **Verificar el catálogo ANTES de asignar modelos** — un modelo que no existe en el
   provider falla silenciosamente (caso real: `deepseek-v4-flash-0731` asignado pero
   inexistente en NaN/B.AI/OpenCode-Go):
   ```bash
   curl -s -H "Authorization: Bearer $KEY" <base_url>/models | python3 -c "import sys,json; print([m['id'] for m in json.load(sys.stdin)['data']])"
   ```
2. **Definir el provider en el bloque `providers` del MISMO config** que lo referencia
   en `fallback_providers`. **PITFALL CRÍTICO:** un perfil que lista `OpenCode-Go` en
   `fallback_providers` pero no tiene su bloque `providers.OpenCode-Go` NO resuelve el
   fallback — la cascada muere en silencio (mordió en producción 26/08; se replicó el
   bloque a los 9 bots).
3. **Repartir modelos por bucket** — no concentrar 5 bots en el mismo modelo/endpoint
   (rate-limit de NaN es `max 5 simultaneous requests`). Modelo primario distinto por bot.
4. **Replicar a perfiles**: copiar el bloque `providers` completo (con keys) a cada perfil,
   NO solo la lista de fallback. Verificar por re-lectura del YAML.
5. **Activar `smart_model_routing`** (cheap_model qwen3.6) para respuestas cortas sin
   gastar el modelo principal.
6. **Verificar** con re-lectura YAML + chat probe al modelo.

## B.AI (api.b.ai) — qué sirve gratis

- Con key sin saldo: `deepseek-v4-flash` responde OK (free-limited) — verificado 26/08.
- `gpt-5.x`, `glm-5.x` → `access_denied: Deposit required` (premium bloqueado sin saldo).
- `minimax-m2.7` → `insufficient_user_quota` (balance=0).
- No asumir "varios gratis": probar cada modelo con un chat probe ligero (`max_tokens:3`).

## OpenCode-Go (API de la suscripción)

- Endpoint: `https://opencode.ai/zen/go/v1` (compat OpenAI).
- **Los IDs de modelo en la API NO llevan prefijo `opencode/`** — es `mimo-v2.5`,
  NO `opencode/mimo-v2.5` (este último devuelve `401 Model not supported`).
- Campo `cost: "0"` en la respuesta = no consume usage (subs cubierta).
- Detalle completo en `references/opencode-go-api.md` (modelos, errores, curl).

## Fallback de EJECUCIÓN (no solo de modelo)

La cascada de providers cubre fallos de API. Para crons que mueren por otra causa
(permisos, runtime), ver el watchdog en `hermes-team-ops` (vigia-fallback-watchdog) y
el wrapper API `/opt/data/scripts/hermes-fallback-opencode-api.py`.

**Limitación honesta:** un fallback por API re-ejecuta el PROMPT y produce texto, pero
NO ejecuta herramientas de Hermes (mem_save, engram, publicación). Para jobs de texto
(reportes) es completo; para jobs de memoria/acciones, la protección real es fix de
permisos + cascada de providers + retry.

## Pitfalls

- `fallback_providers` sin el provider definido en `providers` → cascada muerta en silencio.
- Asignar un modelo documentado pero no listado en el catálogo → falla silenciosa.
- 5+ bots en el mismo modelo → 429 concurrente.
- Los keys viven SOLO en config.yaml; nunca en scripts ni logs del wrapper.
- Los perfiles corren en `/opt/data/profiles/` (bind mount real), no en
  `/root/hermes-agent/data/profiles/` — verificar contra la ruta correcta.

## Verification

- `grep -A8 fallback_providers <perfil>/config.yaml` → lista completa.
- `grep -A4 "OpenCode-Go:" <perfil>/config.yaml` → bloque providers presente.
- Chat probe: `curl -s <base_url>/chat/completions -d '{"model":"X","messages":[{"role":"user","content":"ok"}],"max_tokens":3}'` → 200 con `choices`.