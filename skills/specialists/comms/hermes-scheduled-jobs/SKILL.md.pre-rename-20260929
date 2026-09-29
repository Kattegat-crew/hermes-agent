---
name: hermes-scheduled-jobs
description: "Use when creating or debugging Hermes cron jobs."
tags: [cron, hermes, drift-skip, watchdog, multiplex, perfiles]
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [cron, scheduled-jobs, drift_skip, fallback, watchdog, multiplex, perfiles]
    category: devops
    related_skills: [hermes-team-ops, hermes-multiprofile-cron-ops, hermes-skills-provisioning]
---

# Hermes Scheduled Jobs — mecánica de crons (crear y diagnosticar)

Cómo crear y mantener crons en Hermes (especialmente en configuración
multi-perfil / multiplexada): pin de proveedor/modelo, drift_skip, sintaxis de
expresión, skills de los jobs, avisos falsos del CLI y rescate con watchdog.
Validado 26/08/2026 al implementar 9 crons `guardar-diario-memoria` escalonados
en perfiles de bots (comms, bragi, sindri, freyja, vili, ullr, heimdall,
hermodr, brokkr).

## When to Use

- Crear un cron en un perfil concreto (no el default).
- Un cron falla sin traceback claro (`last_status=error`, sin modelo llamado).
- El CLI dice "Gateway is not running" y no sabes si el job correrá.
- Quieres que un cron sobreviva a fallos del proveedor o del proceso.

## Prerequisites

- CLI hermes del contenedor: `/usr/local/bin/hermes` (o `/opt/hermes/bin/hermes`).
- Para crons de un perfil SIEMPRE pasar HERMES_HOME dentro del contenedor:
  `HERMES_HOME=/opt/data/profiles/<p> hermes cron create ...`
- Ruta real de jobs: `/opt/data/profiles/<p>/cron/jobs.json` (¡NO
  `/root/hermes-agent/data/profiles/<p>/cron/` — en este VPS /opt/data es el home
  real de perfiles; excepción: perfiles `--isolated` como roshi viven en
  /root/hermes-agent/data/profiles/).
- Datos del cron: `python3 -c "import json; d=json.load(open('<jobs.json>')); ..."`

## How to Run

Crear un job de memoria por perfil (patrón guardar-diario, validado):

```bash
HERMES_HOME=/opt/data/profiles/<p> /usr/local/bin/hermes cron create \
  --name guardar-diario-memoria \
  --deliver local \
  --repeat 9999 \
  --skill engram-memory-system \
  --skill guardado-doble-memoria \
  --script daily_session_report.py \
  --model <modelo> --provider <provider> \
  "<min> <hora> * * *" "<prompt completo>"
```

## Quick Reference

- **PIN obligatorio**: `--provider` + `--model` en el job. Sin pin → drift_skip.
- **Expresión cron**: `<minuto> <hora> * * *`. `6 0 * * *` = 00:06.
- **Verificación real**: leer jobs.json (`next_run_at`, `last_status`,
  `failure_streak`), NO fiarse del warning del CLI.
- **Fallback de ejecución**: watchdog que re-ejecuta jobs fallidos vía
  proveedor alternativo (ver references/fallback-watchdog.md y
  scripts/fallback_watchdog.py).

## Procedure

### 1. Crear con pin (evita drift_skip)
Siempre declarar provider/model del job. Un job SIN pin usa la config global de
inferencia; si esa config cambia (p.ej. se renombra un provider), Hermes lo
SALTA sin llamar al modelo: `last_status=error`, `failure_streak` sube, sin
traceback útil en logs. El pin queda en jobs.json (`provider`, `model`);
`provider_snapshot`/`model_snapshot` pueden ser None y es normal.

### 2. Sintaxis de expresión
Formato de 5 campos: `minuto hora día-mes mes día-semana`. El primer campo es
MINUTO. Trampa frecuente: `0 6 * * *` = 06:00, no 00:06. `0 24 * * *` falla
"out of range". Para escalonar a medianoche: `6 0 * * *`, `12 0 * * *`, ...

### 3. Aviso falso "Gateway is not running"
`hermes cron create` lo imprime aunque el gateway multiplexado vaya a disparar
los crons de todos los perfiles. Confirmar con next_run_at futuro en jobs.json.

### 4. Skills de los jobs (cargables top-level)
El loader de skills del cron NO resuelve skills anidadas (p.ej.
`guardado-doble-memoria` dentro de `engram-memory-system/`) ni perfiles con
`skills/` vacío ("Skill(s) not found and skipped"). Provisionar symlink
top-level por perfil (ver skill `hermes-skills-provisioning`).

### 5. Escalonar para no disparar rate-limit
Un solo bucket de API (NaN-Builders: "max 5 simultaneous requests") se cae con
ráfagas. Escalonar jobs de todos los perfiles (cada 6 min en el ejemplo) y
repartir modelo primario por bot + `fallback_providers` en cascada.

## Pitfalls

- **drift_skip**: es la causa #1 de "cron muerto sin error claro". Ver pin §1.
- **HERMES_HOME**: crearse en el perfil equivocado crea el job en default.
- **`--no-agent` entrega el stdout del script como mensaje**; para watchdog
  silencioso, diseñar el script para que stdout vacío = nada que reportar.
- **Fallback API ≠ agente con tools**: una llamada a LLM vía HTTP solo produce
  texto; NO ejecuta herramientas Hermes (mem_save/engram, publicación). Para
  jobs de memoria la protección real es pin + cascada de providers + retry.

## Verification

- `hermes cron list` desde el HERMES_HOME del perfil → job con next_run_at futuro.
- jobs.json: `enabled: true`, `provider`/`model` explícitos.
- Tras un run: `last_status: ok`, `failure_streak: 0`.
- Smoke del script del job en el perfil con `HERMES_DB_PATH`/env apropiado.

## References

- `references/fallback-watchdog.md` — patrón de 3 capas (NaN → B.AI →
  OpenCode-Go), wrapper API, limitación honesta.
- `references/opencode-go-api.md` — endpoint, modelo IDs sin prefijo, escaneo
  de modelos gratuitos (cost=0).
- `scripts/fallback_watchdog.py` — watchdog idempotente que escanea jobs.json
  de todos los perfiles y re-ejecuta jobs fallidos vía proveedor fallback.