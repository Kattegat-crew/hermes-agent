# Fallback de ejecución para crons — patrón de 3 capas (validado 26/08/2026)

Objetivo: que un cron/task/agente nunca muera si el proveedor principal falla.

## Las 3 capas (en cascada)

| Capa | Tipo | Qué es | Estado |
|------|------|--------|--------|
| 0 | Primario (HTTP) | NaN-Builders, modelo por bot | config `model.default` |
| 1 | Reintento | `agent.api_max_retries: 3` (backoff) | nativo |
| 2 | Fallback de API | `fallback_providers: [provider: B.AI]` (+ OpenCode-Go) | config |
| 3 | Fallback de ejecución | watchdog que re-ejecuta el prompt del job vía proveedor alternativo | scripts/fallback_watchdog.py |

Nota: el retry nativo (capa 1) y `fallback_providers` (capa 2) los maneja Hermes
automáticamente. La capa 3 es por si el problema NO es del modelo (permisos,
proceso caído, config rota): un cron del perfil de sistema (vigía) escanea los
jobs.json de todos los perfiles y, ante `failure_streak >= 2` o `last_status`
distinto de ok, re-ejecuta el `prompt` del job vía una llamada HTTP a un
proveedor alternativo (OpenCode-Go / mimo-v2.5, cost=0).

## Wrapper API (no CLI)

Decisión de operación (26/08): el fallback NO lanza el CLI `opencode run` ni
requiere `opencode auth login`. Llama directo a la API:

- Endpoint: `https://opencode.ai/zen/go/v1/chat/completions`
- Modelo: `mimo-v2.5` (ID SIN prefijo — ver references/opencode-go-api.md)
- Auth: `Authorization: Bearer <OPENCODE_GO_API_KEY>` (key del config del
  perfil o env `OPENCODE_GO_API_KEY`; NUNCA hardcodeada en scripts).
- Escribe `estado.json` (exit_code, duración, modelo, output_tail, timestamp)
  para que el watchdog / Vigía lo lea.

Exit codes del wrapper: 0 = éxito, 124 = timeout, 3 = sin key (inactivo),
2 = invocación inválida, 1 = falló (detalle en estado.json).

## LIMITACIÓN HONESTA (no vender humo)

Una llamada a LLM vía HTTP solo produce TEXTO. NO ejecuta las herramientas de
Hermes (mem_save/engram, publicación, APIs). Para jobs que producen texto
(reportes, resúmenes, avisos) el fallback de ejecución es completo. Para jobs
de MEMORIA (guardar-diario) genera texto pero NO hace el doble guardado real —
ahí la protección real es:
1. fijar permisos del runner (chown/chmod del directorio output del job al uid
   del proceso — ver gateway-ops),
2. pin del job (--provider/--model, ver SKILL.md §1),
3. cascada de providers (NaN → B.AI → OpenCode-Go).

## Verificación

- `python3 scripts/fallback_watchdog.py --dry-run` → lista jobs fallidos sin ejecutar.
- Run real con `OPENCODE_GO_API_KEY` seteada → re-ejecuta y escribe estado.json.
- En jobs regulares de memoria, verificar `last_status: ok` tras el fix de permisos.