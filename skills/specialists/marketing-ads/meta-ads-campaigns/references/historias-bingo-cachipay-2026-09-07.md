# Historias publicadas — Evento Bingo Cachipay (07/09/2026)

**Regla del Admin (verbatim):** SIEMPRE a ambas cuentas (IG + FB) · material TAL CUAL (sin cartela/logo/overlay) · videos cortar a **15-20s** · **fotos 10s**.

## 8 historias publicadas en IG @goldengame_casinos (ig_user_id 40006158832316994, word_id instagram_demal-molala)
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

## Cortes elegidos (verificación vision_analyze con contact sheet)
- **Video 53.9s (Cachipay evento):** cortar **0-20s** — abre con cartel "Bingo Millonario" (gancho), jugadores, animador.
- **Video 58.8s (Cachipay bingo):** cortar **20-35s** — ganador muestra cartón de bingo + billetes posando con personal (clímax).
- **Video 14.3s:** completo (cumple rango; clímax del grito ~12s).
- Otros: completo, solo upscale a 1080x1920.

## Flujo de publicación IG Stories (script Python verificado)
1. Preprocesar a 1080x1920 → fotos: PIL cover-crop; videos: ffmpeg `scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920`.
2. Verificar con vision_analyze (enfoque/cortes/legibilidad) — para videos usar contact sheet + frame clave.
3. Subir a `/opt/reels/assets/<slug>` vía scp; confirmar URL HTTP 200 con cache-buster `?v=<epoch>` (Cloudflare cachea 404).
4. IG Stories = 2 pasos: `INSTAGRAM_POST_IG_USER_MEDIA` (media_type STORIES + image_url/video_url) → container id; luego `INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH` (ig_user_id + creation_id) → media id.
5. Video grande (>20MB): subir con timeout ≥280s; re-ejecutar solo el video si toca el timeout del paso container.

## ⚠️ FB Stories NO tiene tool directa (pendiente)
El conector Composio NO expone FB Stories (solo feed: FACEBOOK_CREATE_PHOTO_POST). Para que IG Story llegue a FB: activar **crossposting IG→FB** en Business Manager (Meta → Business Settings → Instagram Accounts → vincular @goldengame_casinos → "Compartir historias en Facebook" ON). Hasta que se active, las historias van SOLO a IG. El usuario ya fue informado y decidirá cuándo activarlo.
