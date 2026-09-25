---
name: hermes-model-rotation
description: "Use when rotating a Hermes profile model to a new one."
tags: [hermes, modelos, rotacion, providers, config, perfiles, smoke-test]
version: 1.0.0
author: Ragnar
triggers:
  - modelos: rotar modelo / cambiar modelo principal / nuevo modelo disponible / actualizar modelos / qwen3.8 / glm5.3 / NaN Cloud
  - provider: actualizar catálogo de modelos / providers.models / custom_providers / fallback sin tocar
  - verificación: smoke test de modelo / leer respuesta de hermes chat / state.db messages
---

# Hermes Model Rotation — rotar el modelo principal de perfiles Hermes

Rotación de `model.default` (y opcionalmente auxiliares) de uno o muchos perfiles cuando aparece
un modelo nuevo en el proveedor (NaN Builders u otro), **sin tocar fallbacks ni `.env`**.
Validado 26/08/2026 al rotar 14 perfiles a `qwen3.8-flash` (local + prod) cuando `glm5.3-flash`
aún no estaba habilitado en el plan.

## Workflow (orden exacto)

1. **Descubrir los IDs reales del proveedor** (NO inventar nombres):
   `GET <base_url>/models` con key + User-Agent de navegador (NaN exige UA o da 403/1010).
   NaN devuelve solo `id`s — sin `context_length`; los specs van del dashboard o por smoke test.

2. **Verificar disponibilidad REAL del modelo** — listado ≠ habilitado:
   ```python
   POST /v1/chat/completions {"model":"<id>","messages":[{"role":"user","content":"hola"}],"max_tokens":8}
   ```
   - 200 + respuesta → disponible.
   - **401 `{"error":{"message":"Missing Authentication header"}}`** con la MISMA key que sí
     funciona en otros modelos → el modelo **NO está en el plan** (dashboard cloud.nan.builders
     → plan/cuotas). No tocar credenciales; la acción es del usuario (habilitar el modelo).
     Caso real 26/08: `glm5.3-flash` 401 en 3/3 mientras `qwen3.8-flash`/`deepseek-v4-flash` OK.

3. **Backup** de cada config antes de tocar (`cp config.yaml /opt/data/backups/config-<perfil>-<ts>-pre-<modelo>.yaml`);
   en prod remoto, backup bajo su propio `/opt/data/backups/`.

4. **Editar como dict, NUNCA por strings/regex.** Fallo real de naive regex: quedó
   `default: qwen3.8-flashdeepseek-v4-flash` (pegado sin salto, YAML roto). Método seguro:
   `yaml.safe_load` → `data["model"]["default"] = <nuevo>` → sync catálogo →
   `yaml.safe_dump(sort_keys=False)` → validar el dump con `yaml.safe_load` → backup → escribir.
   Script reutilizable: `scripts/rotate_model_yaml.py`.

5. **Sincronizar catálogo** en los bloques que el perfil use:
   - `providers.NaN-Builders.models` — siempre (autoridad de ruteo).
   - `custom_providers` (bloque con `name: NaN-Builders`) — SOLO si existe. **Prod NO tiene
     `custom_providers`**: usa `model` con `provider: custom` + `base_url:
     http://hermes-llm-proxy:8742/v1` (nginx, no filtra modelos) + `fallback_providers`. Un
     chequeo `custom=False` ahí es esperado, no un error.

6. **Verificar**:
   - `yaml.safe_load` de cada config OK y `model.default` con el valor exacto (con su espacio).
   - Smoke real: `hermes chat -q "..."` (o `--profile <p>`) y leer la respuesta. Las sesiones
     viven en **`state.db`** (tabla `messages` por `session_id`), NO en `sessions/*.jsonl`:
     ```python
     sqlite3.connect('state.db'); SELECT role,content FROM messages WHERE session_id=? AND role='assistant' ...
     ```
   - Revisar qué perfiles NO deben rotar por inercia: código/repos (mantener deepseek-v4-flash
     1M ctx para repos), bots ligeros de alerta (gemma4) — rotación selectiva, no masiva ciega.

## Pitfalls

- Nunca editar `config.yaml` con regex/strings (el tool las bloquea; y la regex rompe YAML).
- No declarar un modelo "disponible" solo porque aparece en `GET /models` — smoke obligatorio.
- No tocar `fallback_providers`, `.env`, ni keys durante una rotación de modelo.
- `hermes config set` sin `--profile` puede escribir en OTRO perfil (el activo por defecto del
  binario, p. ej. sindri) — usar `HERMES_HOME=/opt/data` para default y verificar la ruta en la
  salida. (Ver también skill `hermes-team-ops`.)
- Tras rotar, los cambios hot-reload por turno (sin reiniciar gateway); `profile_routes` no.

## The 3 skills que NO se pueden editar (user-owned)

`nan-builders-api` (UA/Cloudflare, modelo tests), `hermes-multiprofile-model-config` (401 por
keys, multiplex Discord) y `hermes-provider-configuration` (estructura providers/custom) están
marcadas user-owned (`created_by=None`): el curator las rechaza. Para actualizarlas desde una
sesión, correr `hermes curator adopt <skill>` primero.

## Referencias

- `references/rotacion-modelos-2026-08-26.md` — bitácora: matrices local/prod, GLM 401, estructura prod, fallo naive.
- `scripts/rotate_model_yaml.py` — script reutilizable (backup + dict + validación).