---
name: google-drive-sheets-ops
description: "Use when creating Google Sheets or accessing Drive via API."
version: 1.0.0
author: hermes
license: MIT
metadata:
  hermes:
    tags: [google, drive, sheets, api, oauth, refresh-token, csv, export, trash]
triggers:
  - crear/editar una hoja de cálculo de Google a partir de datos o recibos
  - listar archivos de una carpeta concreta de Google Drive
  - descargar/exportar PDF, DOCX, XLSX, CSV de Drive
  - enviar a papelera (trash) un archivo de Drive
  - el login de Google da invalid_grant / token revocado
---

# Google Drive & Sheets — operaciones por API (perfil default)

Complementa a `google-drive-access` (user-owned, no editable desde curator): esta skill suma
los MECANISMOS de API verificados (listar por carpeta, exportar nativos, crear hoja nativa sin
Sheets API, trash) y la credencial que SI funciona para el perfil default.

## Credencial canónica del perfil default

`/opt/data/google_token.json` puede dar `invalid_grant` (revocado/expirado). Lo que SÍ funciona
son los secrets que usa el MCP `ncl_google` (config.yaml `mcp_servers.ncl_google`):

- Mapa: `/opt/data/connections-map.json` → entrada `owner==default` y `status==active`
  (p.ej. `jonathan-drive` → service `drive`, cuenta jonathaun124@gmail.com).
- Secret: `/opt/data/secrets/<conn>.json` con `client_id`, `client_secret`, `refresh_token`, `scopes`.
- Scope de `jonathan-drive` = `https://www.googleapis.com/auth/drive` (alcanza listar,
  descargar, exportar, crear y convertir a hoja).

> Intercambiar refresh_token → access_token fresco (patrón que SÍ funciona; el token crudo
del `.json` viejo da 401):

```python
import json, urllib.parse, urllib.request
cred = json.load(open('/opt/data/secrets/jonathan-drive.json'))
body = urllib.parse.urlencode({'client_id': cred['client_id'],
    'client_secret': cred['client_secret'], 'refresh_token': cred['refresh_token'],
    'grant_type': 'refresh_token'}).encode()
AT = json.loads(urllib.request.urlopen(urllib.request.Request(
    'https://oauth2.googleapis.com/token', body), timeout=30).read())['access_token']

def api(url, method='GET', data=None):
    req = urllib.request.Request(url, headers={'Authorization': 'Bearer '+AT}, method=method)
    if data is not None:
        req.add_header('Content-Type', 'application/json'); req.data = json.dumps(data).encode()
    return json.loads(urllib.request.urlopen(req, timeout=60).read())
```

## Listar contenido de UNA carpeta (por ID)

El MCP `drive_search` solo busca por nombre a nivel global. Para limitar a una carpeta usar
la query `'<parent>' in parents`:

```python
q = f"'{FOLDER_ID}' in parents and trashed=false"
url = f'https://www.googleapis.com/drive/v3/files?q={urllib.parse.quote(q)}&pageSize=100&fields=files(id,name,mimeType,modifiedTime)'
# api(url) -> files[]
```

## Exportar un nativo (docs/sheets) — usar `/export`, NO `alt=media`

`files/{id}?alt=media&exportMimeType=...` da 403 `fileNotDownloadable` (solo binarios).
Endpoint correcto:

```python
url = f'https://www.googleapis.com/drive/v3/files/{FILE_ID}/export?mimeType=text/csv'  # o text/plain, xlsx
# GET con Bearer AT -> contenido. Verificar SIEMPRE leyéndolo antes de declarar éxito.
```

## Crear hoja nativa de Google Sheets SIN Sheets API habilitada

Si `spreadsheets.values.update` devuelve 403 `SERVICE_DISABLED` (Sheets API off en el proyecto
OAuth), NO se puede habilitar con un token scope `drive` (da `ACCESS_TOKEN_SCOPE_INSUFFICIENT`).
Solución: subir el contenido como CSV con mimeType objetivo spreadsheet (import automático),
solo con Drive API + scope drive:

```python
import io, csv
meta = json.dumps({'name': title, 'parents': [FOLDER_ID],
                   'mimeType': 'application/vnd.google-apps.spreadsheet'}).encode()
csv_bytes = csv_bytes  # contenido: csv.writer sobre [headers] + rows, encode('utf-8')
boundary = 'xNCBoundary'
mp = io.BytesIO()
mp.write(b'--'+boundary.encode()+b'\r\n')
mp.write(b'Content-Type: application/json; charset=UTF-8\r\n\r\n'); mp.write(meta+b'\r\n')
mp.write(b'--'+boundary.encode()+b'\r\n')
mp.write(b'Content-Type: text/csv\r\n\r\n'); mp.write(csv_bytes+b'\r\n')
mp.write(b'--'+boundary.encode()+b'--\r\n')
url = 'https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&fields=id,name,mimeType,webViewLink'
req = urllib.request.Request(url, data=mp.getvalue(), method='POST')
req.add_header('Authorization', 'Bearer '+AT)
req.add_header('Content-Type', 'multipart/related; boundary='+boundary)
res = json.loads(urllib.request.urlopen(req, timeout=90).read())
# res['mimeType'] == 'application/vnd.google-apps.spreadsheet' => hoja nativa OK
```

Consecuencia: la hoja queda SIN formato (negrita en encabezado no aplica por API mientras
Sheets API esté off); el contenido queda correcto y es editable en Drive. Para formato hay
que habilitar la Sheets API en la consola.

## Trash (papelera) — mandar body JSON, NO query param

`PATCH files/{id}?trashed=true` devuelve 200 pero NO trona. Usar el body:

```python
api(f'https://www.googleapis.com/drive/v3/files/{FID}', 'PATCH', {'trashed': True})
# verificar: api(f'.../files/{FID}?fields=name,trashed')['trashed'] is True
```

## Fuente autoritativa de pagos de ads (Meta)

El reporte de facturación (`..._n.csv`, encabezado `Meta ads payment`) trae la fila exacta
`Date,Transaction ID,Campaign Name,Campaign ID,Campaign Amount,Payment Method,Payment Status,
Transaction Subtotal,Transaction Tax,Transaction Total,Currency`. Los PDFs "recibo" de la
misma carpeta pueden ser imágenes sin capa de texto (pdftotext no extrae nada) → usar el CSV
como fuente. Traducir: `Paid`->`Pagado`, `Advertising credit`->`Crédito publicitario`; montos
como número + columna Moneda=COP.

## Pitfalls
- No confiar en `google_token.json` si da `invalid_grant`; usar el secret con refresh_token.
- Para verificar un write, exportar/leer de vuelta el archivo ANTES de reportar éxito
  (verificación de estado externo).
- No crear carpetas en Drive sin autorización (ver `mapa-de-carpetas`).
- `files/{id}?alt=media` es solo para binarios; nativos van por `/export`.
