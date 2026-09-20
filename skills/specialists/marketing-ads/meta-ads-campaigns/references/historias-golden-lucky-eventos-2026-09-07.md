# Historias de evento publicadas — Golden + Lucky (07/09/2026)

Relevante para: publicar historias de evento del cliente en IG via Composio (conector `composio-social-publishing`, user-owned).

## Regla del Admin (Jonathan, verbatim) — EMBED
- **SIEMPRE a ambas cuentas** (IG + FB).
- Material **TAL CUAL** — sin cartela, sin logo, sin overlay de marca. La edición on-brand es solo para piezas promocionales que el Admin pida.
- **Videos: cortar a 15-20s. Fotos: publicar en story** (IG fija la duración, no se configura).
- Siempre **1080x1920**.

## Cuentas
- **Golden:** IG @goldengame_casinos (ig_user_id `40006158832316994`, word_id `instagram_demal-molala`). Página FB Golden `820898971112738`.
- **Lucky/Paradise:** IG @thegrandparadiseclubcasino (ig_user_id `27571270162548342`, word_id `instagram_scot-linked`). Página FB Paradise `765896786617957`.

## 8 historias GOLDEN publicadas (media IDs)
| # | Pieza | Media ID |
|---|---|---|
| 01 | Sándwiches (foto) | 18130646068677491 |
| 02 | Ambiente casino (foto) | 18072455828663861 |
| 03 | Ganador Luis Cañón (foto) | 18264437386305693 |
| 04 | Bingo grito (video 14.3s) | 18408184309085313 |
| 05 | Casino Cachipay (video 20s) | 18619027276016912 |
| 06 | Bingo Cachipay animadora (video 18.98s) | 17982605160117288 |
| 07 | Bingo Cachipay ganadores (video 15s) | 18131866375729666 |
| 08 | Bingo Cachipay foto | 18126421621700365 |

## 6 historias LUCKY publicadas (media IDs)
| # | Pieza | Media ID |
|---|---|---|
| 01 | Chiquinquirá 2 video 20s (corte 20-40s) | 18052434608646603 |
| 02 | Primer bingo corto $50K (corte 230-250s) | 18091957493140306 |
| 03 | Segundo bingo corto $100K (corte 72-90s) | 18103920629367292 |
| 04 | Bingo pleno $400K acumulado (corte 36-52s) | 18087494537225000 |
| 05 | Ganador con dinero (corte 36-56s) | 18172139149454976 |
| 06 | Foto "BUENA SUERTE" pleno $400K sin ganador | 17959808990992570 |

## Cortes elegidos (verificados con contact sheet + vision_analyze)
- Video 53.9s (Cachipay evento) → 0-20s: abre con cartel "Bingo Millonario" (gancho), jugadores, animador.
- Video 58.8s (Cachipay bingo) → 20-35s: ganador muestra cartón de bingo + billetes posando con personal (clímax).
- Video 260s (Chiquinquirá 2) → 230-250s: clímax final (mesa de bingo, presentadora, cierre).
- Video 96s → 72-90s: jugador clave, concentración de gente, expectativa de premio.
- Video 52s → 36-52s: entrega de premio, presentadora celebrando con ganador.
- Video 55s → 36-56s: ganador mostrando dinero y cartón con empleada.

## Flujo publicado (2 pasos, script Python)
```py
# 1) crear container STORIES (foto o video)
INSTAGRAM_POST_IG_USER_MEDIA -d '{"ig_user_id":"<ig>","media_type":"STORIES","image_url":"<public>"}'   # foto
INSTAGRAM_POST_IG_USER_MEDIA -d '{"ig_user_id":"<ig>","media_type":"STORIES","video_url":"<public>"}'   # video
# -> data.id = container/creation_id
# 2) publicar
INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH -d '{"ig_user_id":"<ig>","creation_id":"<container>"}'
# -> data.id = media id
```
- Build `-d` en Python (`json.dumps`), leer stdout+stderr.
- **Video >20MB puede dar timeout en el paso container** (default 60s) → subir con `timeout>=280s`; éxito reporta `Container reached FINISHED status after Ns`.
- **Upscale low-res (368x496/478x850) tarda** → ffmpeg con timeout 200-400s.

## FB Stories — limitación del conector
El conector Composio NO expone FB Stories (solo feed: `FACEBOOK_CREATE_PHOTO_POST`). Para que IG Story llegue a FB, activar **crossposting IG→FB** en Meta Business Manager (Business Settings → Instagram Accounts → vincular la cuenta → "Compartir historias en Facebook" ON) — se hace una sola vez. Hasta entonces las historias van SOLO a IG. Informar al Admin.

## Hosting de assets
Subir a `/opt/reels/assets/<slug>` vía `scp` a `root@100.73.30.29`, verificar URL HTTP 200 con cache-buster `?v=<epoch>` (Cloudflare cachea 404). `reels.neuralcrewlabs.com` sirve `/opt/reels/` estáticamente.
