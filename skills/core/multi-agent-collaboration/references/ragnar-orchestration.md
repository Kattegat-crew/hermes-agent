---
name: ragnar-orchestration
description: "Use when orquestando la flota: plan→subplan→worker."
---

# Orquestación Planner → Subplanner → Worker (Nuestro Hermes)

Patrón del tuit de @santtiagom_ (Cursor): escalar agentes NO es añadir en plano; es dejar la coordinación peer-to-peer y pasar a una jerarquía en árbol. Cada worker trabaja sobre su contexto/repo aislado y devuelve el resultado **solo a su asignador**.

**Target:** flota interna de NeuralCrew Labs. NO toca el inbox de escalada de clientes en PROD (eso vive en la skill `escalada-tecnica` y ya está operativo).

## Roles en la jerarquía

| Rol | Quién | Qué hace |
|-----|-------|----------|
| **Planner** | Ragnar (default) | Entiende el objetivo, lo descompone, rutea sub-tareas, agrega resultados, reporta a Jonathan. |
| **Sub-planner** | Ragnar o `delegate_task` anidado / un especialista | Cuando una parte se divide sola, la sub-divide y rutea a sus hijos. |
| **Worker** | `delegate_task` (contexto aislado) + especialistas (Bragi=contenido, Sindri=dev, Freyja=diseño, ...) | Ejecuta una sub-tarea concreta y devuelve evidencia a su asignador. |

## Ciclo del planner (7 pasos)

1. **Entender el objetivo** — entregable esperado + criterio de aceptación (no un ticket monolítico).
2. **Descomponer** en sub-tareas de 2-5 min. Si una parte se divide sola → sub-planner.
3. **Asignar** a cada sub-tarea: `destino` (dominio), `parent_task`, `dependencias`.
4. **Inyectar contexto autocontenido** por worker — el worker NO ve la conversación del planner.
5. **Exigir evidencia observable** en el resultado (archivo en disco >0, URL, ID real, salida real). Prohibido "listo" sin evidencia.
6. **Agregar en bloques** → UN solo reporte a Jonathan, no uno por sub-tarea.
7. **Escalar stuck** — reintento con otro enfoque tras N min; tras 2 fallos del mismo método → subir de worker / escalar.

## Esquema de delegación (liviano, paralelo al buzón)

Cada sub-tarea/woker lleva: `destino` · `parent_task` · `dependencias` · `evidencia` (obligatoria) · `intentos`. Este esquema **no modifica** el schema del buzón PROD.

## Ledger de coordinación

`delegation_state.json` (workspace del perfil default) mapea padre→hijos con estado:
- `pending` → `run` → `done` (con evidencia) | `failed` (con error)
- Avanzarlo al recibir resultados. Idempotente (re-ejecución no duplica). Sirve de traza y para reportar el resumen en bloque.

## Modelo on-demand de los especialistas (despertar)

Los gateways de especialistas son servicios s6 (`gateway-bragi`, `gateway-sindri`, `gateway-freyja`, ...). El default (Ragnar) persiste vía `gateway_state.json` con `"desired_state": "running"`.

Un especialista **se despierta** cuando:
- Alguien le escribe en **Discord** (ping/@mención en su canal).
- Alguien le escribe en **Desktop** (mensaje a su perfil).
- **Ragnar lo necesita** para una sub-tarea de su dominio → activar su gateway on-demand.

Los especialistas se mejoran **incrementalmente** (skills/voz/flujo); no son de una sola vez — se refinan con cada uso.

> **Para activar:** usar la skill de fleet-ops apropiada (`hermes-fleet-lifecycle`, `hermes-multiprofile-gateway-ops`) para levantar/confirmar `desired_state` del gateway; solo se levantan cuando aportan dominio específico (dev tiene 8GB, no todos a la vez). Verificar el comando exacto antes de usarlo en el entorno real.

## Reglas duras

- **Evidencia verificada** por el planner, no autodeclarada por el worker.
- **Reporte en un solo bloque** (sumario agregado), nunca N mensajes.
- **2 fallos del mismo método → cambiar de enfoque/subir de worker** (anti-slop).
- **No sobre-descomponer** (YAGNI) — granularidad 2-5 min, no más.
- **PROD intacto** — este protocolo es solo flota interna.

## Pitfalls

- `delegate_task` corre dentro del mismo gateway → NO requiere levantar especialistas para tareas aisladas; solo los levanta cuando aportan dominio.
- No confundir este protocolo con el inbox de escalada PROD (`escalada-tecnica`).
- Verificar el comando real de activación de gateway (s6/container_boot) antes de dispararlo — no asumir.
