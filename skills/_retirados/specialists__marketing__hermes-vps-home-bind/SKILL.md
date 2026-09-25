---
name: hermes-vps-home-bind
description: >-
  Use when Hermes Desktop (or any SSH session) connects to a VPS but the
  backend uses the wrong data home (e.g. ~/.hermes instead of
  /root/hermes-agent/data), so sessions/bots/profiles don't show. Binds
  HERMES_HOME for all SSH sessions via PermitUserEnvironment.
category: devops
tags: [hermes, ssh, hermes_home, vps, environment, sshd, permituserenvironment]
version: 1.0.0
author: Hermes
triggers:
  - no veo mis sesiones
  - hermes_home
  - data home
  - bind hermes home
  - permituserenvironment
---

# Hermes VPS — bindear `HERMES_HOME` a los datos reales

## Problema

Hermes Desktop en modo SSH lanza su backend con:
```bash
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
```
Si `HERMES_HOME` no se exporta en la sesión SSH, usa `~/.hermes`, que puede ser un
home **distinto y vacío** respecto a donde viven las sesiones, bots y perfiles reales
(p. ej. `/root/hermes-agent/data`). Resultado: Desktop conecta bien pero no muestra
nada.

Diagnóstico del home efectivo (comparar state.db/profiles):
```bash
ssh root@<host> 'echo "HERMES_HOME=${HERMES_HOME:-$HOME/.hermes}"'
ssh root@<host> 'ls -la ~/.hermes/state.db /root/hermes-agent/data/state.db 2>/dev/null'
ssh root@<host> 'ls ~/.hermes/profiles /root/hermes-agent/data/profiles 2>/dev/null'
```
El home que tenga el `state.db` grande y los perfiles (ragnarcho, shared) es el correcto.

## Fix — exportar HERMES_HOME para todas las sesiones SSH

```bash
# 1) Permitir variables de entorno del usuario en sshd
printf 'PermitUserEnvironment yes\n' > /etc/ssh/sshd_config.d/99-hermes-env.conf

# 2) Definir HERMES_HOME para el usuario
umask 077
printf 'HERMES_HOME=/root/hermes-agent/data\n' > /root/.ssh/environment
chmod 600 /root/.ssh/environment

# 3) Validar y recargar sshd
sshd -t && systemctl reload ssh   # o: service ssh reload
```

## Verificar

```bash
ssh root@<host> 'echo $HERMES_HOME'                      # → /root/hermes-agent/data
env HERMES_HOME=/root/hermes-agent/data hermes profile list   # perfiles correctos
```

Después: en Desktop, **Sign out → Sign in** (o cerrar y reabrir) para que el backend
SSH se lance con el home correcto.

## Notas

- `/root/.ssh/environment` requiere `PermitUserEnvironment yes` (default no).
- No requiere cambiar nada en `connection.json` del Desktop; el home lo resuelve el
  entorno SSH, no la app.
- Si hay varias homes (p. ej. `~/.hermes` vs `/root/hermes-agent/data`), decide cuál es
  el canónico (donde vive el gateway y los perfiles) antes de bindear.

## Referencia
- `references/caso-2026-08-20.md` (skill `hermes-desktop-ssh-backend`).