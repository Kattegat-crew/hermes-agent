---
name: peer-agent-collaboration
description: "Use when coordinating work with another Hermes agent."
version: 1.0.0
author: curator-ragnar
category: autonomous-ai-agents
metadata:
  hermes:
    tags: [multi-agent, handoff, verificacion, bot-chat, loop, evidencia]
    related_skills: [multi-agent-shared-channel, peer-report-verification, independent-infra-audit]
---

# Trabajar con otro agente Hermes: handoff, verificación y cierre

**Cuándo:** un humano te pide «háblale a X», «acuerden un plan entre los dos», «que Roshi lo revise»,
o vas a citar/consumir un entregable de otro agente. También cuando el intercambio empieza a
retroalimentarse (un mensaje tuyo por cada uno suyo).

Regla base: el par es un **par**, no un subordinado ni una fuente de verdad. Se le manda el encargo con
contexto completo, se verifica lo que entrega con evidencia viva, y el intercambio **se cierra**.

## 1. Mandarle un mensaje a otro perfil (Bot Chat)

Comando verificado (DEV, 12-sep-2026):

```bash
HERMES_HOME=/opt/data /opt/hermes/bin/hermes -p <perfil> chat --in "~" -c "Bot Chat" \
  --create-if-missing -Q --query-file <archivo.txt>
```

- `-c "Bot Chat"` es el alias corto de `--continue` (nombre de **sesión**, no de chat);
  `--create-if-missing` la crea si no existe.
- **PITFALL que cuesta un intento:** NO quites `HERMES_HOME`. Sin él el CLI resuelve otro home y responde
  `Error: Profile '<perfil>' does not exist` aunque el perfil exista. (El scheduler de cron sí lo
  elimina, pero porque el suyo apunta al home del perfil emisor; en tu shell el correcto es el base.)
- `hermes` **no está en el PATH del contenedor**: usa `/opt/hermes/bin/hermes`.
- Verifica que el perfil existe antes de enviar:
  `HERMES_HOME=/opt/data /opt/hermes/bin/hermes profile list`.
- El mensaje va en **archivo + `--query-file`** (no `-q`): comillas, `$` y backticks llegan verbatim.
- Primera línea del mensaje: `[Mensaje del perfil <emisor> — no es el usuario]`, para que el par no lo
  atribuya al humano.
- **Verifica la entrega en su estado**, no en el eco del comando: `/opt/data/profiles/<perfil>/state.db`,
  tabla `messages`, filtrando por `session_id`. El turno del par tarda minutos: lanzalo en background con
  notify y sigue trabajando.
- El par **no puede** contestarte por el mismo canal: su respuesta queda en su Bot Chat. Lée la del
  `state.db` y tráela al humano tú.

## 2. Hablarle a una PERSONA (no a un perfil)

```bash
/opt/hermes/bin/hermes send --to whatsapp:<chat_id> --file <txt> --json
```

Admite `telegram:<id>`, `discord:#canal`, `plataforma:chat_id:thread_id`; `--list` enumera destinos y
`/opt/data/channel_directory.json` trae los DM con nombre. El `message_id` del JSON **es** la evidencia
de entrega. Regla de ruteo: el resumen de flota y lo operativo va al humano; al agente se le manda
trabajo con contexto, no resúmenes.

## 3. Antes de acordar: criterios medibles y frontera de archivos

- Cambia cada «quedamos en que…» por un **criterio verificable** (comando + salida). Si el plan promete
  «40 tests, uno por paso» y los pasos no están escritos en ninguna parte, pide el anexo **antes** de
  firmar.
- Reparte por **frontera de archivos**: «yo no toco tu script, tú no tocas motor/worker». Hace trivial
  saber de quién es un fallo y evita la fusión a ciegas.
- Acuerda **secuencia con dependencias** y di qué es $0 y qué necesita firma de gasto.
- Exige la prueba de **genericidad** cuando el plan promete generalizar (un caso ficticio que valide sin
  tocar código): es gratis y es lo único que demuestra que no está cableado a un cliente.
- **Un acuerdo por chat NO está cerrado**: pide el documento corregido **commiteado en git** y verifica
  `HEAD == origin/main`. Lo que se verifica es el commit, no el mensaje.

