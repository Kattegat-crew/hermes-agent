# PLAN — Radar Regulatorio DIAN/Coljuegos (F1) por perfil
**Fecha:** 2026-09-22 · **Autor:** Ragnar · **Estado:** aprobado en diseño, pendiente despliegue

## Objetivo
Notificar automáticamente a Helmer y Yulieth los correos críticos de DIAN y Coljuegos
(en el futuro: CCB, alcaldías, bancos) que llegan a las bandejas oficiales de
Lucky Brothers (luckybrothers.sas@gmail.com) y Golden Game (goldengameltda@gmail.com).

## Infra verificada en vivo (2026-09-22, PROD)
- Conexiones ActivePieces activas: `lucky-gmail` (owners: comms, default, helmer, lucky, yulieth),
  `golden-gmail` (owners: comms, default, helmer) — /opt/data/connections-map.json
- Perfiles Hermes en PROD con MCP ncl_google ya montado: helmer, yulieth
  (NCL_MAP=/opt/data/connections-map.json, NCL_SECRETS=/opt/data/secrets)
- Cron de cada perfil con entregas WhatsApp probadas:
  helmer → `whatsapp:109165234127014@lid` · yulieth → `whatsapp:194373190996209@lid`
- Buckets de IA disponibles vía smart_model_routing (deepseek-v4-flash / qwen3.6)

## Diseño F1 por perfil
1. **Cron en perfil helmer** (cada 1h): usa su MCP ncl_google con `--profile helmer`
   → revisa `lucky-gmail` y `golden-gmail` (queries `from:dian.gov.co`, `from:coljuegos.gov.co`
   y variantes `notificaciones@dian.gov.co`, `alertas@coljuegos.gov.co`)
   → clasifica 🔴 CRÍTICO / 🟡 PLAZO / ⚪ informativo con el modelo barato
   → entregará resumen a `whatsapp:109165234127014@lid`
2. **Cron en perfil yulieth** (cada 1h): misma lógica pero SOLO `lucky-gmail`
   (owners de lucky incluyen a yulieth; golden NO)
   → entrega a `whatsapp:194373190996209@lid`
3. Cada alerta incluye: remitente, asunto, fecha, resumen de 3 líneas (IA), link Gmail.
4. Anti-duplicado: registrar IDs de correo ya notificados en un JSON local del perfil.

## Pasos de implementación
- [ ] Crear job cron en /opt/data/profiles/helmer/cron/jobs.json (prompt con queries+clasificación)
- [ ] Crear job cron en /opt/data/profiles/yulieth/cron/jobs.json (solo lucky)
- [ ] Ejecutar corrida de prueba manual del prompt (sin entregar) y validar clasificación
- [ ] Verificar entrega WhatsApp real en ambos grupos
- [ ] Monitor 72h + ajuste de reglas de clasificación

## Otros módulos del plan maestro (ver informe del 22-sep)
- F2: Hub de facturas electrónicas (SIIGO/DIAN XML → Sheet + alerta contador)
- F3: Tablero de trámites Coljuegos/CCB/alcaldías con vencimientos

---
## REGISTRO DE DESPLIEGUE (2026-09-23)
- Jobs creados: helmer id b592f56fcb60 / yulieth id beefb856ecaa, cron "0 8-21 * * *"
- Deliver: helmer wa:109165234127014@lid · yulieth wa:194373190996209@lid
- Dry-run live OK, aislamiento owners verificado, backups jobs.json.bak-radar-20260922
- Hallazgo: boletines DIAN HTML puro -> clasificacion por remitente+asunto
