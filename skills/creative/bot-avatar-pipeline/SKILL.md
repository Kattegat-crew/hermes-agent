---
name: bot-avatar-pipeline
description: "Use when: generar/validar/instalar avatares de bots."
category: media-production
version: 1.0.0
---

# Bot Avatar Pipeline (NeuralCrew)

Pipeline completo para que los bots de la tripulación tengan avatar verificado: generación → QA visual → instalación en el perfil → entrega. Complementa a `quality-check-visual` (checklist QA) y a `flux-models`/`brand-assets-library` (generación/identidad). Entorno NeuralCrew: bots crew = hermodr, bragi, brokkr, freyja, heimdall, sindri, ullr, vili.

## Cuándo usar
- "genera avatares para los bots", "cambia la foto de perfil de X", "las imágenes no corresponden al bot", "configúralo como imagen de cada bot".

## Pasos
1. Localizar el lote: `/opt/data/deliverables/avatares-tripulacion/` (`gen_avatares.py` define las fichas por bot con STYLE+NEG común; API NaN-Buiders flux-2-kein en `https://api.nan.buiders/v1/images/generations`, respuesta b64_json; leer API key del config.yaml del perfil).
2. QA visual de CADA archivo con `vision_analyze` — NO fiarse del nombre del archivo. Preguntar por: quién aparece, objetos en cada mano, nº de manos visibles y dedos, objeto fusionado al cuerpo (p.ej. cuerno "saliendo del hombro"), fondo. Limíte: ≤2-3 llamadas por turno (429 si >5 paralel).
3. Si un avatar falla: regenerar 2-3 candidatos con prompt ENDURECIDO (anatomía explícita: "exactly two hands with five fingers each, only this single figure, no other people, the object held clearly in his hand and separate from the body, nothing growing out of the shoulder"), QA cada candidato y promover el mejor al archivo canónico. Conservar el STYLE base del lote para consistencia.
4. Contact sheets/mosaicos: verificar el pareado etiqueta↔imagen CELDA POR CELDA con visión. El corrimiento de 1 posición (imagen[i] bajo label[i-1]) es el fallo típico al armar mosaicos (pasó con los 8 avatares: las 5 primeras celdas estaban corridas).
5. Instalar en el perfil: copiar a `/opt/data/profiles/<bot>/assets/avatar.png` (512×512 PNG) + `avatar-<bot>.jpg` (1024×1024 JPEG q92). SIEMPRE backup previo (`backup-assets-YYYYMMDD/`).
6. Verificar post-install: tamaños con Pillow (`uv run --with pillow`; `UV_CACHE_DIR=/tmp/uvcache` si /opt/data/.cache/uv no es escribible), y visión sobre 1-2 instalados.
7. Entregar con `MEDIA:` (archivos reales).

## Pitfalls
- No fiarse del nombre del archivo para saber qué bot muestra (puede no coincidir con el prompt).
- Manos extra sobre objetos del protagonista (2ª figura tocando) y objetos fusionados al cuerpo son fallos clásicos de flux-2-kein en retratos con props.
- `vision_analyze` en paralelo: rate-limit 429 si se lanzan ≥5; lote pequeño.
- Pillow no está en el python del sistema; usar `uv run --with pillow`.
- Los avatares viejos pueden quedar cacheados por la app cliente aunque el servidor ya sirva los nuevos (ver `references/desktop-avatar-delivery.md`).

## Referencias
- `references/desktop-avatar-delivery.md` — modelo de entrega al Hermes Desktop: dónde vive el avatar, quién lo lee (get_asset fresco vs UI web hardcodeada), y diagnóstico cuando el usuario "no ve" los cambios.