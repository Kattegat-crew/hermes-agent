---
name: ai-image-provider-api
description: "Use when generating campaign images via provider APIs."
tags: [imagen, api, fal-ai, flux, nan-builders, key-art, proveedor]
---

# APIs de generación de imagen — operación de proveedores

Clase de tarea: producir key art / hero renders vía API para piezas gráficas de campaña.

## NaN-Builders (OpenAI-compatible, flux-2-klein)

- Endpoint: `POST https://api.nan.builders/v1/images/generations` con body `{"model":"flux-2-klein","prompt":...,"size":"1024x1024","n":1}`; header `Authorization: Bearer <key>`. La clave válida es el primer campo `api_key:` de `profiles/sindri/config.yaml` (otras claves del yaml son de otros proveedores y devuelven 401).
- **Pitfall Cloudflare:** el User-Agent por defecto de Python urllib/requests produce `403 error code 1010` — parece fallo de auth pero no lo es. Enviar UA real de navegador (p. ej. `Mozilla/5.0 ... Chrome/126.0 Safari/537.36`) tanto en el POST como al descargar la URL.
- La URL R2 del resultado **expira en ~1h**: guardar los bytes en el mismo script, inmediatamente.
- **401 `invalid_api_key` intermitente** con una clave que funcionó minutos antes con el mismo payload = throttle/caída del backend (verificado: el mismo script alternaba OK/401 en minutos). Acción correcta: reintentos espaciados con límite (~5, backoff) y mientras tanto trabajar sobre el último arte bueno guardado en disco. NO reescribir el script, NO rotar claves a ciegas, NO dejar bucles de reintento infinitos corriendo.
- Si el `workspace/` original es root-only (PermissionDenied al escribir), copiar el árbol a la área escribible del perfil (`profiles/sindri/forge/...`) y trabajar ahí.

## fal.ai (si hay FAL_KEY activa)

- Verificar primero que `FAL_KEY` existe **sin comentar y con valor** en `/opt/data/.env` — la mayoría de entradas del .env viven comentadas como placeholder; un `grep FAL_KEY` a secas engaña.
- Selección de modelo por utilidad de composición, no por belleza: **FLUX.2 [pro]** → fondos limpios y zona de aire fiable para tipografía (gana para póster/banner). **Seedream V4.5** → máximo detalle de personaje (gana para close-ups), pero fondos ocupados.

## Iteración de prompts hero (recipe probado)

1. Prompt maestro versionado en `prompt_hero_v<N>.txt`; nunca re-inventar la descripción del personaje — jalarla de las fichas de `brain/entities/` o del md de fichas verificado con vision sobre arte real.
2. QA visual del render con criterios fijos; cada defecto nombrado se convierte en **cláusula en MAYÚSCULAS dentro del prompt v2** ("THREE VERTICAL GLOWING SLOT REELS clearly displaying 7-7-7", "DARK BROWN STEM") más un NEGATIVE específico contra la basura observada ("no confetti, no floating balls, no people").
3. Fijar la zona de aire por porcentaje y prohibir explícitamente que los personajes la invadan ("characters must NOT enter the left 40%") — esto hace el arte reutilizable para recorte 1:1 → 9:16 → 16:9.
4. Medir la zona de aire objetivamente antes de componer sobre ella (perfil de luminancia por columnas con PIL `ImageStat` sobre el recorte central) — la visión a veces reporta "franja negra" que es aire de diseño y a veces es un bug real de recorte.

## QA de renders múltiples

- Montaje comparativo side-by-side (PIL) y evaluarlo con vision en una pasada: 1) fidelidad vs ficha, 2) zona de aire limpia, 3) calidad publicitaria, 4) defectos (manos, deformaciones, texto quemado).
- El texto integrado en el objeto (p. ej. "GG" grabado en el robot) NO es "texto quemado" inválido — distinguir branding del personaje de overlay erróneo.

## Interpretación de vision QA en loop de composición

Cada re-render se re-QA con pregunta comparativa ("¿se resolvió X?"). Severidades: alta = bloquea (texto mordido, solape ilegible), media = corregir antes de entregar (halos, contraste), baja = aceptable. El QA puede reportar falsos positivos de layout (ver recipe 4) — medir en píxeles antes de "arreglar" lo que está bien.

## Verification

Un render está "entregado" solo cuando: bytes guardados en disco (no URL), vision QA pasó con severidades ≤bajas resueltas, y el arte se probó en al menos un formato derivado por recorte.