## 4. Verificar lo que entrega el par (no creer, medir)

Checklist corto (caso trabajado completo en `references/worked-case-contrato-campana.md`):

1. **Baseline primero:** `git fetch` + `rev-parse HEAD` vs `origin/main`; «pusheado» se comprueba.
2. **Corre SU suite tú mismo**, en el runtime real, y compara el conteo con el que declara.
3. **Audita los tests que comparan:** un test que normaliza (tildes, `lower()`, `casefold`) antes de
   comparar convierte en verde el defecto que dice verificar. Léelo en el test, no lo deduzcas del
   resultado.
4. **Recomputa contra la FUENTE**, campo por campo, no contra su resumen: así aparece lo que no migró
   (bloques completos de listas permitidas, conteos que no cuadran con el índice).
5. **Contradicciones internas:** una entidad excluida dentro de la lista de «activas» es un bug que el
   flujo siguiente cobra (ofrecer una sede cerrada).
6. **Higiene de dueños:** archivos `root:root` en un repo del usuario del servicio rompen «0 archivos
   ajenos» y pueden bloquear worker/crons.
7. **Valor en crudo:** un arreglo puede restaurar el texto y no el dato (`"0728" != 728`).

Cuando el par **te** corrige con evidencia, dilo en la misma respuesta y cítale el mérito: el que te
corrige con comando te ahorra un error futuro.

## 5. Higiene del intercambio (regla anti-loop)

- **Un intercambio por encargo.** Si contestas automáticamente cada mensaje del par, entras en un ciclo
  que quema tokens, satura al humano y no avanza: cada vuelta de «¿de acuerdo?» / «de acuerdo, y
  además…» es el loop.
- **Condiciones de parada explícitas:** (a) el par entregó y tú verificaste; (b) hay una decisión que
  **sube al humano**; (c) el humano pidió cortar.
- Cuando el humano dice «si caíste en loop, interrumpe la interacción»: **corta en seco**. No mandes el
  mensaje de cortesía de cierre ni un resumen periódico; deja el estado en tu reporte al humano y no
  vuelvas a escribirle al par hasta que haya un encargo nuevo.
- Los bugs que encuentres en archivos del par son un **entregable para el humano** (con archivo y línea),
  no una excusa para abrir otra ronda con el par por tu cuenta.

## 6. Probar flujos que exigen firma humana

Usa un **marcador honesto** del test en el campo de firma:
`--por "<Nombre> (CTO) via chat <fecha> — prueba E2E autorizada"`. Queda en la bitácora, es trazable y
no fabrica una aprobación que nadie dio. Nunca firmes con el nombre del humano que no firmó.

## Pitfalls

- **Correr el pipeline del par desde el contenedor falla** (`.venv` del host):
  `ssh dev 'cd <repo> && sudo -u hermes env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp HOME=/tmp .venv/bin/python …'`.
  Con `git` como root hace falta `git -c safe.directory=<repo>` (si no: *dubious ownership*).
- **En el host no existe un grupo llamado `hermes`** (uid/gid 10000): `chown hermes:hermes` falla; usa
  numérico `chown -R 10000:10000`.
- **Guarda el log completo a archivo** (`| tee <log>`): en una corrida E2E los fallos se ven en el log, no
  en la última línea del resumen.
- **No confundas «hay respuesta» con «hay acuerdo»**: el par puede entregar sin aceptar tus condiciones;
  el OK condicionado se acepta explícitamente y se cierra en git.

## Soporte

- `references/bot-chat-messaging.md` — comandos exactos, el intento fallido y cómo se verificó la entrega.
- `references/worked-case-contrato-campana.md` — regresión campo a campo del contrato de campaña del par.
- `references/pipeline-e2e-dry-run-recipe.md` — E2E de un pipeline de contenido en `--dry-run` ($0), qué
  reportar y los bloqueos que aparecieron.

## Relación con otras skills

`multi-agent-shared-channel` (varios agentes en un mismo canal), `peer-report-verification` (verificar el
informe de un par) e `independent-infra-audit` cubren territorio adyacente y **hoy son user-owned**:
`skill_manage` las rechaza con *not curator-managed*. Si quieres que este contenido viva en ellas, pide
`hermes curator adopt <nombre>`; hasta entonces este skill es el homólogo editable.
