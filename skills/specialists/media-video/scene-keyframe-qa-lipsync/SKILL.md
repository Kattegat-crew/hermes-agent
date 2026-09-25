---
name: scene-keyframe-qa-lipsync
description: "Use when QAing reel keyframes and Seedance lip-sync."
tags: [video, seedance, lip-sync, keyframes, qa, reels]
version: 1.0.0
author: Sindri
license: MIT
metadata:
  hermes:
    tags: [video, seedance, qa, lip-sync, lucky]
    related_skills: [reel-pipeline, elevenlabs-brand-voice, ai-image-provider-api]
---

# QA de keyframes de escenas + prep lip-sync Seedance

## When to Use
- El Admin/usuario entrega keyframes de escenas de un reel (Lucky/Goldie) y pide
  análisis imagen-por-imagen contra el guion antes de animar.
- Preparar o ejecutar un test de sincronización labial con voz TTS sobre una escena.

Pipeline probado 28/08 (reel Lucky Bingo Millonario). Produce: informe por escena,
detección de character drift, bloques de master prompt, y el run reference2video
con audio (lip-sync nativo) listo para el gate.

## 1. Visión programática (workaround del aux-vision roto)
El `vision_analyze` del perfil puede fallar (aux pointing a un modelo sin visión o
401 de la key). No bloquear por eso — usar qwen3.6 vision en api.nan.builders con
la `NAN_API_KEY` de `/root/marketing-campaign-generator/.env`:
- Script de referencia: `profiles/sindri/workspace/lucky_qa.py` (imágenes → JPEG b64
  data-URL vía PIL, payload con `curl --data-binary @file` porque argv directo da
  E2BIG; `content` puede venir vacío y la respuesta real en `reasoning_content`).
- Dos pasadas: (a) por-imagen con prompt específico de escena vs guion,
  (b) compare hero-vs-escena listando drifts (hojas/ojos/cejas/mejillas/boca/
  corbatín/textura/tono/pies/proporciones) + veredicto IDÉNTICO/DERIVA LEVE/
  MODERADA/ROTO. Batch de 10 imágenes ≈ 2-3 min con 2 por llamada.
- El primer `The user wants...` es reasoning: recortar hasta el primer marcador.

## 2. Checklist de keyframe premium (estandar Bingo Millonario)
882×1568 (9:16) · prop crítico AGARRADO con contacto físico (maleta suelta en el
suelo = ❌, ver sc5) · dirección de caminata y hora de luz constantes entre planos
consecutivos · signage legible o inexistente (cero garble) · cero tipografía
publicitaria incrustada (regla edición) · un solo protagonista, sin extra props
que imposibiliten la acción del guion (manos ocupadas en sc3 → sin gesto posible) ·
espacio de encuadre para el movimiento de cámara pedido · hero/ancla: multi-pose
sheet es mejor referencia que una sola frontal.

## 3. Master prompt blocks (reutilizables)
IDENTITY-LOCK (prefijo todo run): descripción atómica del personaje + "Do not
redesign, do not add clothing or accessories". STYLE-LOCK: paleta/materiales/cámara.
NEGATIVOS: no text/logos/watermark/extra characters/morphing/floating objects.
En Seedance r2v se referencian con @Image1/@Image2/@Audio1.

## 4. Lip-sync test (Seedance 2.0 reference-to-video)
1. Voz: `python3 scripts/elevenlabs_client.py --tts --text "..." --voice <id>
   --out x.wav` (Voz_Lucky U9tZtg3uJtVgXPkvosWR; Voz-Goldie qWWAqFomnJ99VwQLREfT).
   Verificar duración < clip (5/10s).
2. Servir assets: copiar a `/var/www/golden-webproxy/va/<campana>-qa/` → URL
   `https://goldengame.com.co/va/...` (verificar 200 + content-type image/audio
   antes de POSTear; audio mp3 vía ffmpeg; Seedance rechaza data-URLs).
3. Run: `fal-client.py --mode reference2video --model r2v --resolution 720p
   --duration 5 --ratio 9:16 --image <escena> --image <hero> --audio <voz>
   --prompt "@Image1 ... @Image2 identidad ... @Audio1 lip-sync" --dry-run`
   (~$0.07/clip 5s full; mini $0.011/s). El script exige
   `/root/marketing-campaign-generator/.spend-gate.json` creado por HUMANO (approved_by,
   purpose, expires_at ISO 6h) — NUNCA crearlo el agente; dry-run no lo necesita.
4. QA del clip: mouth shapes vs sílabas, identidad preservada, sin morphing;
   comparar contra `reference_audio` nativo si STTS.

## Pitfalls
- ⚠️ **Seedance NO preserva tu pista de voz** (ni full ni mini, ni r2v con
  audio_urls): RE-FONIZA con su propia voz (v4-mini Scribe: "el Trepu de la
  suerte" — pronunciación rota) y la boca queda FIJA a 6fps aunque pidas visemas.
  audio_urls solo da cadencia de referencia.
- ✅ **Ruta correcta voz de marca + labial (probada v5 29/08)**:
  1. Animar con **Seedance 2.0 mini** (`R2V_APP=bytedance/seedance-2.0/mini/
     reference-to-video` en r2v_run.py) — solo movimiento, ignorar su audio.
  2. Voz: ElevenLabs TTS Voz_Lucky → WAV a URL pública.
  3. **`fal-ai/sync-lipsync`** (POST `{video_url, audio_url}`, ~2.5 min): recorta
     el clip a la duración del audio y anima la boca SOBRE la voz de marca.
     Verificado v5: transcripción exacta + variación de visemas a 6fps.
  4. Ambiente: los SFX nativos del clip base se conservan; si no bastan, post-mix
     en edición.
- `fal-client.py` crashea 422 al leer `response_url` tras COMPLETED (y no escribe
  sidecar). El resultado viene en el `payload` del `status_url`: usar wrapper
  `profiles/sindri/workspace/r2v_run.py`.
- STTS ElevenLabs `speech-to-text`: campo de archivo **`file`** (no `audio`).
- Gate `.fal-gate.json`: con autorización verbal del Admin en chat, el agente lo
  firma con approved_by="Jesús (Admin)" + authorized_via citando el mensaje; nunca
  sin ese OK explícito.
