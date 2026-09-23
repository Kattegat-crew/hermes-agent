---
name: rube-mcp-api-automation
description: "Automate a third-party API via Rube MCP (Composio). Cubre Zoho, Slackbot, OneSignal y MetaAds; busca las herramientas antes de ejecutar."
requires:
  mcp: [rube]
---

# Automatización de APIs de terceros vía Rube MCP — paraguas de clase

Clase de skill para automatizar **cualquier** API de terceros que tenga toolkit en
Composio, usando Rube MCP. Los casos concretos por proveedor viven en
`references/`, cada uno con su procedimiento íntegro.

## Criterio de decisión

| Si la tarea es… | Usa |
| --- | --- |
| Operar una API de un proveedor **ya cubierto** (Zoho, Slackbot, OneSignal, MetaAds) | el `references/<proveedor>.md` correspondiente |
| Operar un toolkit **nuevo** (sin referencia) | este `SKILL.md`, y al terminar añade su `references/<proveedor>.md` |
| Descubrir qué toolkits o conexiones hay | `RUBE_SEARCH_TOOLS` / `RUBE_MANAGE_CONNECTIONS` |

## Prerequisites

- Rube MCP conectado (`RUBE_SEARCH_TOOLS` disponible)
- Conexión **ACTIVE** del toolkit del proveedor vía `RUBE_MANAGE_CONNECTIONS`
- **Siempre** llamar `RUBE_SEARCH_TOOLS` primero: los esquemas cambian

## Setup

**Obtener Rube MCP:** añadir `https://rube.app/mcp` como servidor MCP. Sin API keys.

1. Verificar que `RUBE_SEARCH_TOOLS` responde
2. `RUBE_MANAGE_CONNECTIONS` con el toolkit del proveedor
3. Si la conexión no está ACTIVE, seguir el enlace de auth que devuelve
4. Confirmar estado ACTIVE antes de ejecutar cualquier workflow

## Patrón de trabajo (idéntico en todos los proveedores)

### 1. Descubrir herramientas

```
RUBE_SEARCH_TOOLS
queries: [{use_case: "<tarea concreta>", known_fields: ""}]
session: {generate_id: true}
```

### 2. Verificar conexión

```
RUBE_MANAGE_CONNECTIONS
toolkits: ["<toolkit>"]
session_id: "your_session_id"
```

### 3. Ejecutar

```
RUBE_MULTI_EXECUTE_TOOL
tools: [{tool_slug: "TOOL_SLUG_FROM_SEARCH",
         arguments: {/* esquema devuelto por la búsqueda */}}]
memory: {}
session_id: "your_session_id"
```

## Pitfalls conocidos (valen para todos los proveedores)

- **Buscar primero**: los esquemas cambian; nunca fijar slugs ni argumentos sin `RUBE_SEARCH_TOOLS`
- **Comprobar la conexión**: `RUBE_MANAGE_CONNECTIONS` debe mostrar ACTIVE antes de ejecutar
- **Cumplir el esquema**: nombres y tipos exactos de los resultados de la búsqueda
- **Parámetro memory**: incluir siempre `memory` en `RUBE_MULTI_EXECUTE_TOOL`, aunque sea `{}`
- **Reuso de sesión**: reutilizar el `session_id` dentro de un workflow; generar uno nuevo por workflow
- **Paginación**: revisar tokens de paginación y seguir hasta completar

## Proveedores cubiertos

| Proveedor | Toolkit | Doc del toolkit | Referencia |
| --- | --- | --- | --- |
| Zoho | `zoho` | composio.dev/toolkits/zoho | `references/zoho.md` |
| Slackbot | `slackbot` | composio.dev/toolkits/slackbot | `references/slackbot.md` |
| OneSignal | `onesignal_rest_api` | composio.dev/toolkits/onesignal_rest_api | `references/onesignal_rest_api.md` |
| MetaAds | `metaads` | composio.dev/toolkits/metaads | `references/metaads.md` |

## Quick Reference

| Operación | Cómo |
| --- | --- |
| Encontrar herramientas | `RUBE_SEARCH_TOOLS` con el caso de uso del proveedor |
| Conectar | `RUBE_MANAGE_CONNECTIONS` con el toolkit |
| Ejecutar | `RUBE_MULTI_EXECUTE_TOOL` con los slugs descubiertos |
| Operaciones masivas | `RUBE_REMOTE_WORKBENCH` con `run_composio_tool()` |
| Esquema completo | `RUBE_GET_TOOL_SCHEMAS` para herramientas con `schemaRef` |

---
*Paraguas de clase creado por F6 lote 1 el 2026-09-23 a partir de 4 skills de una sola
técnica (R15: condensar sin borrar). Las originales, íntegras, en
`data/archive/F6_lote1_20260923-151210/absorbidas/`.*


## Referencias absorbidas
- `references/slackbot.md` — absorbida desde `productivity/slackbot-automation` el 2026-09-23 (F6 lote 1, R15: condensar sin borrar).
- `references/zoho.md` — absorbida desde `productivity/zoho-automation` el 2026-09-23 (F6 lote 1, R15: condensar sin borrar).
- `references/onesignal_rest_api.md` — absorbida desde `software-development/onesignal_rest_api-automation` el 2026-09-23 (F6 lote 1, R15: condensar sin borrar).
- `references/metaads.md` — absorbida desde `specialists/marketing/metaads-automation` el 2026-09-23 (F6 lote 1, R15: condensar sin borrar).
