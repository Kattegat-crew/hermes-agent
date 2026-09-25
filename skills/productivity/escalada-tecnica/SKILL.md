---
name: escalada-tecnica
description: "Use when a task cannot be completed and must be escalated."
tags: [escalada, tickets, buzon, evidencia, protocolo, handoff]
---

# Protocolo de Escalada Tecnica (Regla Bob)

Cuando un agente NO puede completar una tarea (falta de herramientas, 2 intentos fallidos del mismo enfoque, o duda sobre el resultado), la ESCALA al agente tecnico del perfil default via buzon compartido.

## Regla dura anti-falso-exito

PROHIBIDO reportar exito sin evidencia observable (archivo en disco con tamano > 0, respuesta de API, entrada en log). Si no hay evidencia, el estado real es NO LOGRADO y se escala. Nunca digas 'listo' basandote en intencion.

## Cuando escalar (cualquiera de estos)

- La tarea requiere herramientas que no tienes (terminal, ffmpeg, codigo).
- Fallaste 2 intentos del mismo enfoque. PROHIBIDO insistir con variaciones del mismo metodo.
- No puedes verificar el resultado con evidencia.

## Como escalar (agente cliente)

Escribe un ticket JSON en `/opt/data/inbox/<tu-perfil>/pending/ticket-<fecha>-<perfil>-<num>.json`:

```json
{
  "id": "ticket-20260909-nancy-001",
  "tarea": "Descripcion clara y autocontenida de lo que se necesita",
  "archivos": ["/opt/data/ruta/al/archivo"],
  "intentos_fallidos": ["que intentaste y por que fallo"],
  "canal_entrega": "/opt/data/profiles/<perfil>/documentos/ o whatsapp:<numero> o bot-chat:<perfil>",
  "estado": "pending"
}
```

Reglas del ticket:
- La tarea debe ser AUTOCONTENIDA: el agente tecnico no ve tu conversacion.
- Los archivos deben estar bajo /opt/data/ y existir.
- Si el usuario espera respuesta por WhatsApp, indica el numero en canal_entrega.
- Despues de escribirlo, informe al usuario: 'He escalado tu solicitud al equipo tecnico'.

## Como ejecutar (agente tecnico / default)

El cron `escalation-watcher` corre cada 5 min con el script `scripts/escalation_watcher.py`. Cuando hay tickets, el script los reclama (pending -> processing) e inyecta instrucciones en el prompt. El agente debe:

1. Ejecutar la tarea con las skills del catalogo.
2. Verificar con evidencia real (ls -la, tamano > 0).
3. Mover el ticket a done/ (con campo evidencia) o failed/ (con campo error). Nunca borrar tickets.
4. NO entregar por WhatsApp directamente salvo que canal_entrega lo pida explicitamente.

## Estados del ticket

pending (en pending/) -> processing (reclamado) -> done (con evidencia) | failed (con error)

## Ubicaciones en PROD

- Buzon: /opt/data/inbox/<perfil>/{pending,processing,done,failed}/
- Script watcher (canonico para cron): /opt/data/home/.hermes/scripts/escalation_watcher.py (copia espejo en /opt/data/scripts/)
- Log del watcher: /opt/data/inbox/watcher.log
- Cron: job 'escalation-watcher' en el perfil default (cada 5 min, deliver local)
- Skill de transcripcion asociada: audio-video-transcription

## Gotchas verificados (2026-09-09)

- El cron exige script RELATIVO a ~/.hermes/scripts/ (no rutas absolutas).
- `hermes cron runs` solo registra ejecuciones con stdout (tickets); runs silenciosos no aparecen.
- API whisper NaN: WAV >~2MB da 413 del proxy nginx -> convertir a MP3 antes. Audio sin voz (-91dB) retorna texto vacio (no es bug); diagnosticar con ffmpeg volumedetect.
- Segmentos <2 min retornan texto vacio; >52 min retornan 503. Chunk recomendado: 50 min.
- Claim atomico: shutil.move pending->processing + flock exclusivo evitan doble procesamiento.