---
name: cron-fleet-audit
description: Use when auditing every Hermes cron job across profiles.
version: "1.0"
author: Ragnar
created: 2026-09-10
category: devops
metadata:
  hermes:
    tags: [cron, auditoria, flota, perfiles, dev, prod, read-only, watchdog]
    related_skills: [scheduled-job-diagnosis, cron-runtime-verification, cron-delivery-routing, hermes-cron-runtime-verification]
---

# Auditoría de flota de crons (todos los perfiles, dev + prod)

Cuando el Admin pide "escanea / diagnostica **todos** los crons" ("he visto que algunos
están fallando, mira que sean pertinentes, funcionen y no tengan errores"), no un job
concreto. Complementa a `scheduled-job-diagnosis` (que diagnostica UN job); esto es el
barrido completo de la flota.

**Regla de oro:** si el pedido es "diagnostica, aún no hagas nada", la auditoría es
**read-only**. No dispares jobs (`run` ejecuta scripts con efectos externos), no
re-dispares, no cambies `deliver` "para probar", no repares en el mismo turno: entregas
el informe con veredicto por job y esperas OK.

## 1. Inventario (los jobs viven en `cron/jobs.json` de cada home)

- default: `/opt/data/cron/jobs.json` · perfiles: `/opt/data/profiles/*/cron/jobs.json`
- PROD: `/opt/hermes/data/cron/jobs.json` + `/opt/hermes/data/profiles/*/cron/jobs.json`
  (en prod `/opt/data` es symlink a `/opt/hermes/data`)
- Host (fuera de Hermes): `ls /host/etc/cron.d/` y `systemctl list-timers`.
  Dev tiene `hermes-gateway-fleet` (`*/5` → `gateway-fleet-health.sh`) y `hermes-sync`
  (02:00); prod **no** tiene cron de flota Hermes (solo backups) — eso es un hallazgo,
  no un supuesto.

## 2. Escáner

Corre `scripts/cron_fleet_audit.py` (read-only, stdlib) sobre todos los `jobs.json`:

```bash
python3 scripts/cron_fleet_audit.py /opt/data/cron/jobs.json /opt/data/profiles/*/cron/jobs.json
# prod: copia el archivo (no lo pipees por stdin) y ejecútalo con rutas explícitas
ssh prod 'cat > /tmp/cron_fleet_audit.py' < scripts/cron_fleet_audit.py
ssh prod "cd /opt/hermes/data && python3 /tmp/cron_fleet_audit.py cron/jobs.json profiles/*/cron/jobs.json"
```

Banderas: `STATUS=<x>` (error / blocked_config…), `streak=N`, `ATRASADO(Nm)`
(`next_run_at` vencido con el job enabled), `NUNCA-CORRIO`, `off:<state>`,
`SCRIPT-FALTA`, `SCRIPT-EN-OTRO-HOME`, `DELIVERY-ERR`.

## 3. Lee la evidencia, no el status

- `last_status: ok` **no** prueba que el job sirvió. Abre el último
  `cron/output/<jobid>/*.md` de cada job sospechoso.
- **Sano**: `0 bytes` o `**Status:** silent (empty output)` en un watchdog NO_AGENT;
  en modo `monitor`, `no_change (agent run suppressed)`.
- Los `.md` root-owned se leen con `docker exec hermes-agent cat <archivo>` (ese exec
  entra como root; en el contenedor NO hay `sudo`).
- Verifica además: existencia del script + `python3 -m py_compile <f>` / `bash -n <f>`,
  bit de ejecución, y dueño de `cron/output/<jobid>/` (dir `root:root` ⇒ el job muere
  en la entrega).

## 4. Clases de fallo que se repiten

- **`blocked_config`** → el job se **aborta antes de correr**: su `deliver` apunta a una
  plataforma que ese perfil no tiene configurada. Causa raíz típica: el gateway del perfil
  arrancó con `No messaging platforms enabled`
  (`grep -i 'No messaging' /opt/data/profiles/<p>/logs/gateway.log`) y su
  `gateway_state.json` muestra `"platforms": {}`. Un bot de alertas así lleva días mudo
  mientras `failure_streak` sube: repórtalo como "bot sin canal", no como job roto.
- **`Script not found: <ruta>`** → resolución **por perfil**: un `script` con nombre suelto
  resuelve en `<home>/scripts/`; una **ruta absoluta de otro home**
  (p.ej. `/opt/data/profiles/<otro>/scripts/x.py` declarada en el home default) se busca tal
  cual y falla. Comprueba con `ls <home>/scripts/<script>`.
- **`can't open file '/opt/data/...'` aunque el archivo exista** → la corrida la hizo el
  ticker root del HOST, donde `/opt/data` es OTRO árbol. El script debe detectar entorno
  (`[ -f /.dockerenv ]`) y usar `/root/hermes-agent/data/...` + `docker exec -u 10000`
  cuando corre desde el host.
- **"Skills no encontradas y omitidas"** en la cabecera del `.md` → el job corre degradado;
  las skills pueden existir en disco igual (revisar por qué no resolvieron).
- **Falso verde** → job `ok` cuyo contenido sale vacío TODOS los días (p.ej. ventana
  00:00→07:03 sin `--yesterday`): funciona pero no sirve. Va en *pertinencia*, no en errores.
- **`deliver: origin` con entrega fallida** → revisa la plataforma del `origin` en el config
  del perfil (`platforms.<x>.enabled`), no solo el `deliver` del job.

## 5. Pertinencia (lo que se borra, no se arregla)

- Jobs pausados cuyo script imprime `[HOLD]`/no-op desde hace semanas.
- One-shots `completed` acumulados (y los que tienen error viejo: residuo, no incidencia).
- **Duplicidad de rol**: la misma vigilancia en `default` y en un perfil dedicado (uno
  entrega y el otro no) → decidir dónde vive el rol.
- Fixes aplicados **sin corrida de verificación**: repórtalos como "pendiente de confirmar
  en la próxima corrida", nunca como cerrados.

## 6. Formato del informe

Por job: *sano* / *falla real* (causa raíz + evidencia + qué falta) / *pertinencia dudosa*.
Agrupa por severidad, da cifras primero (N jobs, N fallos reales, N candidatos de limpieza)
porque el Admin decide sobre eso, y cierra con "no he tocado nada" + próximos pasos propuestos.

## Pitfalls de la auditoría

- **Zona horaria**: comparar `next_run_at` contra `now` con `time.mktime`/`time.localtime`
  produce **falsos ATRASADO de horas** (el TZ del Python remoto ≠ el del contenedor). Usa
  `datetime.fromisoformat` (+ `tzinfo=utc` si es naive) y compara en UTC.
- **No pipees el escáner por stdin de ssh**: `ssh prod 'python3 - args'` mezclado con globs
  o `xargs` se come el stdin y devuelve vacío. Copia el archivo y ejecútalo.
- **Imprime el ARCHIVO en cada bloque** de resultados: el mismo UUID de job puede existir
  clonado en varios `jobs.json` → identifica por par (archivo, id) o atribuirás el fallo al
  perfil equivocado.
- Los accesos a `jobs.json` y a `cron/output/` son de solo lectura; no toques `deliver`,
  `enabled` ni `failure_streak` durante una auditoría.

## Referencias

- `scripts/cron_fleet_audit.py` — escáner read-only de todos los `jobs.json` (local y prod).
- `references/fleet-audit-2026-09.md` — auditoría real dev+prod del 10/09/2026: inventario,
  fallos con causa raíz, candidatos de limpieza y latentes.
- `scheduled-job-diagnosis` — diagnóstico de UN job que "no hizo su trabajo".
- `cron-delivery-routing` / `cron-runtime-verification` — dónde cae la salida y si el job
  puede correr en el namespace del gateway.
