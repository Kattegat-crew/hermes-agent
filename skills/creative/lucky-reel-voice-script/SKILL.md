---
name: lucky-reel-voice-script
description: "Guiones de voz para reels con lip-sync pos-generado."
---

# Guion de voz para reels con lip-sync pos-generado

Cadena aprobada (Lucky/Bingo Millonario, 29/08): `Seedance mini clip → fal-ai/sync-lipsync con WAV ElevenLabs`. El modelo no obedece visemas ni respeta la voz de marca (refoniza); el labial se hace sobre los píxeles DESPUÉS.

## Consecuencias para el guion de voz (mi lens, Content)

1. **El clip se recorta a la duración del audio** (sync-lipsync). Si una línea TTS mide más que la escena del storyboard, la escena final queda cortada o hay que regenerar TTS más rápido/rasurado. Regla: medir cada línea con Voz_Lucky ANTES de dar por aprobado un guion de video; presupuestar ≥1s de aire al final para gestos de cierre (saludo, "¡Suban!").
2. **Nada de música pedida al generador** — el Admin pone música en edición. Los prompts piden SFX diegéticos nombrados explícitamente (pasos sobre pavimento mojado, ruedas de maleta, ambiente terminal) y niegan música ("no music, no soundtrack, no singing").
3. **Ritmo del habla = ritmo del reel**: medir con Voz_Lucky real — **~2.2 palabras/seg** (medido por Sindri 29/08; no fiarse de estimaciones de 2.7). Digits se leen expandidos ("53" = "cincuenta y tres"). Las cinco líneas del guion maestro deben caber en sus tramos del §11 con ±0.5s. Si una línea no cabe, primero `--speed 1.1–1.3` en ElevenLabs (Sindri validó L3 a 1.3 → 6.5s), y solo si aún no cabe se acorta la FRASE, nunca la escena.
4. **Voz de marca siempre ElevenLabs** (Voz_Lucky), nunca la nativa de Seedance como plan A. La nativa solo como cadencia/referencia.

## Plantilla de prompt motion (lo que le toca a Content refinar por escena)

- Identity/style locks + acción + registro ("host, not performer") + SFX diegéticos + negaciones (no text, no morphing, no extra characters, no music).
- NO incluir órdenes de visemas (ineficaces en esta cadena).
- Entregar al lip-sync una cara claramente hablando: "talking directly to camera, mouth open mid-word".

Referencia: workspaces bragi/sindri (`PROMPT_MOTION_SC1_v2_lipsync.md`, `ANALISIS_GUION_IMAGENES_LUCKY_bragi.md`) y skill de pipeline de Sindri `scene-keyframe-qa-lipsync`.
