---
name: hermes-release-adoption
description: Use when updating Hermes or reporting version/novedades.
---

# Hermes Release Adoption — versión viva y migración de features nativas

Cuándo: después (o antes) de un update de Hermes, o cuando el Admin pregunta
versión/novedades. Objetivo doble: (1) decir la versión REAL que corre el
gateway con evidencia, (2) convertir release notes en decisiones de migración
concretas para la flota (dev + prod, 12+ perfiles).

## 1. Verificar la versión viva (evidencia, no memoria)

Tras un update vía docker el checkout del host puede no ser legible como repo
(`git log` vacío/exit 128). Fuentes fiables en orden:

```bash
# Versión viva del gateway (el dato que importa):
docker exec hermes-agent /opt/hermes/bin/hermes --version
# Metadata del paquete instalado:
docker exec hermes-agent sh -c 'head -5 /opt/hermes/hermes_agent.egg-info/PKG-INFO'
# Release notes oficiales del tag:
# https://github.com/NousResearch/hermes-agent/releases/tag/<TAG>
```

Trampas verificadas (02/09/2026):
- El tag de GitHub usa FECHA (v2026.8.31) y el semver interno es OTRA cosa
  (v0.21.0) — mismo release, dos sistemas de numeración. No busques "v0.21.0"
  como tag: mapa semver→tag en la página /releases.
- `hermes --version` del host wrapper puede apuntar a otra instalación; usar
  `docker exec` para el dato del gateway.
- Si el release cubre varias versiones (v0.21.0 rolló v0.20.1–v0.20.6), leer el
  release completo, no el delta del último tag.

## 2. Mapear release notes → flota (checklist de adopción)

Por cada highlight, clasificar: NUEVO (capacidad disponible), OBSOLETO (reemplaza
un parche propio), IRRELEVANTE. Preguntas fijas:
- ¿Qué crons/watchdogs propios ahora los cubre el scheduler nativo?
- ¿Qué scripts de orquestación (delegación, peer-comms) ahora son nativos?
- ¿Cambió el formato de config.yaml (providers, fallback_model, cron)? → revisar
  migración antes de reiniciar perfiles.
- ¿La feature aplica a prod (169.58.189.222) o solo a desktop?

Regla: NO migrar de inmediato lo que ya funciona — evaluar tras el update, con
campaña activa se pospone. Verificar disponibilidad real de flags con `--help`
en la versión instalada (el release anuncia, el binario manda).

## 3. Inventario v0.21.0 "Pantheon" (2026.8.31) — evaluado para nuestra flota

- **Crons con memoria** (`continuity=true`, notepad persistente, monitor-mode sin
  LLM si nada cambió): reemplaza dedupe manual en prompts de Vigía y watchdogs →
  migración pendiente en hermes-scheduled-jobs (user-owned).
- **`hermes peer`** (DM bot-a-bot durable): candidato para handoff Bragi→Sindri
  sin pasar por Ragnar; evaluar vs A2A/AP webhook actual.
- **Bot Mode en Desktop** (roster, avatares deterministas, group chats,
  @-menciones): los avatares de perfiles (skills devops/hermes-bot-avatars) siguen
  siendo la vía canónica server-side; Desktop añade la capa visual de roster.
- **delegate_task steerable** (list/steer/stop, JSON schema, costo): ya en uso;
  revisar defaults nuevos (250 iter, 10 hijos concurrentes) al dimensionar.
- **Seguridad**: AGENTS.md/skills/memoria exigen aprobación de escritura → los
  agentes no pueden reescribir sus propias órdenes; compatible con nuestro gate
  humano de aprobación creativa.
- **Multiplex selectivo + MCP lifecycle RPC por perfil**: útil para served_profiles
  grandes; revisar si reemplaza reinicios completos de gateway en operaciones.
- **Telegram inline picker / CLI power wave / 6 providers nuevos (GLM-5.3-Flash,
  qwen3.8-max/flash ya en catálogo)**: rotación de modelos vía skill
  provider-manager sigue siendo el mecanismo.

## Referencias

- Skills user-owned con el detalle operativo profundo (pendientes de
  `hermes curator adopt`, no editables por el curador autónomo):
  `devops/hermes-vps-update` (procedimiento de update completo),
  `devops/hermes-scheduled-jobs` (crons multi-perfil), `context-monitoring`
  (forense de sesiones vía state.db).
- Release notes: https://github.com/NousResearch/hermes-agent/releases
