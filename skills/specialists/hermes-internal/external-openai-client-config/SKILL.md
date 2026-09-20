---
name: external-openai-client-config
description: Add OpenAI-compatible providers to Brave or AI clients.
---

# Configurar provider OpenAI-compatible en clientes AI externos

Cubre cómo aparcir un endpoint OpenAI-compatible (típicamente NaN Builders u
otro provider custom) en un asistente AI que no es Hermes — Brave Leo (BYOM),
etc. NO confundir con `provider-manager` (ese gestiona providers en el
`config.yaml` de Hermes).

## Regla de oro del endpoint

El cliente externo **POSTea la URL exacta que le des, verbatim** — no le
añade `/v1`, no reescribe paths. Por eso el campo *Server Endpoint* debe ser
la URL **COMPLETA** del chat completions:

```
https://api.nan.builders/v1/chat/completions
```

no solo `https://api.nan.builders/v1`. Dejar slash final suele romper.

## Brave Leo BYOM — pasos

1. `brave://settings/leo` → **Bring Your Own Model / Custom model** → **Add custom model**
2. Rellenar la tabla de campos (ver `references/brave-leo-byom.md` — incluye
   la config exacta para NaN + el System Prompt de navegación).
3. Guardar y **seleccionar el modelo como ACTIVO** (solo configurado = no funciona).

Campos comunes (varía el label, no la semántica):
`Label`, `Model Request Name` (= string `model`), `Server Endpoint`,
`Context Size`, `API Key`, `Vision Support`, `Tool Support`, `System Prompt`.

## Comportamiento de Brave por debajo (confirmado en brave-core)

- Manda `content` como **LISTA de parts** OpenAI multimodal
  (`[{"type":"text","text":...}]`), `stream:true`, `max_tokens`.
- **`temperature` hardcodeada a 0.7** — sin campo para cambiarla.
- User-Agent real de Chrome → pasa Cloudflare/UA-gated APIs (el error
  "403 code 1010" solo pega con UA no-navegador).
- Con Tool Support ON inyecta un array `tools` y espera roundtrip
  `role:"tool"` — providers sin tool-calling (como NaN) pueden fallar;
  mantener OFF.

## AI Browsing (agéntico) — SI el usuario quiere clics/navegación

El Leo normal **NO toca páginas** (solo resume la activa). La navegación
agéntica es otra feature experimental: **AI Browsing**.
- Activar: `brave://flags` → `#brave-ai-chat-agent-profile` → Enabled → Relaunch.
- Corre en **perfil aislado** (no toca cookies/sesiones reales).
- Riesgos documentados por Brave: prompt injection, tareas con login fallidas.
- Detalle y fechas de release en `references/brave-leo-byom.md`.

## Troubleshooting

- "Network error": endpoint sin slash final + modelo **seleccionado activo**.
- Respuestas de plantilla: API key vacía o slash final.
- Verificar el endpoint antes desde terminal con curl (ver skill `nan-builders-api`).