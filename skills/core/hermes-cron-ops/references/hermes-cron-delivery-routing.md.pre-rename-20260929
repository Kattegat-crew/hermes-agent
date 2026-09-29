---
name: hermes-cron-delivery-routing
description: Rules for which profile delivers cron output to which chat
version: 1.0.0
author: Ragnar
metadata:
  hermes:
    category: devops
    tags: [cron, whatsapp, delivery, routing, profiles]
---

# Hermes Cron Delivery Routing Skill

Regla de quién entrega qué a qué chat en la flota Hermes, verificada en PROD el 16-sep-2026 tras corregir en voz alta un diagnóstico propio impreciso.

## When to Use
- Crear o mover crons que entregan por WhatsApp, Discord u otro canal.
- Diagnosticar `platform 'whatsapp' not configured/enabled` en un cron.
- Decidir desde qué perfil corre un job que debe notificar a un chat concreto.

## Donde Vive el Script de un Job (no_agent)
El campo `script` se resuelve RELATIVO a `<HERMES_HOME>/scripts/` (= `/opt/data/scripts/` dentro del contenedor), **no** en `home/.hermes/scripts/`. Un script mal ubicado produce `Script not found: <ruta>`, el job queda en `last_status: error` y el engine publica el aviso de fallo EN EL CANAL DE DESTINO (borrable por la API si el bot tiene Manage Messages).

El mismo job lo tickean el gateway del contenedor y el backend del Desktop, con arboles distintos → el envoltorio debe resolver el proyecto por runtime:

```sh
BASE=/opt/data
[ -f /opt/data/config.yaml ] || BASE=/root/hermes-agent/data
exec python3 "$BASE/<proyecto>/scripts/<script>.py" --dias 3
```

Tras crear un job `no_agent`, verificar con una corrida real: `Result: ok` + `Status: silent (empty output)` cuando no hay novedad (evidencia: cron `9d5a5c4868f4`, 16-sep-2026).

## The Rule (verificada en PROD)
1. Cada chat lo entrega el perfil al que está RUTEADO en `profile_routes` (config del gateway). Ese ruteo primario decide TODO.
2. `platforms.whatsapp.enabled: false` NO bloquea la entrega a los chats propios del perfil. Evidencia: `nancy` saca 12 recordatorios diarios con `enabled: false`; `helmer` entrega su informe diario de ventas sin interrupción.
3. El error `platform 'whatsapp' not configured/enabled` es el FALLBACK fallido, no la causa raíz. Ocurre cuando el perfil intenta entregar a un chat que NO es suyo (el ruteo primario falla cerrado) y además su config de plataforma está apagada. Síntoma de chat equivocado.
4. Consecuencia operativa: el diario de Helmer sale del perfil `helmer` y el de Yulieth del perfil `yulieth`. NO centralizar entregas en `default` por comodidad.

## How to Verify (antes de confiar en una entrega)
1. Leer `profile_routes` y confirmar qué perfil es dueño del chat objetivo.
2. Sondeo read-only de la sesión de WhatsApp del host (device-list, lid-mapping) con tokens enmascarados ([REDACTED]).
3. Prueba de canal (F0) - job temporal que manda UN mensaje real al chat objetivo, con autorización previa del Admin porque el mensaje es real y visible.
4. Para probar un **fallo**: no basta `Updated job:` del CLI. Crear un job temporal en el perfil de origen con script `exit 7` y el `failure_deliver` en prueba, dispararlo con `cron run <id>`, y leer en el `jobs.json` el campo `last_delivery_error` + en el log `cron.scheduler: delivered to ...`. Recien ahi se sabe si la ruta existe.
5. Los **ids de job** se obtienen del `jobs.json` del perfil (filtrar por `name`), NO parseando `hermes cron list`: su formato no expone el id de forma estable y `grep` sobre el devuelve vacio.
6. `cron run` (manual) corre fuera del gateway: puede responder `Ran now: failed` en un job que si entrega por scheduler, y al revés. La linea `delivered to` del log es la unica evidencia de entrega; `Ran now: succeeded` y `exit 0` no lo son.

## Pitfalls
- `enabled: false` en la plataforma NO prueba que el perfil no pueda entregar. Medir con ruteo + prueba real antes de afirmar incapacidad.
- Un perfil solo entrega a SUS chats. Para un chat ajeno, o se agrega el ruteo o corre el job desde el perfil dueño. Ejemplo real - el PDF mensual de Helmer al chat del Admin falla desde `helmer` con el error del punto 3 y corre en `default` (dueño de ese chat).
- Corregir en voz alta el diagnóstico propio cuando la evidencia lo contradice (nancy demostró que la regla anterior estaba mal) - preferencia del Admin.

## Avisos de fallo (`failure_deliver`) - misma regla, verificado 16-sep-2026
`--failure-deliver` NO salta la regla del ruteo: un job del perfil `helmer` con `--failure-deliver whatsapp:<chat del default>` **no entrega** y deja `last_delivery_error = platform 'whatsapp' not configured/enabled` en el job. Probado con un job que falla a proposito (exit 7). Consecuencia: **no se puede enrutar el fallo de un job de un perfil al chat de otro perfil**.

Patron que SI funciona - un vigilante en el perfil dueno del chat destino:
1. Job en el perfil dueno (aqui `default`, que es quien puede escribirle a Bob), `no_agent`, cada 30 min.
2. El script lee los `jobs.json` de los perfiles implicados y reporta los que quedaron en `last_status=error`.
3. Dedup por `(job_id, last_run_at)` en un JSON propio - un mismo fallo se avisa UNA vez.
4. Sin novedades: stdout vacio (silencio). Implementacion `scripts/alertas_ventas.py` en PROD + job `6a65ad887c5b`.

Ventaja sobre el flag: cubre jobs `deliver: local` (que antes fallaban mudos) y tambien los que entregarian el error al cliente. `failure_deliver: local` explicito es mejor que dejarlo en None cuando no aplica - dice "no notifica, lo cubre el vigilante".

## Verification
- Después de cualquier cambio de ruteo - correr la prueba F0 y confirmar llegada en el chat real. Exit 0 del job NO es evidencia de entrega.