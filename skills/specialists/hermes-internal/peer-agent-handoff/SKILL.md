---
name: peer-agent-handoff
description: "Use when handing work to or verifying a peer agent."
version: 1.0.0
category: autonomous-ai-agents
author: Ragnar
metadata:
  hermes:
    tags: [multi-agente, handoff, bot-chat, acuerdo, verificacion, perfiles, roshi, ragnar]
    category: autonomous-ai-agents
    related_skills: [hermes-multiprofile-gateway-ops, agent-worktree-orchestration, admin-reporting]
---

# Peer-agent handoff — hablarle a otro perfil y aceptar su entrega

Trabajo que **cruza entre agentes** de la flota: pedirle algo a otro perfil (Roshi, Bragi, Sindri,
Vigía, un especialista), cerrar un acuerdo con él, y decidir si su entrega se acepta. El Admin lo pide
en frases cortas: «envíaselo a Roshi», «acuerden un plan entre los dos», «¿qué opinas de este plan?».

Regla base: lo que otro agente reporta es un **self-report**. Se verifica con tus comandos; el
entregable de tu lado es `verificado X/N` con el comando detrás de cada verificación.

## 1. Hablarle a otro perfil y que ACTÚE (bot-chat) — receta verificada 12-sep-2026

Inyecta el mensaje como turno real en la sesión "Bot Chat" del otro perfil. Es el mismo mecanismo que
usa el scheduler para `deliver: bot-chat:<perfil>`.

```bash
cd /opt/data && HERMES_HOME=/opt/data /opt/hermes/bin/hermes -p <perfil> chat \
  --in "~" -c "Bot Chat" --create-if-missing -Q --query-file /opt/data/drafts/<mensaje>.txt
```

- `-c "Bot Chat" --create-if-missing`: reanuda (o crea) esa sesión. La salida lo confirma:
  `↻ Resumed session <id> "Bot Chat"`.
- `--query-file`: el texto viaja **verbatim** (comillas, `$(…)`, backticks intactos). Escribir el mensaje
  a archivo y pasarlo así elimina el infierno de quoting.
- **`HERMES_HOME` NO se quita.** Con `-p <perfil>` hay que dejarlo apuntando a la base (`/opt/data`).
  Si se unset, el CLI resuelve otro home y falla con `Error: Profile '<perfil>' does not exist` **aunque
  el perfil exista**. Pre-flight: `HERMES_HOME=/opt/data /opt/hermes/bin/hermes profile list`.
- Corre como `hermes` (uid 10000) → no deja archivos `root:root`.
- Es un agente completo (minutos): lanzarlo en background con notificación y **no** dar por entregado por
  el exit code del lanzador; confirmar en la BD del par (§2).
- Marca el emisor en el texto (`[Mensaje del perfil default (Ragnar) — no es el usuario…]`) para que el
  par no lo confunda con su humano, y pídele la contrapropuesta explícita («OK o contrapropuesta»).

## 2. Leer su respuesta (no te llega sola)

La respuesta queda en **su** sesión, no en tu chat: `/opt/data/profiles/<perfil>/state.db`, tabla
`messages`, `session_id` = el de "Bot Chat", `role='assistant'` (abrir read-only con
`file:…?mode=ro`). La notificación de fin del proceso solo trae el resumen que el par le mandó a *su*
humano. Antes de citarlo, comprueba que ya escribió (actividad reciente en esa sesión).

## 3. Acordar (cuando el Admin dice «acuerden entre los dos»)

El entregable no es el intercambio de mensajes: es un **acuerdo escrito** con (1) secuencia y
dependencias, (2) reparto por unidad con **frontera dura de archivos** («yo no toco X, tú no tocas Y»),
(3) regla de evidencia (ninguna unidad se cierra sin comando + salida), (4) criterio de aceptación por
unidad, y (5) la exigencia de **commitearlo al repo** (`docs/planes/…`): un acuerdo que solo vive en un
chat no es un acuerdo.
Separa lo que cada uno hace **sin firma** (trabajo $0: contrato, tests, dry-runs) de lo que exige firma
humana: el gasto y las ventanas en producción se escalan al Admin en una línea con su tope declarado,
nunca se deciden entre agentes. Y si te corrige, acéptalo por escrito («me corrijo: …») devolviéndole un
matiz verificado, no un «ok».

## 4. Aceptar su entrega: verificación con capa extra

1. **Baseline primero.** Si dice «commiteado y al día», compruébalo (`git fetch` + `rev-parse HEAD` vs
   `origin/main`). Un baseline viejo invalida todo lo demás en silencio.
