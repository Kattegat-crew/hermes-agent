---
name: hermes-team-ops
description: "Use when who-owns-what or cron handoff between profiles."
tags: [roster, equipo, crons, handoff, perfiles, profiles, ownership, hermes]
version: 1.0.0
author: Ragnar
metadata:
  hermes:
    tags: [roster, equipo, crons, handoff, perfiles, roshi, vigia, division-trabajo]
    category: communications
    related_skills: [hermes-multiprofile-cron-ops, admin-reporting, guardado-doble-memoria, hermes-production-deployment]
---

# Hermes Team Ops — Roster, propiedad de crons y handoffs entre agentes

Cómo operar el equipo de agentes de NeuralCrew Labs: quién es quién, quién es
dueño de qué (especialmente crons), y cómo traspasar trabajo/ownership entre
perfiles de forma verificable.

## When to Use

- Alguien pregunta "¿quién hace qué?" o "¿de quién es este cron?".
- Hay que migrar/traspasar crons de un perfil a otro (handoff de ownership).
- Se coordina trabajo en un grupo multi-agente (Ragnar/Roshi/Vigía/equipo marketing).
- Antes de reportar crons al Admin: verificar en qué perfil viven realmente.

## Roster del equipo (corregido por Jonathan 25/08/2026 — DIVISIÓN DE TRABAJO EXPLÍCITA)

- **Ragnar** = asistente personal de Jonathan. Orquestación, decisiones, alertas
  personales (pico y placa, informes 8am/8pm a Telegram). NO produce campañas.
- **Roshi** (slug interno: `roshi`, NO renombrar el slug) = asistente de Chucho. Operativo: documentos, reportes, automatizaciones,
  QA de integridad de campañas, plantillas (campaign.yaml → 5 docs).
- **Vigía** = operaciones del sistema. DUEÑO de todos los crons de sistema/servicios:
  health checks, mantenimiento nocturno, páginas y servicios arriba. NO produce campañas.
- **Equipo Marketing/Contenido** = bots SEPARADOS por perfil (Content/Social/Ads/Funnel,
  posiblemente por cliente: golden-marketing, lucky-marketing). Es UN EQUIPO APARTE,
  no Ragnar/Roshi/Vigía.

Regla derivada: nunca reportar crons de sistema como "míos" (Ragnar) — pertenecen
a Vigía. Verificar con `docker exec -e HERMES_HOME=/opt/data/profiles/vigia hermes-agent hermes cron list`.

## Propiedad de crons (estado verificado 25/08/2026)

| Cron | Perfil dueño | Delivery |
|------|-------------|----------|
| context-report-morning (8am) | Ragnar (default) | telegram:8709909260 |
| context-report-evening (8pm) | Ragnar (default) | telegram:8709909260 |
| alerta-pico-y-placa (6am) | Ragnar (default) | telegram:8709909260 |
| guardar-diario-memoria (23:00) | **UNO POR CADA AGENTE** (default, roshi, vigia, y prod: helmer, jacqueline, nancy, yulieth, neural-admin-test) | local |
| hermes-maintenance-night (3:30) | Vigía | discord |
| vigia-health-2h | Vigía | discord |
| vigia-informe-0800 | Vigía | discord |
| vigia-auditoria-2100 | Vigía | discord |

Regla de memoria: CADA agente tiene su PROPIO guardar-diario-memoria que guarda la
memoria de ESE agente — nunca un job central que guarde por todos.

## Handoff de crons entre perfiles (receta validada 25/08/2026)

Pasos para traspasar ownership de crons de un perfil origen (ej. default) a un
perfil destino (ej. vigia):

1. **Verificar scripts en el perfil destino**: los scripts (`--script`, `--monitor-script`)
   se resuelven contra `~/.hermes/scripts/` del perfil DESTINO. Copiar:
   ```bash
   docker exec hermes-agent sh -c 'mkdir -p /opt/data/profiles/<dest>/scripts && \
     cp /opt/data/scripts/<script>.py /opt/data/profiles/<dest>/scripts/'
   ```
2. **Crear los jobs en el destino** (con `HERMES_HOME` DENTRO del contenedor):
   ```bash
   docker exec -e HERMES_HOME=/opt/data/profiles/<dest> hermes-agent hermes cron create \
     --name <nombre> --deliver <discord|local|...> --skill <skill> \
     --monitor-script <script.py> --model <modelo> --provider <provider> \
     --repeat 9999 -- "<schedule>" "<prompt completo>"
   ```
   Notas: `--repeat 9999` para que sea indefinido; `--monitor-script` hace que el
   agente solo corra si cambia la salida (ahorro de tokens); el CLI NO soporta
   `--enabled-toolsets` (el job hereda todos los toolsets del perfil).
3. **Remover los duplicados del origen**:
   ```bash
   docker exec -e HERMES_HOME=/opt/data hermes-agent hermes cron remove <job_id>
   ```
4. **Verificar AMBOS lados**: `hermes cron list` en destino y origen. El aviso
   "Gateway is not running" al crear en un perfil NO es bloqueante si el gateway
   multiplexado del default dispara los crons de todos los perfiles servidos.

## Pitfalls

- **`hermes config set` sin `--profile` puede escribir en un perfil distinto del default.** El binario `/opt/hermes/bin/hermes` (dentro del contenedor) tiene su propio perfil activo por defecto — verificado 26/08/2026: `hermes config set display.show_reasoning false` sin flags escribió en `/opt/data/profiles/sindri/config.yaml`, NO en el default. Para tocar el default (Ragnar) usar `HERMES_HOME=/opt/data /opt/hermes/bin/hermes config set ...`, y SIEMPRE leer la salida "✓ Set ... in <ruta>" para confirmar el archivo tocado (fuente de verdad de dónde escribió).
- **Ocultar el razonamiento (thinking) de un perfil:** `display.show_reasoning: false` a nivel raíz (cubre CLI/TUI/Discord) + `display.interim_assistant_messages: false` + explícito por plataforma si se quiere. El default de Hermes es `show_reasoning: true` (config_defaults.py) — un perfil sin bloque `display` muestra TODO el pensamiento. Aplicado 26/08/2026 a roshi (bloque display nuevo) y default (raíz + platforms).
- **No editar skills user-owned** (created_by=None): el curator las rechaza. Si una
  skill de este territorio necesita cambios y es user-owned, recomendar
  `hermes curator adopt <skill>` — no intentar patch repetido.
- El CLI del host `hermes` es wrapper docker exec SIN `-e HERMES_HOME` → crea en
  default aunque hagas cd al perfil. Siempre pasar HERMES_HOME dentro del contenedor.
- No confundir "AP caído" con "AP movido": verificar en el VPS correcto (AP vive en
  prod junto a Twenty desde ~25/08; en dev :8088 no responde porque ya no corre ahí).
- Perfiles nuevos (o recién creados desde Desktop) pueden nacer sin bloque
  providers/ → 'Unknown provider' al correr crons. Copiar providers + chown 10000.

## Verificación

- Después de un handoff: `cron list` en ambos perfiles, y el job destino debe tener
  `state: scheduled` con `next_run_at` futuro.
- Para confirmar quién es dueño de qué cron: leer `cron/jobs.json` de cada perfil
  (`/opt/data/profiles/<p>/cron/jobs.json`, default usa `/opt/data/cron/jobs.json`).

## Referencias

- Skills relacionadas (user-owned, requieren adopt para editar): `hermes-multiprofile-cron-ops`
  (técnica por-perfil), `admin-reporting` (formato reportes), `guardado-doble-memoria`
  (patrón de memoria por agente).
