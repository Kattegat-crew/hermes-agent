---
name: cron-delivery-routing
description: "Use when routing or debugging where cron output lands."
tags: [cron, entrega, routing, discord, whatsapp, devops]
version: 1.0.0
author: Ragnar
metadata:
  hermes:
    tags: [hermes, cron, delivery, discord, whatsapp, webhook, routing, devops]
    category: devops
---

# Cron Delivery Routing (dónde aterriza la salida de un job)

Clase de tarea: cambiar/revisar el destino de entrega de jobs programados, y diagnosticar «el cron corrió pero el mensaje nunca llegó». Solapa con las skills user-owned `scheduled-job-diagnosis` (job que no hizo su trabajo) y `hermes-cron-runtime-verification` (namespace/verificación) — este documento cubre la capa de ENTREGA.

## Regla #1: `last_status: ok` NO significa entregado

Una corrida puede quedar verde y no llegar a ningún canal. La verdad está en:

- `jobs.json → last_delivery_error` (lo último que falló, por job).
- `grep -ahE "delivery error|WhatsApp send failed|Discord send failed" /opt/data/logs/agent.log` (histórico, con hora y job id).
- `executions.db` (status/pid/error por corrida) — pero ojo: sin stdout el run no deja fila, así que la ausencia de filas no es ausencia de ejecución.

Recetas completas (queries, mapeo de canales, diff de tokens, protocolo de cambio) en `references/cron-delivery-forensics.md`.

## Semántica de `deliver`

- `deliver` acepta **lista con comas**: `whatsapp:573166910728@s.whatsapp.net,discord:1542126606900920340`. Los destinos se intentan por separado y **uno que falla no bloquea a los demás** (`_resolve_delivery_targets` + `continue` por destino en `_deliver_result`). Esa es la mitigación correcta cuando un canal es frágil.
- `attach_to_session: true` hace la entrega **continuable**: el reply del usuario entra con el brief del job en contexto. Requiere destino explícito único (con `deliver='origin'` usa el chat de origen).
- Destinos válidos: `local`, `all`, `bot-chat[:<perfil>]`, `<plataforma>:<chat_id>[:<thread_id>]`. La plataforma debe estar configurada.
- **Cada entrega es un solo intento, sin retry.** Si falla, el mensaje se pierde en silencio (el usuario se entera solo si pregunta).

## Pata WhatsApp: frágil por diseño

- Sale por un único `POST http://localhost:3000/send` al bridge local. Si el bridge está reconectando (`Connection closed (reason: 428/503). Reconnecting…` en `/opt/data/whatsapp/bridge.log`) un socket keep-alive viejo devuelve `[Errno 104] Connection reset by peer` o `Server disconnected`.
- `curl 127.0.0.1:3000/health` = `connected` **no prueba** que un envío concreto salió; y si no hay línea en `bridge.log` para ese minuto, la petición nunca llegó al bridge.
- Caso real (09-10/09/2026): `calendario-paquete-diario` generó el reporte dos mañanas seguidas y la pata de WhatsApp murió con ECONNRESET las dos veces → el admin nunca lo recibió; 6 fallos así en 2 días (≈15% de los envíos de los jobs de campaña).

## Pata Discord: la opción estable

- Destino: `discord:<channel_id>` (postea el bot del perfil). Verificado end-to-end: disparo manual y el mensaje apareció en el canal.
- Para mapear id→nombre: `DISCORD_BOT_TOKEN` de `/opt/data/.env` + `/users/@me/guilds` + `/guilds/{id}/channels`; el `topic` del canal delata al bot dueño (ej. «Bragi — NeuralCrew Content»).
- Si el canal ya está en `discord.free_response_channels` del perfil, las respuestas del usuario entran a ese perfil → es lo que habilita «responder en el canal para aprobar». Con `require_mention: true` el usuario debe responder al mensaje del bot o mencionarlo.
- Confirmar permiso del bot (ADMINISTRATOR, o bit SEND_MESSAGES) antes de elegir el canal.

