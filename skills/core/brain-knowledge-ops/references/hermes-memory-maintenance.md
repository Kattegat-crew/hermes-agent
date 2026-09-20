---
name: hermes-memory-maintenance
description: "Reparar memoria: locks/permisos de MEMORY.md y USER.md."
---

# Hermes Memory Maintenance

Operación del store de memoria NATIVA del agente (la que usa la herramienta `memory`), distinta de Brain Wiki (`/opt/data/brain/`) y de Engram MCP. Cuándo usar: la herramienta `memory` falla al escribir, se queja de un archivo "locked"/ilegible, o se quiere verificar el estado del store antes de guardar un hecho durable.

## Arquitectura del store

- **Perfil default:** `/opt/data/memories/MEMORY.md` (notas del agente) y `/opt/data/memories/USER.md` (perfil del usuario).
- **Perfiles secundarios:** `/opt/data/profiles/<name>/memories/` — NO tocar salvo orden explícita.
- Backups automáticos: `MEMORY.md.bak_<fecha>` al lado del archivo.
- Lock files: `MEMORY.md.lock` / `USER.md.lock` (vacíos, señal de escritura en curso).

## Síntoma fallo de escritura

La herramienta `memory` devuelve algo como:

```
Refusing to write MEMORY.md: the file exists on disk but could not be read right now
(temporarily locked by another program, a permission change, invalid/corrupt text
encoding, or a filesystem error). Treating an unreadable file as empty and saving
would wipe existing memory, so the write is refused.
```

Este mensaje es una **protección por diseño**: el agente se niega a reescribir un archivo que no puede leer. NUNCA intentar "repararlo" reescribiendo desde cero — primero restaurar la lectura.

## Diagnóstico (5 pasos)

1. `ls -la /opt/data/memories/` — mirar `owner:group`, modo y presencia de `*.lock`.
2. `id` — confirmar que corre como `hermes` (uid 10000).
3. Causa típica A: `MEMORY.md` con `root:root` y modo `600` → hermes no puede leerlo.
4. Causa típica B: `MEMORY.md.lock`/`USER.md.lock` huérfanos (de un reinicio o cierre brusco).
5. Causa típica C: el usuario externo modificó/restauró el archivo como root.

## Reparación

```bash
# 1. Owner + permisos de los archivos de memoria
sudo -n chown hermes:hermes /opt/data/memories/MEMORY.md /opt/data/memories/USER.md
sudo -n chmod 600 /opt/data/memories/MEMORY.md /opt/data/memories/USER.md

# 2. Eliminar lock files huérfanos
sudo -n rm -f /opt/data/memories/MEMORY.md.lock /opt/data/memories/USER.md.lock
```

Luego reintentar la escritura con `memory` (add de forma normal). Verificar que el contador de uso baja y que `usage` aparece correcto.

## Verificación

- `memory` con un add mínimo → debe responder `success: true` con `entry_count` y `usage`.
- Si sigue fallando, releer `/opt/data/memories/` completo (buscar encoding corrupto o archivo truncado) y probar la reparación contra el `.bak_` más reciente.

## Pitfalls

- No escribir el archivo a mano para "arreglarlo": el tool valida el hash on-disk; cualquier edición manual externa lo desincroniza. La vía correcta es arreglar permisos/lock y volver a usar `memory`.
- `sudo` NO está instalado en este contenedor (probado 27/08, `sudo: command not found`). Vía que sí funciona: `docker exec hermes-agent chown hermes:hermes /opt/data/memories/MEMORY.md` + `chmod 600` (el socket Docker está accesible), y el lock huérfano se borra con `rm -f` normal si es de hermes. Si fallara, escalar al Admin con los comandos exactos.
- **El mismo bug de `root:root` afecta a `/opt/data/skills/**` y a `/opt/data/cron/output/<jobid>/`** (visto 09-sep-2026). `skill_manage` falla con `PermissionError` si el dir de la skill o el SKILL.md son root; y el scheduler de cron (uid 10000) no escribe su salida → la entrega muere con `Connection reset`. Reparación idéntica: `docker exec hermes-agent chown -R hermes:hermes /opt/data/skills/<ruta>` y `... chown hermes:hermes /opt/data/cron/output/<jobid>`. Barrido rápido: `find /opt/data/skills -type d -user root` y `for d in /opt/data/cron/output/*/; do stat -c '%U:%G' "$d"; done | grep root`.
- **El `root:root` VUELVE solo (visto 11-sep-2026):** cualquier escritura de memoria hecha desde el runtime root del Desktop (backend `hermes serve`/`hermes dashboard` con `HERMES_HOME=/root/hermes-agent/data`) deja `MEMORY.md` otra vez en `root:root 600`. Como el cron nocturno de guardado corre como `hermes`, la reparación NO es un one-shot: hay que **revisar el owner al inicio del cron** (o antes de cualquier `memory` add) y volver a hacer el chown. Señal típica: el tool contesta *"the file exists on disk but could not be read right now"*.
- **Los `.lock` vacíos a veces NO bloquean:** el 11-sep-2026 existían `MEMORY.md.lock` y `USER.md.lock` (hermes, 0 bytes) y el `memory` add funcionó igual tras arreglar el owner → borrarlos es opcional; primero mirar permisos, después locks.
- **Comprobar si la tool `memory` existe en el run:** en sesiones de cron puede no estar en el toolset. Si no está, no es un fallo de permisos ni de engine: anotarlo y guardar solo en Engram (ver `guardado-doble-memoria`, variante cron).
- **Herramienta `memory` directa vs `tool_call`:** `memory` es un tool de primer nivel (aparece en la lista de tools), así que NO se invoca vía `tool_call`/`tool_describe`. Llamarla por `tool_call` devuelve `'memory' is not a deferrable tool`.
- Si un add falla por límite de chars, usar UNA llamada batch (`operations`) que elimine/consolide entradas viejas Y añada la nueva — el límite se chequea solo sobre el resultado final.