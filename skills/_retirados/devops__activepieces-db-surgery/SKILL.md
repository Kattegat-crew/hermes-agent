---
name: activepieces-db-surgery
description: "Use when: crear/editar flows ActivePieces en su Postgres."
version: 1.0.0
author: Sindri (Producer)
metadata:
  hermes:
    tags: [activepieces, postgres, flows, jwt, docker]
    related_skills: [vps-host-repo-access, video-ai-generator]
license: MIT
compatibility: hermes
---

# ActivePieces: crear/editar flows vía Postgres (receta verificada)

## When to use
Cuando hay que crear un flow/workflow nuevo en ActivePieces, inyectarle credenciales/headers a un piece-http existente, o auditar flows — sin UI. Probado 28/08/2026 en AP de NeuralCrew (VPS prod .222, contenedores ap-app/ap-db/ap-worker/ap-redis; UI :8088).

## Topología del caso NeuralCrew (ACTUALIZADA 29/08 tras migrar AP a prod .222)
- AP vive en .222 (Tailscale 100.73.30.29); el reel-worker en dev .250 (Tailscale 100.86.8.81:8090). Los flows POSTean a `http://100.86.8.81:8090` — la URL vieja `10.0.1.1:8090` quedó MUERTA con la migración (dentro de ap-app no resuelve; probado 29/08). Verificar alcance: `docker exec ap-app curl -m 8 http://100.86.8.81:8090/health`.
- Acceso: SSH root@100.73.30.29 con la key del host → `docker exec -i ap-db psql -U postgres -d activepieces < /tmp/x.sql` (el `-f /tmp/x.sql` NO funciona: busca el archivo DENTRO del contenedor).
- Publicación: `flow.publishedVersionId` SÍ existe en esta versión de AP (los flows del reel pipeline lo tienen apuntando a su última versión). Sin embargo AP ejecuta la versión DRAFT — editar la fila DRAFT de `flow_version` alcanza; setear publishedVersionId solo alinea UI/estado.
- Webhook de producción por API: `POST http://localhost:80/api/v1/webhooks/<flowId>` dentro de ap-app (la ruta `/v1/...` SIN prefijo `/api` devuelve el HTML del SPA, no la API). Un POST de prueba con body mínimo devuelve `{}` 200 y genera un run; el paso piece-http fallará (400) si el body no pasa la validación del worker — eso confirma auth+conectividad sin crear jobs reales.

## Reglas del esquema (verificar con information_schema antes de fiarse — AP cambia entre versiones)
- IDs de `flow`/`flow_version` son `varchar(21)` base62 (tipo `TiRdZ7xkbD86d2eM7B9KJ`). **NO usar `gen_random_uuid()`** (36 chars → error de longitud). Generar en Python: `secrets.choice(ALPHABET)` 21 veces.
- NOT NULL de `flow_version`: `connectionIds` y `agentIds` son **ARRAY** (`ARRAY[]::text[]`, un JSON `'{}'` falla), `notes` es **JSONB pero AP lo crea SIEMPRE como ARRAY** (`'[]'::jsonb` — un `''` falla y un objeto `'{}'::jsonb` crashea la UI), `valid` bool, `state` ('DRAFT'), `trigger` jsonb.
- **Pitfall `notes` objeto (29/08):** INSERT con `'{{}}'::jsonb` deja `notes={}` y al abrir el flow la UI explota: `Unexpected Application Error! t.map is not a function` (el front hace `.map` sobre notes). Fix: `UPDATE flow_version SET notes='[]'::jsonb WHERE "flowId"=(SELECT id FROM flow WHERE "externalId"='<x>') AND jsonb_typeof(notes)='object';` + usuario refresca el navegador.
- `flow`: `externalId` (nombre visible/URL-safe), `status` ('ENABLED'), `deleted`='false' (check constraint — no null).
- El header/credencial de un piece-http vive en `trigger->nextAction->settings->input->headers` (jsonb). Trigger webhook = `settings.triggerName: catch_webhook`, piece `@activepieces/piece-webhook`; acción = piece `@activepieces/piece-http` action `send_request` con `url/method/body/headers/body_type`.

## Cómo pasar el SQL sin morir en el quoting
El quoting anidado docker→ssh→bash→psql rompe cualquier SQL con comillas inline. **Receta ganadora**: script Python que (1) construye el JSON con `json.dumps`, (2) escapa literales SQL duplicando `'`, (3) base64 del .sql, (4) SSH que ejecuta `echo <b64> | base64 -d > /tmp/x.sql && docker exec -i ap-db ... < /tmp/x.sql`. Correr ese Python por stdin en un contenedor con la key SSH montada:
`docker run --rm -i -v /root/.ssh:/keys:ro alpine sh -c 'apk add -q python3 openssh-client; python3 -' < inject.py`
(Usar `INSERT ... SELECT FROM flow WHERE "externalId"=...` para resolver el FK sin hardcodear ids.)

## Verificación obligatoria después de escribir
1. `SELECT` de vuelta: flow ENABLED + flow_version con el header correcto (verificar prefijo/sufijo del token contra uno freshly-minted).
2. E2E funcional: POST real al endpoint del worker con token minteado igual → esperar el código de éxito (202 en el worker AKARI; sin token → 401).
3. Los tokens JWT nunca se imprimen en el chat; generar y usar directo en el payload.

## Modelo de trigger canónico (reel pipeline, 28/08)
`webhook catch` → `piece-http POST http://100.86.8.81:8090/jobs` con `Authorization: Bearer <JWT firmado con REEL_WORKER_JWT_SECRET>` y `body: {"data": "{{trigger.body}}"}` (URL corregida 29/08; los 3 flows compartían la 10.0.1.1 muerta). Flows existentes: `reel-orchestrator` (9wusDPr3RgmVXvZt8tszm), `reel-callback` (v6pQk2m8RgVnLx4tAeBzJ), `video-generator` (TiRdZ7xkbD86d2eM7B9KJ) — todos ENABLED, publicados y E2E verificados 29/08 (mintear JWT con scripts/make_worker_token.py del repo video-ai-generator).