## Webhook: identidad sí, destino de cron NO

- El webhook de Discord (canal → Integraciones → Webhooks) sirve para que los mensajes aparezcan con **identidad propia** (ej. «Crons de posts»), pero la plataforma `webhook` de Hermes es **solo de entrada**: no tiene emisor saliente, así que `deliver: webhook:<url>` no funciona aunque `webhook` figure en `_KNOWN_DELIVERY_PLATFORMS`. Si se quiere esa identidad: el script postea por curl y el job va con `deliver: local`.
- Un webhook recién creado puede venir **copiado con un carácter cambiado** → `401 {"message":"Invalid Webhook Token","code":50027}` en GET y en POST (el id puede ser perfectamente válido). No adivinar: recuperar el token real con `GET /guilds/{id}/webhooks` y comparar carácter por carácter.

## Protocolo de cambio de destino (con red)

1. `cp -a /opt/data/cron/jobs.json /opt/data/cron/jobs.json.bak-<motivo>-$(date +%Y%m%d-%H%M%S)`.
2. `cronjob_manage(action='update', job_id=..., deliver='discord:<channel_id>')` — no editar el JSON a mano mientras un ticker pueda estar escribiendo.
3. Leer `jobs.json` de vuelta y confirmar `deliver`.
4. Disparar UNA vez (`action='run'`) y verificar **leyendo el canal** (`GET /channels/<id>/messages`), no solo que el run dio ok.
5. Jobs que solo hablan ciertos días (informe mensual = primer lunes; publish = solo si hay piezas aprobadas) **no se pueden probar con un disparo manual**: decir eso en vez de declarar verificado.

## Webhook de Discord: patrón probado (no_agent + curl/urllib)

Cuando el destino es un **webhook** (identidad propia, sin bot), `deliver: webhook:<url>` no existe (la plataforma `webhook` es solo de entrada). El patrón que funciona, verificado end-to-end (11/09/2026, perfil vigia):

1. Job `no_agent=True` + `deliver: local` (stdout vacío = silencio total, sin ruido en el canal).
2. Un script **poster** reutilizable en `<perfil>/scripts/` que lee el texto por stdin y hace el POST con `username` propio, trocea a <=1900 chars y **nunca** lanza excepción (log a `logs/discord_post_error.log`, exit 0): un fallo de entrega no debe romper el job.
3. Un **wrapper** por job que ejecuta el chequeo, y solo si hay salida (alerta) la manda al poster. Los errores del chequeo (`2>&1`) también entran por ahí: se convierten en alerta, nunca en silencio falso.
4. La URL vive en el `.env` del perfil (`VIGIA_DISCORD_WEBHOOK=...`), no incrustada en el prompt ni en el script.

Ventaja: cero LLM en watchdogs de alta frecuencia (cada 10 min) y el canal queda limpio (silencio = sano).

## Silencio en jobs agent-mode: el token [SILENT]

Un watch en modo agente (vigilancia de bandeja, radar de aprobaciones) que debe hablar SOLO con novedad real depende del supresor del scheduler: `/opt/hermes/cron/scheduler.py:738-769` (`SILENT_MARKER = "[SILENT]"`, verificado 23-sep-2026).

- Tokens que suprimen la entrega: `[SILENT]`, `SILENT`, `NO_REPLY`, `NO REPLY` — como respuesta completa, primera línea o última línea, case-insensitive y trimmed. Un token a mitad de frase se considera contenido real y SÍ entrega (anti-falsa-supresión). Comparte matcher con el lane de webhook (`gateway.response_filters.is_autonomous_silence_response`): las dos vías autónomas no divergen.
- **"SILENCIO" en español NO suprime la entrega** — el prompt del job debe pedir el token literal `[SILENT]`.
- La corrida suprimida igual se guarda en `cron/output/<id>/` (auditable: qué vio y por qué calló).

