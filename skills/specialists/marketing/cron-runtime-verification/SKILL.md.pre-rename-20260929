---
name: cron-runtime-verification
description: "Use when verifying Hermes cron jobs inside the gateway ns."
tags: [hermes, cron, nsenter, gateway, verificacion, devops]
version: 1.0.0
author: Ragnar
---

# Cron Runtime Verification (host ↔ gateway container)

Los crons de Hermes ejecuta el scheduler DENTRO del contenedor del gateway: namespace de montaje propio, PATH propio, python 3.13 propio. El host (donde trabaja Ragnar vía terminal) es otro mundo. Un "verificado" hecho desde el host puede ser falso.

## Regla de oro

Antes de declarar un cron operativo, TODO check crítico corre en el namespace real del gateway:

```bash
G=$(pgrep -f 'hermes gateway run' | head -1)
nsenter -t $G -m -S 10000 -u -- env HOME=/opt/data \
  PATH=/opt/data/.local/bin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin <cmd>
```

`setpriv --reuid=10000` solo cambia uid — NO cambia mount namespace → falsos verdes. (Caso real 2026-09-08: cron "100% verificado" con setpriv fue declarado RECHAZADO por auditor con nsenter; el repo que ejecutaba no existía en el contenedor.)

Checklist reproducible con `scripts/audit_cron.sh` (esta skill).

## Mapa del entorno dual (verificado por inodo)

| Path en gateway (cron) | Equivalente host |
|---|---|
| `/opt/data` | `/root/hermes-agent/data` (volumen compartido — MISMO inodo) |
| `/opt/data/repos`, `scripts`, `secrets`, `.ssh`, `cron/output` | `data/repos`, `data/scripts`, ... |
| `/root` del contenedor | 700 root-only, NO es /root del host — nada del host es visible ahí |
| host alcanzable | `ssh root@10.0.2.1` (clave del gateway en `data/.ssh`) |

Implicaciones:
- Repos independientes pueden vivir en el host `/root/<repo>` (accesible desde el contenedor vía `/host/root/<repo>` gracias al montaje `/host:rw,rslave`), o en `data/repos/<repo>` si son exclusivos de Hermes. Mover = `mv` del original + permisos adecuados (`chown -R hermes:10000`) + `git config --global --add safe.directory` en ambas vistas + actualizar rutas. NUNCA clonar segunda copia (causa histórica de "editas una copia vieja").
- Scripts Python usan ruta auto-detectada relativa a `Path(__file__)` o resolución multi-entorno: `/host/root/x`, `/root/x`, `/opt/data/repos/x`.
- **Los wrappers `.sh` en `data/scripts/` DEBEN auto-detectar el repo igual que el .py** (NO hardcodear una sola ruta). Resuelven con `for c in /host/root/x /root/x /opt/data/repos/x /root/hermes-agent/data/repos/x; do [ -r "$c/<target>" ] && REPO=$c && break; done`.
- Credenciales/secrets bajo `data/` son legibles por uid 10000; si el repo vive en `/root` del host, debe tener permisos de grupo para uid 10000 o sus credenciales inyectadas en `data/.env`.

## Checks mínimos antes del "operativo" (todos bajo nsenter)

1. `python3 -c 'import <deps>'` — el python del gateway es 3.13 con deps propias, las del host (3.12) no cuentan
2. `git pull --ff-only` desde el repo → credenciales + ownership del cron-user
3. El wrapper completo del cron → exit 0, stdout solo para eventos accionables
4. Escritura real: `touch /opt/data/cron/output/<job_id>/.wt` (si el dir existe pero es root:root 700 → chown 10000)

## Instalar deps python para el gateway (contenedor SIN red)

```bash
# 1) host: descargar wheels cp313 (multi-platform opportunist)
mkdir -p /root/hermes-agent/data/repos/wheels && cd $_
pip download -q --python-version 313 --only-binary :all: \
  --platform manylinux_2_34_x86_64 --platform manylinux_2_17_x86_64 <paquetes>
# 2) gateway, como uid del cron — HOME=/opt/data OBLIGATORIO (sin él escribe en /root → Errno 13):
nsenter -t $G -m -S 10000 -u -- env HOME=/opt/data python3 -m pip install -q --user \
  --break-system-packages --no-index --find-links /opt/data/repos/wheels <paquetes>
```

`uv pip install --python /proc/$G/root/...` falla (symlinks fuera del ns). El venv del gateway `/opt/hermes/.venv` (py3.13) no tiene pip — NO lo uses para scripts de cron; usa `/usr/bin/python3` del contenedor, cuyo user-site es `data/.local/lib/python3.13/site-packages`.

## Binarios del host fuera del contenedor (composio, etc.)

El binario Bun de composio hace core dump dentro del contenedor; el CLI real vive en `/usr/local/bin/composio` del HOST. Puente: `ssh -o BatchMode=yes root@10.0.2.1 composio execute ...` (la clave del gateway autoriza). Antes de inventar un puente, comprueba qué hay en cada vista: `ls /proc/$G/root/usr/local/bin/<bin>` vs `command -v <bin>`.

## GitHub deploy keys (multi-repo)

Una deploy key atada a un repo da "Repository not found" en los demás (404, no auth-error). Por repo nuevo que toque un cron: `ssh-keygen` dedicado → `gh api repos/<org>/<repo>/keys -f title=... -f key=... -f read_only=false` y ponerla primero en `IdentityFile` de `data/.ssh/config`.

## Auditor independiente anti-autoengaño

Para sistemas importantes, lanzar sesión fresca que no crea en las afirmaciones del constructor:

```bash
hermes -z "$(cat /tmp/reviewer_prompt.txt)" --yolo > /tmp/reviewer_report.md 2>&1
```

Prompt del reviewer: solo-lectura explícito (prohibido publicar/commitear/escribir), checklist numerado con PASS/FAIL + evidencia exacta, instrucción de verificar con nsenter, veredicto final. Verificar después los hallazgos del reviewer contra `/proc/$G/root` — los tuyos propios también. Un check sin evidencia en el entorno real es FAIL.

## Otros detalles del scheduler

- Scripts de cron deben vivir bajo `~/.hermes/scripts/` (o aquí `data/scripts/`) — el scheduler lo exige; el wrapper puede exec a cualquier ruta.
- `notify` en terminal background: solo bool o lista — nunca string "True".
- Perfiles aislados: vigia/roshi tienen sus propios `/proc/<pid>` — verificar contra el pid del gateway del perfil dueño del cron.
- Estado 4 (guardrails) puede interceptar patches en turnos tardíos pese a un "dale" previo al plan: aplicar todas las ediciones del plan en el mismo turno en que se autoriza.