2. **Reejecuta tú su evidencia.** Validador/CLI y **su suite completa**, con el intérprete correcto y
   como el usuario dueño del repo (ver Pitfalls). «36/36 verdes» se convierte en dato solo si lo corres tú.
3. **Regresión contra la fuente de verdad** si el artefacto migra o reemplaza algo (§5).
4. **Higiene de lo que acaba de escribir.** `find . -not -user hermes -not -path './.git/*'`: un par que
   corre como root deja rutas `root:root` que rompen el criterio «0 archivos ajenos» y pueden bloquear a
   los procesos hermes (worker, crons). Se reporta; el `chown` se **propone**, no se ejecuta.
5. **Devuelve hallazgos priorizados**, con el criterio de aceptación de la unidad siguiente — no una
   lista plana. Y reconoce con el mismo detalle lo que el par hizo bien.

## 5. Regresión de un artefacto que migra (la parte que más se salta)

Que valide contra su propio schema no dice nada: el schema solo prueba lo que el autor pensó en meter.
Compara contra la **fuente vieja**, campo por campo, buscando cinco clases de pérdida:

- **Conjuntos que desaparecen.** Diff los *sets* de valores (cifras permitidas, números, frases
  requeridas y prohibidas, listas de vetos), no solo los campos presentes. El hallazgo más caro aparece
  aquí: bloques enteros que la migración pierde en silencio y el consumidor deja de chequear sin fallar.
- **Transformación silenciosa del texto.** Compara literal. Tildes borradas no son cosméticas: el
  matching aguas abajo (vetos, frases prohibidas) deja de casar y los prompts/rótulos salen sin tildes.
  Regla: verbatim; si hay que normalizar, se normaliza en los dos lados.
- **Conteos y contradicciones internas.** Recuenta con script contra la fuente, nunca a ojo. Y busca
  entradas presentes a la vez en dos listas opuestas (una sede en `activas` y en `excluidas`): el
  consumidor cobra esa contradicción aguas abajo.
- **Deriva de identificadores.** Un formato canónico declarado que no coincide con ningún id vivo debe
  marcarse **forward-only + alias**: renombrar lo publicado rompe URLs y dashboards. Nada se renombra en
  PROD sin ventana.
- **Alcance real vs etiqueta.** Un bloque llamado `activas` que contiene una entrada histórica o excluida
  es una etiqueta mentirosa: el consumidor la usará como lista de opciones válidas.

## Pitfalls

- **No confundas «procesado» con «entregado».** El lanzador en background devuelve 0 al arrancar; el error
  real aparece en su salida (p.ej. `Profile … does not exist`). Lee la salida del proceso antes de
  reportar el envío al Admin.
- **Namespace ajeno.** Las rutas del par son de *su* entorno (contenedor `/opt/data/…` = host
  `/root/hermes-agent/data/…`). Un `No such file` al medir su artefacto suele ser esto.
- **`.venv` del host usado desde el contenedor** → `Could not find platform independent libraries`.
  Corre por `ssh dev` y **como el usuario dueño**, no como root, para no dejar `__pycache__` ajeno:
  `ssh dev 'cd /root/<repo> && sudo -u hermes env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp HOME=/tmp
  .venv/bin/python -m pytest tests/<archivo> -q -p no:cacheprovider --basetemp=/tmp/pytest-…'`.
- **El par commitea mientras tú revisas.** Su HEAD puede haber avanzado y un «pendiente: sin pushear» tuyo
  quedar viejo en minutos. Re-verifica git justo antes de reportar.
- **No cierres un acuerdo con decisiones que no son tuyas.** Gasto, ventanas en producción y renombrados
  publicados van al Admin; tú propones con tope declarado.

## Soporte

- `references/regresion-contrato-campana-2026-09-12.md` — caso trabajado: regresión campo a campo de un
  contrato de campaña nuevo contra su fuente (`datos-duros.yaml`, `index.json`, `registry.json`), con los
  seis hallazgos y el comando de cada check.

## Relación con otras skills

`peer-report-verification` (devops) cubre la verificación de informes de un par y `hermes-team-ops`
(communications) el roster y el handoff de crons: **ambas son user-owned**, así que esta skill recoge las
mecánicas que no se pueden añadir ahí. Si el Admin las adopta (`hermes curator adopt <nombre>`), lo de
arriba debería fusionarse en ellas en vez de duplicarse.
