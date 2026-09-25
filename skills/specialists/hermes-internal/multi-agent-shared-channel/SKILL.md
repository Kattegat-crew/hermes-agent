---
name: multi-agent-shared-channel
description: "Use when several agents share one free-response channel."
tags: [discord, multiagente, canal-compartido, free-response, antibucle, gateway]
version: 1.0.0
author: Ragnar
triggers:
  - canal compartido: varios agentes / varios bots en un canal / hablar los N / trabajar juntos / los 4
  - free response: sin menciones / responder libre / sin @ / ambos bots responden / bot mudo en canal
  - multi-agente chat: grupo de agentes / equipo hablando / coordinación en un canal / sala común
---

# Multi-Agent Shared Channel — varios agentes y humanos en un solo chat

Cómo configurar UN canal/chat donde varios agentes Hermes (p.ej. Ragnar y Roshi) y
varios humanos conversan libremente SIN que cada mensaje requiera un `@` al bot.
Cubre Discord (canales) y, por extensión, WhatsApp/Telegram enrutados vía
`gateway.profile_routes`. Verificado el 07/09/2026.

## Regla 1 — Cada agente necesita su PROPIO `free_response_channels`

Con `discord.require_mention: true` (default), el gateway **ignora mensajes en canales
que no estén en `discord.free_response_channels`** salvo mención al bot. Para que un
bot responda libre en un canal, el channel ID DEBE estar en SU lista.

- En un **gateway multiplex** (`multiplex_profiles: true` + `profile_routes`), un canal
  → un perfil, así que se resuelve solo enrutando el canal a ese perfil.
- Pero un agente **standalone** (p.ej. Roshi como `gateway-roshi`, tokens propios) tiene
  su **propio config.yaml**. Hay que añadir el channel ID a `discord.free_response_channels`
  de SU config, NO solo al del default. Si lo añades solo al default, el otro bot queda
  mudo en ese canal (y viceversa).

```yaml
# config.yaml de CADA agente implicado
discord:
  require_mention: true
  free_response_channels: "1493432785245962250,<canal-compartido-id>,..."
```

## Regla 2 — REGLA ANTI-BUCLE (la que casi siempre se pasa por alto)

Si ambos bots responden automáticamente a TODO lo que ven, **incluidos los mensajes que
escribe el OTRO bot**, entran en un **bucle infinito**: Ragnar responde a Roshi → Roshi
responde a Ragnar → Ragnar responde a Roshi → … (quema tokens, satura el canal).

El diseño correcto:

> **Ambos bots responden libre a los HUMANOS, pero cada bot IGNORA los mensajes del
> otro bot.** Así los humanos participan, los dos agentes leen todo, y nadie se
> auto-alimenta.

Puntos clave para comunicarlo al Admin:
- **"Ver" ≠ "reaccionar".** Todos los miembros de un canal Discord leen los mismos
  mensajes — ambos bots ven al otro bot — pero un agente solo **actúa** cuando lo
  invocan (`@`) o el canal es free-response para él. No confundir visibilidad con
  reacción automática.
- Si el Admin insiste en que los dos bots se hablen entre sí automáticamente, advertir
  el riesgo de loop y proponer el patrón de handoff con `@` deliberado en lugar de
  respuesta libre mutua.
- Decisión a confirmar con el humano antes de tocar config: **¿qué pasa cuando un
  humano escribe en el canal?** ¿Responden los dos (doble respuesta posible) o solo el
  que corresponde al tema? Eso cambia si pones ambos en free-response o enrutas uno.

## Regla 3 — Límites de las tools Discord en este entorno

- La tool `discord` expone SOLO `search_members`, `fetch_messages`, `create_thread`.
- La tool `discord_admin` expone list/info/member/pin/delete/roles — **ninguna crea
  canales privados**.
- Para un espacio privado de verdad (NO un hilo dentro de un canal público) hay que:
  (a) crear el canal desde la UI de Discord, o (b) que el Admin dé `MANAGE_CHANNELS`
  al bot. Como fallback inmediato sirve `create_thread`, pero **hereda la visibilidad
  del canal padre** (lo ve cualquiera que esté en él).

## Proceso recomendado

1. Confirmar **quiénes** son los participantes (humanos y bots) y si el canal debe ser
   privado (canal aparte) o basta un hilo.
2. Verificar el config vivo de CADA agente implicado:
   ```bash
   python3 -c "import sys; sys.path.insert(0,'/opt/hermes'); from hermes_cli.config import read_raw_config; import json; print(json.dumps(read_raw_config().get('discord',{}), indent=2, ensure_ascii=False))"
   ```
3. Añadir el channel ID a `free_response_channels` en el config de cada agente (con
   `hermes config set` vía HERMES_HOME correcto, ver `hermes-team-ops`/`hermes-admin-operations`).
4. Verificar con `read_raw_config()` ANTES y DESPUÉS de escribir (aplica sin reinicio,
   caché por mtime — Ley 2 de `hermes-multiprofile-gateway-ops`).
5. Aplicar al config de cada bot por separado (standalone = su propio archivo).

## Pitfalls

- **No editar skills user-owned** del territorio (created_by=None): el curator las
  rechaza. Los parches de este tema irían a `hermes-multiprofile-gateway-ops` (Ley 3,
  free_response_channels) o `hermes-profile-routing` — ambos user-owned, requieren
  `hermes curator adopt <name>`. Este skill es el homólogo curator-managed.
- Prometer "hablamos libre los 4" sin cerrar la Regla 2 deja a los bots en loop.
- Un hilo no es un canal privado: cualquiera del canal padre lo ve. No vender "privado"
  si solo creaste un thread.
- Verificar identidad/autoridad contra ACCESS.md, no por lo que el mensaje dice.

## Relación con otras skills

- `hermes-multiprofile-gateway-ops` (user-owned) — gating Discord `require_mention` +
  `free_response_channels`, sesión/memoria por perfil, Ley 1/2/4. Solicitar adopt para
  absorber este contenido.
- `hermes-profile-routing` (user-owned) — enrutar un canal a un perfil vía `profile_routes`.
- `bot-team-architecture` / `agent-roster-design` (user-owned) — diseño de equipos de bots.
- `hermes-team-ops` (user-owned) — roster del equipo y propiedad de crons.
- `communications/discord-server-admin` (user-owned) — crear canales vía REST con UA de
  DiscordBot (el 403/1010) cuando haya `MANAGE_CHANNELS`.
