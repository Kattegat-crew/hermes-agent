---
name: reel-voice-lipsync
description: "Use when a reel needs correct pronunciation and lip-sync."
tags: [reels, lipsync, voz, tts, elevenlabs, fal, pronunciacion, video]
---

# Voz de marca + lip-sync para reels de personaje IA

Clase de trabajo: darle a un reel de personaje IA (Seedance/Monid u otro
image-to-video) una voz de marca en español con pronunciación CORRECTA y labial
REAL, sin regenerar el video ya pagado.

## La decisión: 3 caminos y cuándo sirve cada uno (lección central 29/08)

| Camino | Pronunciación | Labial | Cuándo usar |
|---|---|---|---|
| Respelling en prompt de Seedance | ❌ no obedece (la voz nativa no es TTS que lee texto) | congelado | nunca como solución |
| **STTS ElevenLabs** (audio→audio) | ❌ **COPIA la pronunciación del audio fuente** (verificado: hereda "trevól"/"Parodise") | no lo toca | solo para cambiar TIMBRE conservando cadencia, cuando la pronunciación fuente ya es buena |
| **TTS desde texto corregido + sync-lipsync** | ✅ el texto lo escribe el agente (respelling funciona) | ✅ re-dibuja labios siguiendo la voz | **ESTÁNDAR** para reels de personaje hablando |

⚠️ La skill `elevenlabs-voice-narration` documentaba el STTS como "la solución para
re-hacer el audio" — es INCORRECTO para corregir pronunciación (user-owned, pendiente
`hermes curator adopt` para enmendar). No repetir ese camino.

## Receta validada (S1 Lucky, 29/08, end-to-end publicado)

1. **TTS desde texto corregido**: `POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id}?output_format=mp3_44100_128`, body `{text, model_id: "eleven_multilingual_v2", voice_settings:{stability:0.5, similarity_boost:0.75, style:0.15, use_speaker_boost:true}}`, header `Accept: audio/mpeg` → MP3 crudo. Respelling: "Paradais", sílabas separadas, números en palabras.
2. **Calzar voz al clip**: `ffmpeg -filter:a "atempo=<ratio>"` — ratio = dur_voz/dur_clip (8.59s→8.10s = atempo 1.0611, imperceptible hasta ~6-8%).
3. **Publicar WAV en URL https pública** (el proveedor descarga el audio; localhost no sirve). Regla vigente: verificar con fetch EXTERNO (web_extract), no curl del propio VPS.
4. **sync-lipsync (fal.ai queue async)**: POST `https://queue.fal.run/fal-ai/sync-lipsync` con `{video_url, audio_url, sync_mode: "cut_off"}` → `request_id` + `status_url`; poll cada 5-10s; al COMPLETED descargar de `response_url`. Duración real: ~5 min (no 2.5 como se estimó). Output viene RECORTADO a la voz (8.10s→8.04s: despreciable en clips de 8s).
5. **Publicar como versión NUEVA** y QA (abajo).

Costo real por escena: **$0.07 sync-lipsync** (fal) + TTS por caracteres (créditos ElevenLabs, céntimos). El clip de video NO se regenera — se aprovecha el ya pagado.

## QA del labial: frames RECORTADOS a la cabeza (falso negativo documentado)

Una grilla de frames de cuerpo completo hace que el modelo de visión diga "boca
congelada/idéntica" AUNQUE el labial esté perfecto (píxel de boca insuficiente).
Procedimiento correcto:
1. Extraer 4-6 frames (`-ss 0.5/1.5/2.5/4.0/5.5/7.0`).
2. Recortar cabeza: `-vf "crop=720:500:0:200"` para 720×1280.
3. `hstack` y preguntar: "¿la boca cambia de forma entre paneles (abierta con dientes / entreabierta / forma O) o es idéntica?".
Con crop se distingue articulación real de boca fija; sin crop, un falso negativo
lleva a re-pagar un lipsync innecesariamente (casi pasó 29/08).

