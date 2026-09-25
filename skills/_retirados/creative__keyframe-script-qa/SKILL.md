---
name: keyframe-script-qa
description: "Use when: analizar keyframes de escenas contra el guion."
version: 1.0.0
---

# QA guion × keyframes (pasada de Content sobre arte del producer)

Clase de tarea: cuando llegan renders escena-por-escena (caso: reel Lucky / Bingo Millonario, room Video-prod 29/08) y se pide analizarlos junto con el guion para fijar el estándar de futuras producciones. El rol de Bragi aquí NO es duplicar el QA técnico del producer: es la **verificación independiente con lens de historia y marca**, y el aderezo de voz al master prompt.

## Regla de oro: pasada propia, nunca eco
- Analizar **cada imagen con visión real** y cruzar contra el guion maestro. El valor para la sala es confirmar O corregir al teammate con evidencia. (Aquí se cazó que los dedos fusionados estaban en la mano del asa de Sc1, no en el saludo de Sc5 como reportó el producer; y signage extra no reportado: "EXPRESOS", "TERMINAL INTERMUNICIPAL".)
- Aprobar de memoria el informe ajeno = pasada perdida. Si el informe ajeno acierta, igual se declara "confirmado en mi pasada" por ítem.

## Qué mirar por imagen (checklist derivado del guion Seedance)
1. **Identidad del personaje vs hero**: nº/forma de hojas, ojos+catchlight, pajarita, **pies desnudos (NO shoes)** — las escenas tienden a poner botines (deriva leve-moderada). Hero + studio sheet (multi-pose) siempre como image_urls de identidad en cada run.
2. **Contacto físico de props**: todo objeto que menciona el guion debe estar agarrado con mano real o no entra al frame (maleta abandonada en Sc5 = error grave → regenerar o cubrir en motion).
3. **Continuidad del viaje**: vector de caminata y azimut del sol constantes entre planos consecutivos (Sc2C sesgada a la derecha vs frontal 2A/2B → fijar en prompt de movimiento). La hora dorada con suelo mojado refleja era "gratis" en todas → subirla a regla del STYLE-LOCK: *"unified by a single golden hour… every shot reads as one continuous journey"*.
4. **Textos ambientales**: legibles y bien escritos o inexistentes (cero garble). Los rótulos de un tríptico/tablero de intención NO deben imitarse dentro de las escenas — gráficos de venta van en edición (§13 del guion). Verificar citando textualmente qué dice cada letrero.
5. **Aptitud lip-sync** (para la escena del test): boca abierta con dientes definidos, contacto visual, aire de encuadre para el movimiento de cámara pedido; audio ÷ duración del clip debe dejar aire al final (3.34s en clip 5s ✅).
6. **Compliance Colombia**: máquinas tragamonedas/rótulos "JACKPOT" visibles → bokeh/DOF garantizado en motion + negativo *"no gambling UI, no jackpot machine as focal point, no winner celebrations"*. Cartones/fichas con números inventados rozan "no cartones inventados" → se señala como **decisión del Admin**, con voto de marca propio.
7. **Dictados de campaña** (mes del amor y la amistad, frases vetadas, una línea sutil por pieza): verificar que ninguna imagen los contradiga.

## Formato de entrega (lo que validó el Admin)
Archivo .md en workspace + resumen denso en sala, con:
- **Tabla de veredicto cruzado**: claim del teammate → qué vio mi pasada → estado (✅ confirmado / ⚠️ matiz / ✗ corregido).
- Sección "lo que las imágenes cuentan como historia" (lens Content: registro del personaje *"host, not performer"*, firma lumínica, qué escena vende la oferta sin decir de más).
- **Master prompt en 3 bloques** (IDENTITY-LOCK atómico / STYLE-LOCK / NEGATIVOS) heredado del producer + aderezos de voz, sin tocar anatomía.
- Checklist del estándar que se lleva la agencia para futuras campañas.
- Pendientes que requieren nombre/aprobación del Admin (gate de gasto, cartón de Sc4, regeneraciones).

## Workaround cuando auxiliary.vision del perfil no acepta imágenes
Síntoma: `vision_analyze` responde descripciones HIPOTÉTICAS construidas desde tu propio prompt ("no se ha proporcionado ninguna imagen, pero…") — output inventado, peligroso. Fix (script `workspace/lucky_qa_bragi.py`): llamada directa a qwen3.6 vision en `https://api.nan.builders/v1/chat/completions`, NAN_API_KEY del `/root/marketing-campaign-generator/.env`, imagen a ≤768px JPEG base64. Pitfalls del endpoint: `max_tokens`≥3000 (con 900 trunca → `content` vacío con finish_reason=length; leer `reasoning_content` como fallback), curl --max-time 240, 3 intentos. Nota infra: reportar en sala el config roto (`auxiliary.vision: deepseek-v4-flash@B.AI` no soporta visión) para que lo arregle quien tenga permisos — no hardcodear la limitación como permanente.

## Gate de gasto
Nunca disparar Seedance/fal sin `/root/marketing-campaign-generator/.spend-gate.json` creado por humano (approved_by + purpose + expira 6h). Pedir aprobación con nombre explícito en la sala.
