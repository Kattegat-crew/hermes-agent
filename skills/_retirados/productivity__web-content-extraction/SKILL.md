---
name: web-content-extraction
description: "Usa cuando la página es SPA: busca alternate .md endpoint."
---

# Web Content Extraction — Páginas modernas (SPA / Inertia / Next.js)

## Trigger
- `web_extract` devuelve error de configuración ("Web tools are not configured") o timeout
- El browser tool navegador hace timeout (páginas pesadas, >1MB de HTML)
- La página es una SPA (Inertia/Next.js): HTML lleno de JSON embebido, `<div id="app">`, y el texto útil no aparece en el HTML directo

## Técnica principal: alternate markdown/plain-text endpoints (confirmado 08/2026)

Muchos sitios de documentación sirven una versión **markdown plana** de cada artículo aunque la app sea JS-heavy. Lo anuncia el `<head>`:

```html
<link rel="alternate" type="text/markdown" href="https://<host>/help/cli.md">
```

1. Fetch del HTML y buscar en `<head>`:
   `rel="alternate" type="text/markdown"` (o `.json` / `.txt`)
2. Fetch de la URL del href (`...md`) en vez del HTML completo.

Caso real Bitwarden Help: `/help/cli/` = 1.4MB de HTML (app Inertia, JSON embebido); `/help/cli.md` = ~40KB de markdown limpio y completo (incluye código, tablas, notas). Sin Inertia, sin banners, sin scripts.

## UA header obligatorio

Usar siempre UA de Chrome real — muchos sitios (Bitwarden, r.jina.ai da 403 con el default) vetam el UA de urllib por defecto:

```python
headers = {
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
  "Accept": "text/markdown,text/plain;q=0.9,text/html;q=0.8",
  "Accept-Language": "en-US,en;q=0.5",
}
```

## Script mínimo (urllib, sin curl)

```python
import urllib.request
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", "Accept": "text/markdown,text/plain;q=0.9"})
with urllib.request.urlopen(req, timeout=30) as r:
    data = r.read().decode("utf-8", errors="ignore")
```

Pitfalls:
- **curl NO está instalado** en este VPS — usar urllib.
- Si hay `decompress`/data zlib, urllib lo maneja solo (Content-Encoding gzip lo descomprime automáticamente).
- Páginas con 403 (r.jina.ai) — probar extraer el `.md` directo del sitio antes de pedir readers externos.

## Cadena de fallback completa
1. `web_extract` (Firecrawl) → 2. browser tool → 3. urllib directo (UA Chrome) con búsqueda de alternate markdown → 4. agent-reach/obscura si están instalados → 5. reportar al usuario.

## Referencias
- `references/bitwarden-cli-case.md` — caso completo Bitwarden Help: síntoma, extracción del .md, resultado.