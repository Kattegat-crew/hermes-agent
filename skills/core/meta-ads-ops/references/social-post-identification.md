---
name: social-post-identification
version: 1.0.0
author: Ragnar
license: MIT
description: Use when a social post needs caption extraction or tool ID.
tags: [instagram, ingesta, viral, identificacion, github, verificacion]
related_skills: [ingest-pipeline, web-research-briefing, twitter-telegram-ingestion, tiktok-ingestion, agent-reach]
---

# Identificación de posts sociales y de la herramienta detrás de un post viral

**Cuándo:** llega un link a un post social (IG/TikTok/X) para ingestar, y hay que (a) extraer el caption sin sesión y (b) identificar la herramienta/producto real cuando el post no lo nombra. Complementa a `ingest-pipeline` (el pipeline de guardado), que no cubre NINGUNA de las dos cosas.

## 1. Extraer el caption de Instagram

La escalera verificada vive en `references/extraccion-social-instagram.md`. Resumen:

- `web_extract` directo y el HTML de IG son trampas: IG responde **200 con ~627 KB que NO contienen metadata útil** (solo `<title>Instagram</title>`). No pierdas turnos parseando ese HTML.
- **Vía viva: `curl https://r.jina.ai/<url-completa>`** → devuelve `Title: <Autor> on Instagram: "<caption completo>"` en markdown.
- Vías muertas verificadas: `?__a=1&__d=dis` (Page Not Found), `ddinstagram.com` (timeout), `web_extract` sin FIRECRAWL_API_KEY (403).
- Si solo sale el caption, decláralo: el contenido de los slides NO queda verificado.

## 2. Post viral que NO nombra la herramienta (CTA "comenta X y te mando el link")

El link se regala por DM para farming de comentarios: el post nunca dice qué es. Receta en 4 pasos:

1. **Posts gemelos del mismo guion**: `web_search` con la frase distintiva del caption traducida al inglés + "instagram". Los reels gemelos en inglés suelen sí nombrar la herramienta.
2. **GitHub Search API**: `curl -s "https://api.github.com/search/repositories?q=<nombre>&sort=stars"` → repo canónico + forks (las variantes offline/CLI traen README con stack, requisitos y coste que el post omite).
3. **Verificar los claims del guion**: métricas con `/repos/<owner>/<repo>` (stars, forks, license, pushed_at — citar con fecha); funding con prensa (36kr, Preqin, TechCrunch). Lo que el post afirma y la prensa no confirma → marcarlo no verificado en la ingesta.
4. **Ingestar apuntando al repo**, no solo al post: el post caduca, el repo es la fuente viva.

## 3. Calidad del .md en brain/ingestas

Los archivos que solo llevan frontmatter + resumen quedan pobres frente a la convención de cuerpo desarrollado: añadir sección `## Análisis` con los datos verificados (qué es, cómo funciona, métricas del repo con fecha, stack/coste, caveats de licencia, aplicación concreta para NeuralCrew).

## Pitfalls

- Un post viral es fuente secundaria: los claims del guion («20 años», «$4M en 24h») van marcados como verificados SOLO si prensa independiente los confirma.
- La licencia importa para la aplicabilidad (AGPL-3.0 no es embebible en SaaS de cliente sin revisión legal): mírala en `/repos/<owner>/<repo>` antes de sugerir uso.
- Si la identificación queda como hipótesis fuerte pero sin confirmación del propio post, dilo explícitamente en la nota de la ingesta.
