---
name: hermes-admin-operations
description: Operate/config/audit Hermes Agent (provider/gateway).
version: 1.0.0
author: Ragnar
triggers:
  - configurar hermes / cambia el modelo / cambia el proveedor / añade skill o MCP / audita la config / mantenimiento de hermes
  - provider: proveedor / provider / NaN-Builders / OpenRouter / base_url
  - gateway: gateway caído / reinicia el gateway / puerto serve / desktop no conecta
  - plan de rol administrador: agente administrador de Hermes / bot de operaciones
metadata:
  hermes:
    tags: [hermes, ops, config, provider, gateway, cron, administrator]
---

# Hermes Admin Operations — operar la plataforma Hermes como operador principal

Patrón del "agente administrador de Hermes" (inspirado en el rol Havoc / Bot Mode de Hermes Desktop, 08/2026): en lugar de memorizar cada comando, recibir la **intención** ("quiero X resultado"), inspeccionar la config real, hacer el cambio, verificar que quedó y **escalar solo lo humano**. Ragnar es el agente administrador sobre el perfil propio; este skill formaliza el ciclo en maquinaria reutilizable.

## Disparadores

- «configurar hermes», «cambia el modelo/proveedor», «añade skill/MCP», «audita/revisa config», «haz mantenimiento de hermes», «el gateway cayó», «el desktop no conecta».
- Cualquier petición que toque `config.yaml`, `.env`, `cron/jobs.json`, `mcp_servers`, perfiles o el gateway.

## Ciclo operativo D-I-V-E (núcleo)

1. **D = Diagnosticar / INSPECT** — leer el estado real ANTES de tocar nada:
   - `hermes config list` / `hermes config get <ruta>` — config vigente.
   - `hermes model` · `hermes gateway status` · `ss -tlnp` (puertos reales escuchando, p. ej. 9112/8642/8645).
   - `cron/jobs.json` · configuración de MCP · perfiles en `profiles/<name>/config.yaml`.
   - Nunca adivinar: si no sabes el estado, léelo.

2. **I = Cambiar CHANGE** — con backup SIEMPRE:
   - Copiar `config.yaml` → `config.yaml.bak-<fecha>` antes de tocar (o usar `hermes config set KEY VAL` cuando aplica, que valida sintaxis).
   - Secrets NUNCA en `config.yaml` — van en `.env` (tokens, API keys).

3. **V = Verificar VERIFY** — comprobar que el cambio quedó efectivo:
   - Releer la config/key tocada.
   - Health check real: puerto escuchando, `gateway status`, respuesta HTTP.
   - Test de humo del flujo que se tocó (p. ej. desktop conectando, bot respondiendo).
   - "Está hecho" solo tras verificar.

4. **E = Escalar solo lo humano ESCALATE** — qué NO puede hacer un agente:
   - API keys, OAuth, tokens @BotFather, crear bots/perfiles nuevos, credenciales.
   - Escribirlo en `brain/tasks/pending.md` y seguir; NO bloquear el proceso por ello.

## Pitfalls

- **Alias de provider obsoleto**: versiones nuevas de Hermes (p. ej. serve v0.20.4) dejan de reconocer alias heredados tipo `custom:nan-builders`. Síntoma: `Unknown provider 'custom:nan-builders'. Check 'hermes model'...`. Usar el **nombre canónico** del provider (`NaN-Builders` en el config principal del serve) — no el alias viejo. Fix: backup + reescribir esa línea en `config.yaml` (no en `.env`, que ya no lee `LLM_MODEL`), reiniciar `hermes-serve` y verificar.
- **Desktop cachea provider**: tras reiniciar el serve, el Desktop puede mantener el provider viejo en memoria. Si persiste, cerrar la app completa (bandeja del sistema → Salir) y relanzar.
- **Gateway y serve son procesos separados**: `hermes gateway status` "running" NO implica que la API HTTP escuche. Verificar con `ss -tlnp` sobre el puerto real.
- **Reinicio bajo systemd**: `systemctl restart hermes-serve` tarda ~20s y desconecta el Desktop — anunciarlo antes al operador.
- **`hermes gateway status --verbose` NO existe** — no inventar flags; usar `hermes gateway status`.

## Vigilancia automatizada (cron de mantenimiento)

- Job `hermes-maintenance-night` (03:30) con `monitor_script=/opt/data/scripts/hermes-ops-monitor.py`: verifica gateway UP y puertos clave, **monitorea updates del repo de Hermes** (GitHub API vs `hermes --version`), escanea errores del día en logs, revisa **logs de bots y comportamiento** (restarts, timeouts, bucles), comprueba disco/RAM, y como agente asigna **puntuación del output** (score 0-100 por bot) cuando se detecta cambio.
- Salida byte-estable del script = scheduler suprime el run; reporta **solo lo que cambió/se rompió** (silencioso si todo ok).
- Criterios y rutas de scoring: `references/monitoring.md`.
- Los jobs se registran en `cron/jobs.json`; auditar su vigencia en cada mantenimiento.

## Soporte

- Este skill materializa la Fase 1 del plan documentado en `/opt/data/brain/concepts/hermes-admin-operations.md` (ciclo DIVE, fases 1–5, track en `brain/tasks/pending.md`).
- Todo lo que requiere humano (tokens, OAuth, bots nuevos, perfiles) vive en `brain/tasks/pending.md`.