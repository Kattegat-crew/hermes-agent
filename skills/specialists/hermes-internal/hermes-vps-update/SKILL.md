---
name: hermes-vps-update
description: "Actualizar Hermes Agent en el VPS a upstream/main preservando la config. Triggers: update hermes, hermes update on the remote host, actualizar hermes, update hermes vps, alinear hermes a upstream."
license: MIT
metadata:
  author: opencode
  version: "1.0"
---

# Actualizar Hermes Agent en VPS (a upstream/main) sin perder config

Patrón para el mantenimiento de instancias de Hermes en hosts remotos: lleva el
checkout a la última de NousResearch, rearma el gateway Docker y preserva TODA la
config real (`data/`, `.env`, NaN-Builders, allowlists, perfiles). El Desktop OS
pide este procedimiento cuando reporta "update hermes on the remote host".

## Disparadores

- «hermes update», «actualizar hermes en el VPS», «update hermes remote host»,
  «alinear hermes a upstream/main».

## Pre-vuelo: backups (obligatorio)

```bash
# 1. data/ completo (git-ignored, config real)
rsync -aHA /root/hermes-agent/data/ /root/hermes-agent-backups/data-$(date +%Y%m%d-%H%M%S)/
# 2. .env del root
cp /root/hermes-agent/.env /root/hermes-agent/.env.pre-update-$(date +%Y%m%d-%H%M%S)
git -C /root/hermes-agent hash-object .env   # anotar hash para verificar post
```

## Procedimiento

### 1. Alinear checkout a upstream/main

```bash
cd /root/hermes-agent
git fetch origin && git fetch upstream
git checkout -B main upstream/main
git reset --hard upstream/main
git hash-object .env     # DEBE ser idéntico al hash pre-vuelo
git check-ignore data    # → data/
```

Peligro: `git checkout` a `upstream/main` SOBRESCRIBE el `docker-compose.yml`
personalizado del VPS. Restaurarlo SIEMPRE desde la rama previa:

```bash
git show release-v0.20.4:docker-compose.yml > /root/hermes-agent/docker-compose.yml
```

Luego apuntar `image:` a la imagen construida de la rama main (`hermes-agent`).

### 2. Reinstalar venv host + migrar config

```bash
cd /root/hermes-agent
VIRTUAL_ENV=/opt/hermes-venv uv pip install -e ".[all,dev]"
/opt/hermes-venv/bin/hermes --version    # debe decir "Up to date"

# migrar la config REAL (HERMES_HOME explícito — sin él apunta a ~/.hermes)
VIRTUAL_ENV=/opt/hermes-venv HERMES_HOME=/root/hermes-agent/data \
  /opt/hermes-venv/bin/python3.11 -c "
import os; os.environ['HERMES_HOME']='/root/hermes-agent/data'
from hermes_cli.config import migrate_config; print(migrate_config(interactive=False))
"
```

### 3. Reconstruir el gateway Docker

```bash
cd /root/hermes-agent
docker compose build     # reintentar si falla con `denied` en ghcr (ver Pitfalls)
docker compose up -d
```

### 4. Post-verificación

```bash
/opt/hermes-venv/bin/hermes --version
VIRTUAL_ENV=/opt/hermes-venv HERMES_HOME=/root/hermes-agent/data \
  /opt/hermes-venv/bin/python3.11 -c "import os;os.environ['HERMES_HOME']='/root/hermes-agent/data';from hermes_cli.config import check_config_version;print('config_version:',check_config_version()[0])"
cat /root/hermes-agent/data/gateway_state.json | python3 -m json.tool | grep -A1 '"state"'
docker exec hermes-agent /opt/hermes/bin/hermes --version
```

## Pitfalls (anotadas: causa raíz de la operación real)

- **`git checkout upstream/main` sobrescribe `docker-compose.yml` del VPS**: el
  compose genérico de upstream monta `~/.hermes` y crea `hermes` +
  `hermes-dashboard`, NO tu `./data`, `.env`, vault, `mcp_tool.py` → contenedores
  accidentales apuntando a data vacía. **Fix**: restaurar el compose personalizado
  de la rama previa (mounts `./data`, `.env`, `./tools/mcp_tool.py`, vault,
  puertos `3000/9119`, `container_name: hermes-agent`, `image: hermes-agent`).
- **Token `ghcr.io` revocado (en `~/.docker/config.json`)**: rompe el build del
  `uv` público. **Fix**: backup del config docker, quitar la entrada `ghcr.io`
  (pull anónimo de imagen pública OK), reintentar el pull por reset de IPv6
  transitorio.
- **HERMES_HOME explícito**: sin él, `hermes` del host apunta a `~/.hermes`
  (default), NO a la data real del gateway (`/root/hermes-agent/data`).
- **Migración sin pérdida**: esperar `env_added: []` y `config_added: []`.
- **`shared:a2a fatal` (bind 9900)**: pre-existente, no es un retroceso del update.

## Salida

- Archivos tocados y estado post-verificación.
- Ruta de backups creados.
- Comandos reales ejecutados.
- `config_version` y plataformas en `gateway_state`.
- Cualquier incidente.

## Referencias

- `docs/actualizacion-hermes-vps-2026-08-20.md` — bitácora completa de la operación real.
- `hermes-desktop-remote-connection/SKILL.md` — diagnóstico de conexión remota Desktop.
