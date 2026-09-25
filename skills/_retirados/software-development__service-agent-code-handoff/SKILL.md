---
name: service-agent-code-handoff
description: Use when handing task to AGY/OpenCode/Claude Code.
version: 1.0.0
author: hermes
license: MIT
metadata:
  hermes:
    tags: [handoff, spec, prompt, coding-editor, agy, opencode, compliance, implementation, checklist]
---

# Service-Agent Code Handoff (SPEC + PROMPT → AGY/OpenCode)

Patrón para externalizar a un editor de código (AGY, OpenCode, Claude Code) la implementación de features
en repos de clientes *sin* que el orchestrator escriba en el repo. Verificado en Golden Game (ruleta) y
The Grand Paradise Club (tragamoneda) — ambos con casillas de consentimiento legal y páginas legales nuevas.

## Resultado (siempre dos entregables)
1. **`SPEC-<ASUNTO>-<CLIENTE>-<FECHA>.md`** — PERMANENTE, queda en `docs/` del repo como auditoría:
   mapa de archivos/estado, textos exactos, payload/API, SQL, checklist de aceptación ✓/✗.
2. **`PROMPT-<ASUNTO>-<FECHA>.md`** — TEMPORAL y autocontenido para pegar entero al editor. El PROMPT exige
   entregar un INFORME FINAL y **borrarse a sí mismo al terminar** (el SPEC se conserva).

## Pasos
- **Analiza el repo** (componentes, `App.jsx` rutas, `webhook-server.js`, `schema.sql`). Si no está en
  `/opt/repos`, usa la skill `vps-host-access` (docker socket) para leer `/root/<repo>/:ro`.
- **Auditoría de estado por archivo**: tabla Archivo | Estado (ok/parcial/nada) | problema — el SPEC comunica
  al editor QUÉ tocar.
- **Mapa de implementación**: por cada elemento, dónde aparece (archivo+número de línea), texto exacto,
  enlace/redirección.
- **SPEC** incluye "Configuración requerida" por cambio (frontend: estados/validación/reset; backend:
  sanitización + endpoint INSERT; DB: migración SQL con columnas nuevas).
- **PROMPT** autocontenido: contexto obligatorio (lee el SPEC + AGENTS.md), alcance por archivo, reglas
  (no subir a producción si no se pide, no tocar piezas no especificadas), INFORME FINAL obligatorio
  (archivos creados/modificados, checklist ✓/✗, payload resultante, `npm run build`, confirmación del borrado).
- **Entrega**: si tu entorno no puede escribir en el repo (montaje read-only → "outside HERMES_WRITE_SAFE_ROOT"),
  produce los archivos bajo `/opt/data/entregables/<cliente>/docs/` manteniendo la estructura `docs/` del repo y
  dile al usuario que los copie al repo. No crees carpetas nuevas sin autorización.

## Pitfalls
- **Repo read-only**: los writes al mount del repo fallan con "outside HERMES_WRITE_SAFE_ROOT". Entrega en
  `entregables/<cliente>/docs/` y avisa copiar al repo.
- **Migraciones SQL**: versionar SOLO el `*.sql`; indicar que NO se ejecuta desde el repo (la DB corre aparte).
- **Textos legales**: no inventar; verbatim del documento legal de referencia (.docx del paquete). Si falta algo,
  el prompt ordena no inventar y reportarlo pendiente.
- **Prompt autocontenido**: el editor no ve el historial → todo el contexto va dentro del PROMPT.
- **Borrado del PROMPT**: incluir siempre la auto-eliminación al final (el SPEC permanece). Evita basura en `docs/`.

## Plantillas
`templates/prompt-handoff.md` — ejemplo de PROMPT autocontenido (4 casillas de consentimiento) para copiar/modificar.