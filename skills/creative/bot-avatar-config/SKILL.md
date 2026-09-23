---
name: bot-avatar-config
description: "Use when: instalar avatares bots crew + refresco Desktop."
category: neuralcrew-ops
version: 1.0.0
---

# Bot avatar config (flota NeuralCrew)

Arquitectura verificada 2026-08-26 en el deploy `/opt/data`. Cada "bot" crew es un **perfil Hermes**, no un bot de Discord separado.

## Dónde vive el avatar de cada bot
- Perfiles: `/opt/data/profiles/<bot>/` con bots `bragi, brokkr, freyja, heimdall, hermodr, sindri, ullr, vili` (+ roshi, comms, vigia).
- **Avatar canónico** (el que pinta Hermes Desktop): `/opt/data/profiles/<bot>/assets/avatar.png` (512×512 PNG).
- **Tarjeta grande**: `/opt/data/profiles/<bot>/assets/avatar-<bot>.jpg` (1024×1024 JPEG q92).
- Bot Mode: la app desktop "hermes-bots" se detecta por `ui_meta.hermes-bots` en `profile.yaml`; lee/escribe avatares server-side vía JSON-RPC `profiles.get_asset` / `profiles.set_asset`.
- `has_avatar` (que reporta `profiles.list`) = existe `assets/avatar.{png,jpg,webp}`.

## Instalar / reemplazar un avatar
1. **Backup previo**: copia `avatar.png` y `avatar-<bot>.jpg` a un dir con fecha (ej. `deliverables/<proyecto>/backup-assets-YYYYMMDD/`).
2. Redimensionar desde el render fuente (1024×1024): `avatar.png` → 512×512 PNG `optimize=True`; `avatar-<bot>.jpg` → 1024×1024 JPEG `quality=92`.
3. Verificar dimensiones post-escritura (ver comando abajo).
4. QA visual con `vision_analyze` sobre el `avatar.png` instalado (identidad correcta del personaje).

## Verificar con Pillow (el python del sistema NO trae PIL)
```bash
cd /opt/data && UV_CACHE_DIR=/tmp/uvcache uv run --with pillow python3 - <<'EOF'
from PIL import Image
im = Image.open('/opt/data/profiles/<bot>/assets/avatar.png')
print(im.size)  # debe dar (512, 512) para avatar.png, (1024, 1024) para avatar-<bot>.jpg
EOF
```
`/opt/data/.cache/uv` no es escribible → siempre usar `UV_CACHE_DIR=/tmp/uvcache`.

## Por qué Hermes Desktop no muestra la imagen nueva
- El servidor **NO cachea**: `profiles.get_asset` lee el archivo del disco en cada llamada. No hay evento de refresco emitido por el servidor.
- La caché está en el **cliente** (roster en memoria): hay que recargar/reconectar la app para que vuelva a pedir `profiles.list` + `get_asset`.
- Si tras recargar persiste: preguntar al usuario DÓNDE exactamente no se ve (lista lateral / chat / ajustes del perfil) y si antes veía los avatares viejos; verificar de nuevo el sha256 del archivo en disco (puede haber otro proceso sobrescribiendo).

## Discord: un solo bot real
- En el guild NeuralCrew Labs solo hay UN bot miembro: **"Ragnar"** (id `1493385610797252758`). Los 8 crew NO son miembros separados de Discord; cambiar su avatar real = PATCH REST `/users/@me` con el token del bot.
- `DISCORD_BOT_TOKEN` vive en `/opt/data/profiles/{roshi,comms,vigia}/.env` (los `.env` de los perfiles crew están vacíos). Token también disponible vía `curl -H "Authorization: Bot $DISCORD_BOT_TOKEN" https://discord.com/api/v10/users/@me`.

## Relacionados
- `quality-check-visual` — QA de retratos generados (contar manos, objetos fusionados al cuerpo, verificar etiqueta↔imagen en contact sheets). Su sección "Prompts endurecidos" aplica antes de instalar.
- `inspecting-hermes-desktop-dom` — si el Desktop corre en la misma máquina (CDP en `127.0.0.1:9222`), se puede inspeccionar el DOM en vivo; en deploys remotos el Desktop no es visible desde el servidor.

## Referencias absorbidas

- `references/neuralcrew-bot-avatars.md` — absorbida desde `creative/neuralcrew-bot-avatars` el 2026-09-23 (F6 lote 4, R15: condensar sin borrar).
