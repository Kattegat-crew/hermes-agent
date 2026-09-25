---
name: hermes-multiprofile-cron-ops
description: "Use when creating per-profile Hermes cron jobs on a VPS."
tags: [hermes, cron, perfiles, docker, gateway, devops]
version: 1.0.0
author: Ragnar
license: MIT
metadata:
  hermes:
    tags: [hermes, cron, profiles, docker, gateway, multiplex, engram, devops]
    category: devops
    related_skills: [hermes-production-deployment, guardado-doble-memoria, hermes-admin-operations]
---

# Hermes Multi-Profile Cron Ops (VPS con gateway Docker)

Crear, probar y verificar crons por perfil en un VPS donde Hermes corre en Docker con
gateway multi-perfil (multiplex_profiles, un s6 `gateway-<perfil>` por perfil servido).
Aplica a flotas de agentes de clientes (Bob/helmer/jacqueline/...) y a cualquier job
que deba vivir en el `cron/jobs.json` de UN perfil y no en el default.

## Regla de oro — el CLI del host NO sabe de perfiles

En estos despliegues `/usr/local/bin/hermes` es un wrapper `docker exec` **sin**
`-e HERMES_HOME`. Por tanto:

- `hermes cron create` (o cualquier comando de perfil) ejecutado desde el host escribe
  SIEMPRE en el perfil default, aunque hagas `cd` al home del perfil o exportes
  `HERMES_HOME` en el shell del host. Verificado 24/08: 5 jobs "por perfil" acabaron
  en default.
- Método correcto: pasar `HERMES_HOME` **dentro** del contenedor:

```bash
docker exec -e HERMES_HOME=/opt/data/profiles/<perfil> hermes-agent hermes cron create \
  "0 23 * * *" "<prompt>" --name <job> --deliver local \
  --script <script.py> --skill <skill-a> --skill <skill-b> </dev/null
```

- Añade SIEMPRE `</dev/null`: `hermes cron create` consume stdin y un heredoc
  `bash -s` se corta tras el primer job (síntoma: solo el 1er perfil de un loop crea
  el cron). Alternativa: un comando SSH por perfil.
- Para default el home es `/opt/data` (no `/opt/data/profiles/default`).

## Probar un cron sin bloquear el SSH

`hermes cron run <id>` ejecuta el job COMPLETO incluido el LLM: tarda 2-3 min. El
foreground SSH da timeout a los 60s pero el job sigue corriendo en el contenedor.
No lo trates como error.

```bash
nohup docker exec -e HERMES_HOME=<home-perfil> hermes-agent hermes cron run <job_id> \
  </dev/null >/tmp/cron_run_<perfil>.log 2>&1 &
# esperar ~2-3 min y verificar en jobs.json (no en la salida del CLI):
python3 -c "import json; d=json.load(open('<home-perfil>/cron/jobs.json')); [print(j['id'], j.get('last_status'), j.get('last_error')) for j in d['jobs'] if j.get('name')=='<job>']"
```

- El output real de cada ejecución queda en `<home>/cron/output/<job_id>/<ts>.md` —
  leer el FINAL del `.md` para confirmar qué guardó (no confiar solo en last_status).
- `hermes cron status` desde el contexto de un perfil puede decir "Gateway is not
  running" aunque el multiplexor del host lo sirva: cada perfil tiene su propio
  `s6-supervise gateway-<perfil>` que dispara sus crons a la hora programada.

## Rate limits al probar en paralelo

Lanzar varios `cron run` a la vez (misma hora, mismo proveedor LLM) produce
`RuntimeError: HTTP 429 — Too Many Requests` en algunos. Es transitorio: reintentar
en secuencia (o esperar al siguiente tick). No es un fallo de configuración.

## Script de recolección diaria (patrón data-collection)

Para un cron que resuma el día (ej. guardado Engram + memoria nativa), el scheduler
ejecuta el `script:` ANTES del agente e inyecta su stdout al prompt. El recolector
`scripts/daily_session_report.py` lee la `state.db` de sesiones de una jornada
(quién habló, título, mensajes, tool calls, último prompt del usuario).

**Aislamiento por copia**: el script resuelve su DB relativa a sí mismo
(`scripts/../state.db`) → copiándolo al `scripts/` de CADA perfil lee automáticamente
la DB de ESE perfil. Verificación: ejecutarlo y comprobar la DB resuelta.

No requiere toolset `terminal` en el agente del cron: la recolección la hace el
scheduler; el agente solo necesita la herramienta `memory` + MCP (si el job define
`enabled_toolsets`, incluir `memory`; dejarlo `null` hereda todos).

## Verificación de seguridad — SEMÁNTICA, no substring

Comprobar aislamiento con `"all_projects=True" in prompt` da FALSO POSITIVO: el
prompt AISLADO contiene la cadena como prohibición ("NUNCA uses all_projects=True").
Para verificar:
- Aislados: `"NUNCA uses all_projects=True" in prompt`
- Completos: `"all_projects=True" in prompt and "NUNCA uses" not in prompt`

## Verificación post-despliegue (checklist)

1. Script en `<home>/scripts/` con uid 10000 (`install -m 0644 -o 10000 -g 10000`).
2. Un solo job por perfil en su `cron/jobs.json` (no duplicados en default).
3. `cron run` en background → `last_status: ok` y `last_error: None`.
4. Output del `.md` confirma el resultado (o `[SILENT]` = correcto cuando no hay
   actividad: el agente no inventa memorias).
5. Prompt correcto según variante (completo vs aislado) — punto 4 de arriba.

## Referencias

- `references/2026-08-24-cron-guardado-diario-prod.md` — rollout real del cron de
  guardado diario en prod (169.58.189.222): inventario de perfiles, aislamiento
  Engram lógico/físico, errores cometidos, job IDs.
- `scripts/daily_session_report.py` — recolector de actividad diaria listo para
  copiar al `scripts/` de cada perfil.

## Pitfalls

- Wrapper del host sin `HERMES_HOME` → todos los jobs al default (limpiar con
  `docker exec -e HERMES_HOME=<home> hermes-agent hermes cron remove <id>`).
- `cron run` en foreground SSH → timeout aparente (el job sigue; verificar por
  jobs.json).
- Heredoc `bash -s` con `hermes cron create` → se corta tras el 1er job (usar
  `</dev/null` o un SSH por perfil).
- 429 al probar N perfiles en paralelo → reintento secuencial.
- Perfiles cliente: su MCP engram puede tener `--project` propio (aislamiento
  lógico) SIN engram.db física — auditar con `find ... -name engram.db` y
  `grep -A4 engram config.yaml` antes de asumir aislamiento físico.