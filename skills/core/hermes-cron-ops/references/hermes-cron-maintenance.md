---
name: hermes-cron-maintenance
description: Use when editing Hermes cron jobs or auditing silent runs
version: 1.0.0
author: Ragnar
metadata:
  hermes:
    tags: [cron, edit, maintenance, silence-audit, jobs.json, evidence]
    category: devops
    related_skills: [hermes-scheduled-jobs, cron-fleet-audit, hermes-cron-delivery-routing]
---

# Hermes Cron Maintenance — editar jobs en vivo y auditar silencios

Complemento (skills hermanas user-owned, no editables sin adopt) para la
operación DIARIA sobre crons ya creados: cambiar prompts/schedules/deliver y
probar que un run silencioso fue silencio CORRECTO y no entrega perdida.
Validado 17/09/2026 en DEV (edición de prompts de informes matutino/vespertino
y auditoría de 5 silencios) y PROD (16 jobs del día).

## When to Use

- El Admin dicta una regla permanente sobre un informe de cron ("no vuelvas a
  incluir X") → hay que escribir la regla DENTRO del prompt del job.
- Cambiar schedule, deliver o script de un job existente.
- Un cron corrió `ok` pero no publicó nada y hay que demostrar que eso es
  correcto (o demostrar que NO lo es).

## Procedure

### 1. Editar un job (vía CLI, nunca a mano en jobs.json)
```bash
hermes cron edit <id> --prompt "<texto completo nuevo>"
# también: --schedule --deliver --failure-deliver --script --no-agent/--agent
#          --model/--provider --add-skill/--remove-skill
```
- El CLI responde "Updated job: <id>" SIEMPRE; la verificación real es releer
  jobs.json y confirmar el campo editado (grep del sentinela o len del prompt).
- Backup antes de editar en lote: `cp jobs.json jobs.json.bak-<motivo>-<fecha>`.
- Localizar el job leyendo jobs.json con python (default DEV contenedor:
  /opt/data/cron/jobs.json; PROD default: /opt/hermes/data/cron/jobs.json;
  perfiles: profiles/<p>/cron/jobs.json) filtrando por id o name.

### 2. Inyectar reglas permanentes del Admin en un prompt de informe
- Añadir la regla como línea dura al FINAL del prompt existente (no reescribir
  el resto). Ej: "- NUNCA incluyas en este informe pendientes sobre X: motivo."
- Dejar un SENTINELA único dentro del texto nuevo (p.ej. la frase misma) para
  comprobar idempotencia antes de re-aplicar y para verificar después.
- Patrón programático seguro: python lee jobs.json, selecciona ids, y ejecuta
  `subprocess.run(["docker","exec","-u","hermes","hermes-agent",
  "/opt/hermes/bin/hermes","cron","edit",id,"--prompt",np])` — un solo
  ssh para todo el lote, con backup previo.

### 3. Auditar un run silencioso (evidencia POSITIVA)
"corrió ok y no dijo nada" solo prueba que el script decidió callar. Probar el
silencio correcto:
1. Leer el criterio de silencio EN el script del job (stdout vacío = nada que
   reportar es un diseño válido; p.ej. "no hay piezas debidas").
2. Si la entrega es webhook propio del perfil, consultar la API de Discord
   (mensajes de hoy en el canal destino) — evidencia directa de publicación.
3. NO aceptar como prueba la ausencia del log de errores si el script se traga
   excepciones (patrón vigia_post_discord.py: escribe log SOLO cuando falla y
   siempre sale 0) — ausencia de log es señal débil; preferir scripts con
   SUMMARY/estado consultable.
4. La entrega real por plataforma se prueba ÚNICAmente con la línea
   `delivered to <chat>` en el log del perfil (ver hermes-cron-delivery-routing).

## Pitfalls

- `--prompt` reemplaza el prompt COMPLETO: pasar siempre el texto íntegro
  (prompt previo + regla nueva), nunca solo la regla.
- Editar jobs.json a mano evita la validación del CLI y corrompe el store.
- Un cron puede correr desde dos árboles (gateway del contenedor + backend
  Desktop como root): tras editar, un turno viejo aún en cola puede ejecutar
  la versión anterior una vez.
- "Updated job" + "Ran now: succeeded" no prueban nada por sí solos (el run
  manual corre fuera del gateway).

## Verification

- jobs.json re-leído: sentinela presente, schedule/deliver correctos.
- Próximo tick: `last_status: ok` y (si aplicaba) mensaje publicado o línea
  `delivered to` en el log.

## References

- Creación y diagnóstico de crons nuevos → skill `hermes-scheduled-jobs`
  (user-owned; si se adopta, fusionar esta sección de edición allí).
- Auditoría de flota completa → skill `cron-fleet-audit` (user-owned).
