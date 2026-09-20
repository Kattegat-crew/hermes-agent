# Publicar stories de evento del cliente (IG + FB) — verificado 07/09/2026

Cuando el cliente manda footage/fotos de un evento (casino, bingo) para publicar como historias,
el flujo es: normalizar a 9:16 → (videos) cortar al mejor tramo de 15-20s → publicar en IG (2 pasos)
→ FB (crossposting desde IG; NO hay tool FB directa de stories).

## Preferencia confirmada del Admin (Jonathan)
- **Siempre AMBAS cuentas** (IG + FB) al publicar stories del cliente.
- **"Tal cual"** — SIN cartela/logo/overlay ni edición de marca. Solo normalizar tamaño y, para videos, recortar.
- **Videos → cortar a 15-20s** (nunca el clip crudo de 30-60s). **Fotos → publicar tal cual** (IG decide la duración; no se configura segundos en foto).
- **Una pieza por story** (crear container + publicar por cada una), no un post combinado.

## Normalizar video a 1080x1920 (cover-fit — sirve para apaisado Y vertical, low-res)
```bash
ffmpeg -y -i IN.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1" \
  -c:v libx264 -preset medium -crf 24 -pix_fmt yuv420p -c:a aac -b:a 128k OUT.mp4
```
- `force_original_aspect_ratio=increase` + `crop=1080:1920` = **cover-fit centrado**. Maneja 478x850, 720x960, 368x496, 1024x576, 867x1156.
- Clips largos (>25s): el upscale tarda → usar `timeout` alto en la consola (200-300s), no el default.

## Foto a 9:16 (cover-fit centrado, PIL)
```python
from PIL import Image
img=Image.open('IN.jpg').convert('RGB')
W,H=1080,1920; iw,ih=img.size
s=max(W/iw,H/ih); nw,nh=int(iw*s),int(ih*s)
img=img.resize((nw,nh),Image.LANCZOS)
img.crop(((nw-W)//2,(nh-H)//2,(nw-W)//2+W,(nh-H)//2+H)).save('OUT.jpg',quality=92)
```

## Elegir el mejor slice 15-20s de un clip largo (NO cortar a ciegas)
```bash
ffmpeg -y -i IN.mp4 -vf "fps=1/5,scale=220:-1,tile=3x4" -frames:v 1 /tmp/contact.png
# fps=1/4 → 14 frames; fps=1/5 → 12 frames; ajusta el tile al grid
```
1. vision_analyze sobre la hoja de contacto, preguntando: ¿en qué tramo está la acción/emoción cumbre
   (ganador celebrando, grito de bingo, gente levantada)? Dame el rango de segundos.
2. Cortar ese rango:
```bash
ffmpeg -y -i IN.mp4 -ss START -t LEN -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1" \
  -c:v libx264 -preset medium -crf 24 -pix_fmt yuv420p -c:a aac -b:a 128k OUT.mp4
```
Verificado: un clip de 58.8s → corte 20-35s (ganador con cartón+billetes) → story de 15s limpia.
Clips que ya duran 15-19s: NO recortar, solo normalizar (la celebración suele estar al final).

## Verificar antes de publicar
- Frame del producto: `ffmpeg -y -ss N -i OUT.mp4 -frames:v 1 /tmp/chk.png` + vision_analyze (encuadre, nada cortado, momento correcto).
- `ffprobe -v error -select_streams v:0 -show_entries stream=width,height,duration -of csv=p=0 OUT.mp4`.

## Hosting — URL pública que Meta pueda descargar
```bash
scp OUT root@100.73.30.29:/opt/reels/assets/<slug>
curl -s -o /dev/null -w '%{http_code}' 'https://reels.neuralcrewlabs.com/assets/<slug>?v=<epoch>'  # 200
```
Siempre cache-bust con `?v=` por la caché de Cloudflare; `goldengame.com.co` 404a `/assets/` (no usar).

## Publicar en IG (2 pasos) — account `instagram_demal-molala`, ig_user 40006158832316994
```python
# Paso 1: container STORIES (foto: image_url; video: video_url)
INSTAGRAM_POST_IG_USER_MEDIA {ig_user_id:'...',media_type:'STORIES',image_url|video_url:URL}
#   → data.id = creation_id
# Paso 2: publicar
INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH {ig_user_id:'...',creation_id} → published media id
```
Conexiones usadas: ig=instagram_demal-molala (ACTIVE), fb=facebook_uncite-skyish (ACTIVE).
FB Page Golden Game Casinos = `820898971112738`; Paradise = `765896786617957`. Verificar siempre con
`FACEBOOK_LIST_MANAGED_PAGES` (la cuenta maneja varias páginas).

### ⚠️ Video container tarda ~30s+ — subir timeout
`INSTAGRAM_POST_IG_USER_MEDIA` con video STORIES puede tardar 19-31s en FINISHED (status checks).
Publicar 3-4 piezas en una sola llamada de consola puede clavar el default 60s. Pasar `timeout` alto
(280s+) y/o publicar una por una para que un video lento no tumbe el lote. El mensaje
`Container reached FINISHED status after Ns` es ÉXITO normal, no un cuelgue.

## ⚠️ FB Stories: NO hay tool directa en el conector
Las tools `FACEBOOK_*` son solo de *feed* (`FACEBOOK_CREATE_PHOTO_POST`, etc.), NO de stories.
Para que una story llegue a Facebook: activar **crossposting IG→FB** en Meta Business Manager
(Business Settings → Instagram Accounts → vincular el IG → activar "Compartir historias en Facebook").
Es una configuración de UNA VEZ; después cada IG Story se comparte sola. Hasta que el Admin la active,
solo IG recibe la story — no afirmar entrega en FB hasta confirmar el crosspost.

## Piezas publicadas 07/09/26 (IG @goldengame_casinos) — referencia de formato
- 01 Sándwiches foto · 02 Ambiente casino foto · 03 Ganador Luis Cañón foto ·
- 04 Bingo grito video 14.3s · 05 Casino Cachipay video 20s ·
- 06 Bingo Cachipay animadora video 18.98s · 07 Bingo Cachipay ganadores video 15s · 08 Bingo foto.
Video 05 (53.9s→20s) y 07 (58.8s→15s) fueron recortados por contact-sheet; el resto tal cual.
</content>
</invoke>
</parameters>
</invoke>
</skill_manage>
</invoke>
</parameters>
</invoke>
</invoke>
</invoke>

tool
</function_results></invoke>

</function_results>
</result>
</function_results>