Plantilla de prompt para watch crons (4 bloques):

1. Qué buscar + tool concreta (ej. `mcp__ncl_google__gmail_list`) + por qué existe el watch (qué solicitud está pendiente).
2. REGLA DE SILENCIO con exclusiones EXPLÍCITAS: qué NO cuenta como novedad (p. ej. rechazos de anuncios individuales, notificaciones de rendimiento, encuestas, actualizaciones genéricas de la plataforma). Sin esa lista el agente reporta cualquier correo tangencial y el ruido vuelve por la ventana.
3. Camino sin novedad: "responde ÚNICAMENTE con el token [SILENT] y nada más (sin texto antes ni después)".
4. Camino con novedad: campos exactos del reporte + enlace/acción que SIEMPRE debe incluir, y cierre anti-alucinación: "no inventes correos; si la tool falla, responde [SILENT]". Trade-off a decidir por watch: silencio total ante fallo de tool vs fallar ruidoso (si el watch es crítico, mejor failure-deliver).

Edición: `hermes cron edit <job_id> --prompt "..."` (escapar `"`, `$` y backticks para shell). El OK del CLI ("Updated job") NO muestra el prompt resultante: verificar releyendo `jobs.json` del perfil antes de dar el cambio por bueno.

Caso real 23-sep-2026: job `57d1df6d1ab4` "Meta gambling approval — inbox watch" (perfil default, cada 120m, deliver telegram) reportaba cada 2 h cualquier correo de Meta (incluidos rechazos de anuncios individuales) como novedad de la autorización de anuncios de juegos; reescrito con la plantilla de arriba: clasifica en silencio y solo habla si hay respuesta a ESA autorización (aprobación, rechazo o pedido de información).

## Pitfalls

- **403 Forbidden desde Python al postear un webhook de Discord:** con el `User-Agent` por defecto de `urllib` (`Python-urllib/3.x`) Discord/Cloudflare responde `403` aunque la URL sea correcta (`curl` sí pasa). Fija un `User-Agent` propio en la petición. No lo confundas con token inválido (`401`/`50027`) ni con contenido inválido (`400`).
- **`hermes cron run <id>` responde «Job is already being fired by the scheduler; not run again»** si hay un `fire_claim` vivo: el claim caduca a los **300 s** (`_claim_is_live(..., 300)`). Pasa cuando matas un `cron run` a mitad (timeout del tool) y el claim queda huérfano. Espera 5 min y reintenta; NO edites `fire_claim` a mano en `jobs.json`.
- **Matar un `cron run` a mitad** deja la corrida como `unknown` y sin `last_status`: el job NO queda roto, pero su resultado no es evidencia de nada. Dispara con `background=true` y verifica por el canal + `cron/output/<id>/`.
- **Jobs de otro perfil:** usa `hermes -p <perfil> cron list|create|edit|run|remove` (el CLI es profile-aware). `cronjob_manage` y la edición a mano de `jobs.json` solo ven el perfil actual — y editar el JSON mientras el ticker escribe es una carrera.
- Declarar «verificado» con `last_status: ok`: el run verde puede no haber entregado nada.
- Confundir identidad con destino: un mensaje puede aparecer como bot o como webhook; el reply/continuación solo funciona con el bot.
- Restringir la lista de jobs a mover sin decirlo: enumerar exactamente qué jobs cambian y qué jobs NO, para que el usuario pueda corregir en un mensaje (evita re-preguntar).
- Al cambiar de canal, los mensajes previos con instrucciones de aprobación quedan en el canal viejo: recordar al usuario dónde aprobar ahora.
- Si el job corre bajo el ticker root del Desktop (ns host), el `.md` de salida queda `root:root` y no se puede leer como uid 10000; leerlo vía `ssh dev`. Ver `scheduled-job-diagnosis` y `hermes-cron-runtime-verification` (user-owned) para el mapa de namespaces.
