# Auditoría de flota de crons — 10/09/2026 (dev + prod, read-only)

Pedido del Admin: "escanea todos los crons, mira que sean pertinentes, que funcionen y no tengan errores. Diagnostica, no hagas nada."

## Inventario (71 jobs Hermes + cron del host)

- **DEV**: default 20 · roshi 1 · vigia 5.
- **PROD**: default 7 · nancy 23 · jacqueline 8 · helmer 2 · ivan 2 · yulieth 2 · alejandro 1.
- **Host**: dev `/etc/cron.d/hermes-gateway-fleet` (`*/5`, corre `gateway-fleet-health.sh`) y `hermes-sync` (02:00). Prod: **ningún** cron de flota Hermes (solo backups: outline, paperless, vaultwarden, sysstat, e2scrub, staticroute). Dev: timers `vault-sync` y `cleanup-previews`.

## Fallos reales encontrados

1. **`content-intel-daily`** (dev, 06:00, no_agent) — `last_status=error`, `failure_streak=2`. Error: `python3: can't open file '/opt/data/content-intel-build/content_harvest.py'` **aunque el archivo existe**. Causa: la corrida venía del ticker root del host, donde `/opt/data` es otro árbol. Fix ya aplicado ese mismo día 08:00 (`[ -f /.dockerenv ]` + rutas `/root/hermes-agent/data/...` + `docker exec -u 10000`), **sin verificar todavía** en una corrida real → se reporta como pendiente de confirmar en la próxima corrida.
2. **Perfil `vigia`** (dev) — 3 jobs en `blocked_config` con streak 3–4: `hermes-maintenance-night`, `vigia-informe-0800`, `vigia-auditoria-2100`, todos `deliver=discord`. Causa raíz: el gateway del perfil arranca con `No messaging platforms enabled` (`profiles/vigia/logs/gateway.log`; `gateway_state.json` con `"platforms": {}`) → el job se aborta antes de correr y nunca hay alerta. Su 4º job (`vigia-health-2h`, modo monitor) también apunta a discord: aunque detecte algo, se pierde. Resultado neto: ese bot lleva días sin poder alertar por ningún canal.
3. **PROD `profiles/yulieth` — `recordatorio-cumpleanos`** (08:00, enabled) — `last_status=error`, streak 1: `Script not found: /opt/data/profiles/yulieth/scripts/birthday_reminder_yulieth.py` (el archivo existe desde ~13:24 y la corrida fue 13:25 → probablemente resuelto, a confirmar). Además `last_delivery_error: platform 'whatsapp' not configured/enabled` porque en `profiles/yulieth/config.yaml` está `platforms.whatsapp.enabled: false`, pese a que el gateway multiplexado sí tiene sus 3 rutas (`573107864877@s.whatsapp.net`, `'573107864877'`, `194373190996209@lid`).
4. **`inspect-drive-xlsx`** (prod jacqueline) — error por script faltante, pero el job ya está `completed/disabled`: residuo, no incidencia.

## Pertinencia (candidatos a limpiar, no a reparar)

- `resumen-diario-wa` (dev, pausado desde 04-sep): su script imprime `[HOLD] envío deshabilitado — falta confirmación del grupo destino`. No-op; lo cubre el matutino de Telegram.
- `informe-diario-exacto` (dev, 07:00): corre y publica a Discord, pero el informe sale **vacío** porque su ventana es 00:00→07:03 (falta `--yesterday`) → falso verde diario; ya había propuesta pendiente de OK.
- `gateway-restart-ncl-google` (dev): one-shot `completed` del 06-sep.
- Prod: ~19 jobs `completed/disabled` (one-shots de recordatorios y los de cursos/webinars/guías de jacqueline).
- Duplicidad de vigilancia: `default` tiene `vigia-reprobe-puertos-bd` (07:00) y `vigia-fleet-gateways` (10 min), ambos SÍ entregan, mientras el perfil `vigia` tiene su propia vigilancia que no entrega.

## Latentes

- `competitor-news-digest` y `hermes-setup-autoaudit` corrieron el 07-sep **sin sus skills** ("skill no encontrada y omitida": `competitor-news-monitor`, `grounded-citations`, `hermes-agent`), aunque las tres existen en disco; degradaron bien pero hay que ver por qué no resolvieron.
- Prod sin watchdog de flota en el host (dev sí): allá la red de seguridad es solo s6.

## Sano (resumen)

- Dev: matutino/vespertino Telegram, pico y placa, `guardar-diario-memoria` (default/roshi/vigia), probe de puertos, davibank, `sync-connections-map`, flota de gateways, brain graph y los 5 del calendario — `ok`, sin atrasos, scripts existentes y sintaxis válida.
- Prod: guardianes de memoria de los 6 perfiles, saludos 7AM de los 4 clientes, TRM diaria, `escalation-watcher` (5 min) y los 13 recordatorios médicos de nancy — `ok` y al día.
- Ningún job con `next_run_at` vencido ⇒ sin corridas perdidas. Los watchdogs silenciosos entregaban `silent (empty output)`, como deben.