## El camino sin lipsync: TTS calibrado para montaje en CapCut (Goldie Bingo, 30/08 — aprobado "quedó muchísimo mejor")

Cuando Seedance ya animó el labial al ritmo de SU voz nativa, no hace falta re-dibujar
labios: basta calzar la voz de marca al ritmo nativo. Script canónico:
`scripts/fit_voice.py` del repo video-ai-generator (commit 522a1ea). Receta:

1. STT palabra-por-palabra del audio nativo del clip (extraer a 16k mono) = guía del labial.
2. STT del WAV TTS crudo; `atempo = span_tts / span_nativo` (TTS español suele hablar
   12-40% más rápido; S1 Goldie quedó en 0.744, S4 con números largos en 0.609).
3. Pad de silencio INICIAL = onset(1ª palabra nativa) − onset(1ª palabra estirada), para que la
   primera palabra caiga donde la boca empieza (S3 necesitó 1.0s de pad).
4. `apad=whole_dur=<dura_exacta_del_clip>` → el WAV dura lo mismo que el video: en CapCut se
   silencia la pista nativa del mp4 y el WAV se suelta en el 0:00, sin afinar nada.
5. Loudnorm −16 LUFS integrado + highpass 90 Hz. QA automático: delta medio/peor por palabra
   (aceptable ≤0.2s medio; S1 Δ0.02 worst 0.18 → aprobado).
6. Opcional `--mp4`: pre-monta clips/S{n}-vozlimpia.mp4 (video+voz limpia) para que el Admin
   valide el resultado final sin abrir el editor.

**PITFALL GRAVE (causó queixa "se escucha Seedance al fondo")**: en una mezcla con
"ambiente", NO usar el audio del propio clip como fuente del ambiente — arrastra la voz
nativa (bleed) y suena doble. Verificar el entregable con STT: debe transcribir UNA sola
voz. Lo que el editor oye "de fondo" al montar es casi siempre la pista nativa sin silenciar
del mp4 → primero explicar "silencia el audio del clip en CapCut" antes de tocar nada.

## Reglas NO negociables

- **Gate humano para todo gasto** (`.fal-gate.json` firmado por el Admin, 6h; Monid análogo). 'dale/arregla la escena N' = autorización explícita registrable.
- **Galería versionada, JAMÁS borrar**: el Admin quiere ver la evolución (S1.mp4 nativa → S1-vozmarca STTS → S1-lipsync final). Cada versión se agrega, nunca se reemplaza; etiqueta textual de qué es cada una.
- El QA visual se hace ANTES de anunciar el resultado al Admin, no después.
- Verificación externa de URLs publicadas (el curl interno del VPS miente).

## Pitfalls

- `elevenlabs_client.py --stts` del repo puede devolver salida no-audio (bug wrapper): llamar el endpoint directo con `Accept: audio/mpeg` y decodificar con ffmpeg.
- El atempo >1.08 se nota (voz apurada); si la voz excede mucho el clip, recortar texto, no estirar más.
- `sync-lipsync` v2 puede no existir/NoFound: el modelo base `fal-ai/sync-lipsync` verificado vivo 29/08.
- El wrapper de Monid (`monid-client.py`) no acepta params de audio/lipsync — la corrección de voz SIEMPRE es capa posterior, no parámetro de generación.
- El output de lipsync recorta el video a la duración de la voz: para tails sin diálogo, concatenar el tail desde el clip original en CapCut.

## Referencias

- **Herramienta principal**: `scripts/fit_voice.py` (repo video-ai-generator) — calibración TTS↔labial genérica por proyecto (`--project --scenes S1..S6 --voice-substr goldie --mp4`).
- Scripts históricos 29/08: `/tmp/tts_s1.py` (TTS directo), `/tmp/lipsync_s1.py` (submit+poll fal queue).
- Skills hermanas (user-owned, NO editar sin adopt): `elevenlabs-voice-narration` (timbre/STTS), `video-tts-pronunciation-fix` (respelling), `video-ai-generator` (repo/pipeline), `scene-consistency-qa` (QA de stills).
