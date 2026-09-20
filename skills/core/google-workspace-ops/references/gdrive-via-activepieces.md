---
name: gdrive-via-activepieces
description: Use when accessing client Google Drive programmatically.
---

# Google Drive programmatic access via ActivePieces credentials

## Cuándo usar
Tareas de clase «leer/bajar/mapear archivos del Drive de un cliente desde un script»: inventariar carpetas de campaña, espejar assets Drive→servidor, subir entregables. No para OAuth interactivo nuevo.

## Fuente de credenciales (en orden de intento)
1. **Conexión ActivePieces materializada del usuario** (la vía viva): `/root/hermes-agent/data/secrets/<perfil>-drive.json` (ej. `jonathan-drive.json`) con `refresh_token`, `client_id`, `client_secret`, `scopes` (CSV). Ejemplos de uso: `/root/hermes-agent/data/scripts/descarga_drive_ap.py`, `upload_drive_ap.py`.
2. `google_token.json` del contenedor — puede estar REVOCADO (`invalid_grant: Token has been expired or revoked`); si falla, pasar a (1), no reintentar.

## Patrón de servicio (funciona)
```python
import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import google.auth.transport.requests
d = json.loads(Path(SECRET).read_text())
creds = Credentials(token=None, refresh_token=d["refresh_token"], client_id=d["client_id"],
    client_secret=d["client_secret"], token_uri="https://oauth2.googleapis.com/token",
    scopes=d["scopes"].split(","))
creds.refresh(google.auth.transport.requests.Request())   # access token SIEMPRE refrescar
svc = build("drive", "v3", credentials=creds, cache_discovery=False)
```

## Listar/recorrer carpetas
- Hijos de una carpeta: `q="'<fid>' in parents and trashed=false"`, paginar con `pageToken` (pageSize 100).
- Búsqueda por nombre: `q="name contains 'Campañas' and mimeType='application/vnd.google-apps.folder'"` — devuelve homónimos de todos los clientes; anclar por el fid del padre correcto (recorrer desde la carpeta raíz del cliente, no desde búsqueda global).
- Mapeo Drive NeuralCrew: raíz «Neural Crew Labs» = `1yjLxB4lEZe3n79QKK8vlnladPv4FtM7w` → `Clientes/{Golden,Lucky}/Marketing/Campañas/<campaña>/` con `00-contrato / 01-docs / 02-guiones / 03-piezas / 04-aprobadas`. Dentro de 03-piezas: `Reels/Reel N/{Final, Scenes|Escenas, Videos seedance, Voces eleven labs, Voces arregladas, Assets}`.

## Descarga masiva — reglas duras
- **googleapiclient NO es thread-safe**: `MediaIoBaseDownload` con ThreadPoolExecutor corrompió el heap (`corrupted double-linked list`, proceso muerto, temporales en 0 bytes). Descargas SIEMPRE secuenciales (workers=1).
- Idempotencia barata: comparar por TAMAÑO con un solo `ssh "find <dir> -type f -printf '%p %s\n'"` batch por rama — nunca un `md5sum`/`stat` ssh por archivo (60+ ssh = timeout).
- Saneado de nombres locales antes de scp: `re.sub(r"[^\w\s.-]","",name).strip().replace(" ","-")` (evita spaces/UTF-8 raros en URLs y shell quoting).
- Run largo en background: redirigir a log (`> /tmp/x.log 2>&1`), NO `cmd | tail` (retiene salida hasta el final y parece colgado); monitorear con `ls` del destino.

## Referencia: sync de assets de reel
`/root/hermes-agent/data/workspace/sync_drive_reels.py` espeja `03-piezas/Reels/<Reel N>/{Final,Scenes,Videos*,Voces*,Assets}` → `/opt/reels/<cliente>/campañas/<camp>/reels/<slug>/…` (clasificador por nombre de subcarpeta y de archivo; el portal canónico y su protocolo viven en skill `reel-portal-protocol`).

## Pitfalls
- El `md5Checksum` de Drive no siempre viene (multiparte/Apps Script): no depender de él para dedup, usar size.
- Walks anidados con subcarpetas duplicadas tipo «Escenas» vs «Escenas Reel 1» producen entradas repetidas → dedup por `file['id']`.
- Los fids cambian si el cliente recrea carpetas: re-descubrir por nombre bajo el padre conocido antes de reportar la carpeta como inexistente.
