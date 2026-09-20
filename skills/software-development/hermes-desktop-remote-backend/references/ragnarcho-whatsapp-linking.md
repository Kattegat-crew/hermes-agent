# Bot profile routing from Desktop — session deep-dive (20/08/2026)

Caso end-to-end: crear perfil "ragnarcho" desde Hermes Desktop (v0.20.4) contra
`hermes serve` remoto (VPS v0.20.4, puerto 9112) y enrutar WhatsApp de un
miembro del equipo a ese perfil con `gateway.profile_routes`.

## Cadena de fallos reales y sus causas (en orden)

### 1. `unknown method: profiles.create`
- Causa: Desktop más nuevo que el serve (serve seguía en v0.20.0 en memoria).
- Lección: `hermes --version` del binario puede decir v0.20.4 mientras el
  proceso en ejecución sirve v0.20.0. Verificar SIEMPRE con
  `GET /api/status` del serve (no requiere auth) y reiniciar el servicio
  `hermes-serve` para que el proceso tome la versión nueva (~10-45s para
  que el build cargue; el puerto tarda en reaparecer, no alarmarse).

### 2. `Unknown provider 'custom:nan-builders'` (y luego `'nan-builders'` en minúsculas)
- El config principal tenía `model.provider: custom:nan-builders` — alias
  legacy que v0.20.4 ya no resuelve (el flujo baja el nombre con
  `strip().lower().replace(' ','-')` y lo compara contra el registro de
  proveedores/plugins, no contra `custom_providers` por alias).
- Fix 1 (config principal): `sed -i 's/custom:nan-builders/NaN-Builders/'`
  — el nombre debe coincidir con la clave del bloque `providers:`.
- Fix 2 (perfil): los perfiles creados por Desktop solo escriben
  `model.provider` + `model.default`; NO copian `providers:` /
  `custom_providers:` / `model.base_url` / `model.api_key`. Sin eso el
  runner no encuentra credenciales → "Unknown provider '<nombre>'".
  Reconstrucción: copiar esos bloques del config principal al
  `profiles/<name>/config.yaml`, restart serve, probar.

## Después de activar profile_routes — el error genérico

Síntoma: el bot responde en WhatsApp "Sorry, I encountered an unexpected error"
(genérico del gateway).

Causa 1 — **permisos del perfil** (la más común): el serve host crea el
perfil como root (`drwx------ root`), pero el gateway del contenedor corre
como uid `hermes` (10000) y no puede abrir `config.yaml`/`state.db` del
perfil. Fix:
```bash
docker exec hermes-agent chown -R 10000:10000 /opt/data/profiles/<name>
docker exec hermes-agent chmod -R u+rwX /opt/data/profiles/<name>
```
Verificar estado con `ls -la /opt/data/profiles/<name>/` dentro del contenedor.

Causa 2 — si `profile_routes` no enruta: recordar `gateway.multiplex_profiles:
true` es REQUERIDO (el routing está gated en esa flag — gateway/run.py).

## Bind mount del contenedor — no confundir vistas

`docker inspect hermes-agent` → Mounts muestra:
`/root/hermes-agent/data -> /opt/data (bind)`.
Dentro del contenedor `/opt/data` ES el home real (8.8G, 160MB state.db).
Si un `ls` desde "host" y "contenedor" difieren en tamaño, es un false alarm
de namespace — los hechos de verdad son `docker exec` / `docker inspect`.

## Chat_id de WhatsApp = LID, no el número

- `WHATSAPP_ALLOWED_USERS` tiene números planos (573166910728).
- El bridge usa ids internos **LID**: `153580212334603@lid` (DM de Jesús
  Díaz), `120363429706344032@g.us` (grupo oficial), `43001262956766@lid`
  (Jonathan).
- Para enrutar: consultar el `chat_id` REAL en `state.db`:
  ```sql
  SELECT DISTINCT chat_id, chat_type, display_name FROM sessions WHERE source='whatsapp';
  ```
  Nunca derivar el chat_id de un número de teléfono de la allowlist.

## Desktop colgado en "Connecting" (cache corrupta)

- Tras varios reinicios del serve, el Desktop queda "Connecting…" para
  siempre; Retry no ayuda; Tailscale del PC muestra tx alto sin TCP
  ESTABLISHED en 9112.
- Fix Windows: cerrar la app del todo (bandeja → Quit / Task Manager), en
  `%APPDATA%\Hermes` renombrar `Cache`, `Session Storage`, `Preferences`
  a `.bak` (NO tocar `Local Storage` — guarda la config de gateway/sesión).
  Reabrir y re-insertar URL + credenciales.