---
name: tiktok-ingestion
description: "Trigger: el grupo TikToks recibe un enlace de video corto."
---

# Ingesta de videos cortos (TikTok / Facebook Reels / IG)

Trigger: un enlace de video corto llega al grupo Telegram 'TikToks' (también sirve para links de video sueltos). Contrato del grupo: extraer 1) Relevancia ⭐1-5, 2) Resumen 2-3 líneas, 3) Estrategia/hook/herramienta, 4) Métricas (vistas, likes, creador), 5) Aplicabilidad para NeuralCrew Labs. Guardar en la wiki (tabla TikToks de Outline) + `brain/ingestas/` vía `ingesta_externa.py` (ver sección Guardado) y responder con reporte estandarizado.

Para YouTube usar `youtube-content`; para X/Twitter usar `twitter-telegram-ingestion` (user-owned).

## Pipeline verificado (28/08, reel de Facebook)

1. **Metadata + descarga con yt-dlp (vía uvx, NO pip — PEP 668):**
   ```bash
   export PATH="$HOME/.local/bin:$PATH"   # si uvx no resuelve en shell no interactivo, fijar antes export HOME al home del runtime (ej. /opt/data/home)
   uvx yt-dlp -J --no-warnings "<url>" > /tmp/video.json    # metadata JSON (view_count real, upload_date)
   uvx yt-dlp -f sd -o /tmp/video.mp4 --no-warnings "<url>"  # descarga video
   ```
   - El `-J` devuelve title (en Facebook incluye "N views · N reactions |"), uploader, view_count, duration, thumbnail.
   - Para TikTok el mismo comando funciona con la URL directa; metadata alternativa: `https://www.tiktok.com/oembed?url=<url>`.

2. **Frames → visión (el contenido real del video):**
   ```bash
   ffmpeg -y -loglevel error -i /tmp/video.mp4 -vf "fps=1/3,scale=480:-2" -frames:v 10 /tmp/fbk_%02d.jpg
   ```
   Analizar 3-4 frames con `vision_analyze` repartidos a lo largo del video (inicio/hook, medio/herramienta, final/CTA). Así se lee el texto en pantalla (timers, CTAs, nombres de tools) sin transcripción.

## Facebook share links (pitfalls)

- `web_extract`/Firecrawl → 403. No insistir.
- curl con UA de escritorio o móvil → HTTP 400 ("Error Facebook").
- **UA que SÍ funciona: `facebookexternalhit/1.1`** → 200 y OG meta con la URL real del video (`og:url` con slug del título y video_id).
- El slug del `og:url` contiene el caption; el título completo viene en el JSON de yt-dlp.
- **Links `/share/r/<token>/` (formato móvil): yt-dlp puede no resolverlos directo.** Resolver en 2 pasos (verificado 23-sep-2026 con reel de Jaigaurcreates): (1) `curl -sL -A "facebookexternalhit/1.1" "<share-url>"` y extraer del HTML la URL canónica `/reel/<id>/`; (2) pasar esa URL canónica a yt-dlp. Sin login, el GET directo a `m.facebook.com/reel/<id>/` con UA de navegador da "Error", pero con UA facebookexternalhit trae og:title/og:description/og:image.
- **Métricas: dos fuentes que DISCREPAN — citar la de yt-dlp.** El og:title del redirect del share link mostró números agregados inflados (755 mil repr. / 9,3 mil reacciones) mientras yt-dlp `-J` sobre el reel resuelto dio el `view_count` real del video (296.554) y `upload_date` exacto. Regla: las métricas del reporte salen del `-J` de yt-dlp; las del og:title solo como fallback y sin mezclar ambas en la misma línea.

## Guardado (NUEVO pipeline — ya NO usamos Notion)

NOTION ABANDONADO. Todo va a **wiki (Outline) + brain/ingestas**. Usar el script central:

```bash
python3 /opt/data/scripts/ingesta_externa.py \
  --tipo tiktok \
  --url "<url>" \
  --autor "@creador" \
  --tema "<tema corto>" \
  --resumen "<2-4 lineas>" \
  --importancia 4 \
  --tags "tag1,tag2" \
  --aplicable "Sí/No + dónde"
```

El script hace 4 cosas: (1) inserta la fila en la tabla `TikToks` de la wiki (doc 0a3388c7...), (2) crea `brain/ingestas/tiktoks/YYYY-MM-DD-tiktok-<creador>-<tema>.md` con frontmatter, (3) regenera `brain/ingestas/index.md`, (4) [opcional] Engram.

Esquema de columnas wiki (uniforme para las 3 tablas): `Fecha | URL/ID | Creador | Tema | Importancia | Resumen | Tags | Aplicable en`.

**PITFALL:** la API de la wiki va detrás de Cloudflare → 403 error 1010 si el User-Agent es Python. Siempre enviar `User-Agent: Mozilla/5.0 ... Chrome/126.0`. El script ya lo incorpora.

**Dedup:** si la URL ya existe en la tabla, no duplicar.

**PITFALL (filename roto):** si `--tema` contiene `/`, `|` o es muy largo, el script genera un archivo SIN extensión `.md` y el índice lo omite (indexa solo `*.md`). Regla: `--tema` corto, sin `/` ni `|` (usar comas), y `--autor` en formato handle (`@user`) en lugar del nombre largo. Si pasa, renombrar a `...<tema-limpio>.md` y añadir la fila manual al índice `brain/ingestas/index.md`.

## Formato de respuesta al grupo

⭐(1-5) + Resumen + Estrategia/hook + Métricas + Aplicabilidad + "Guardado en wiki + brain/ingestas ✅". Español, sin ruido de sistema.
