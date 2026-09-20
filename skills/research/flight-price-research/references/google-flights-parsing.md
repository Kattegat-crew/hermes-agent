# Google Flights parsing sin browser (verificado 2026-08-23)

Receta validada para extraer tarifas de Google Flights con curl + python3 (sin Browser Use). Usada para BOG→MEL 1-way, BOG→HNL, HNL→MEL, HNL→SYD.

## 1. URL

Formato que funciona (los parámetros `q`, `hl`, `gl`, `curr` sí cambian la respuesta):

```
https://www.google.com/travel/flights?q=Flights%20from%20Bogota%20to%20Melbourne%20on%202026-10-27%20one-way&hl=en&gl=US&curr=USD
```

- `q`: texto libre "Flights from {City} to {City} on {YYYY-MM-DD} one-way" (funciona también "Vuelos de Bogota a Melbourne el 27 de octubre de 2026 ida" con `hl=es&gl=CO&curr=COP`).
- El Top 5 de tarjetas aparece en el HTML inyectado. No se necesita JS.
- Cabeceras útiles: UA Chrome reciente, `Accept-Language`, cookie `CONSENT=YES+cb.20260601-13-p0.en+FX+111` (evita consent wall).

## 2. Extraer los bloques de datos

El HTML (1-2 MB) contiene bloques JS con los datos:

```python
import re, json
html = open('gf.html', encoding='utf-8', errors='replace').read()
blocks = re.findall(r'AF_initDataCallback\((\{.*?\})\);\s*</script>', html, re.S)
# o bien sin `</script>` si no pega
blocks = blocks or re.findall(r'AF_initDataCallback\((\{.*?\})\)', html, re.S)
for i, b in enumerate(blocks):
    m = re.search(r"data:(\[.*\])(?:,\s*sideChannel|\))", b, re.S)
    if m:
        data = json.loads(m.group(1))
        if any(w in json.dumps(data) for w in ('Melbourne','Bogot')):
            open(f'gf_block_{i}.json','w').write(json.dumps(data))
```

El bloque relevante (el que contiene las tarjetas) suele ser el más grande con los nombres de ciudades.

## 3. Precios (rápido, sin estructura)

```bash
python3 -c "
import re
from collections import Counter
html = open('gf.html', encoding='utf-8', errors='replace').read()
print(Counter(re.findall(r'\$\s?[\d,]+', html)).most_common(15))
"
```

- Cada tarifa aparece ~6× (duplicada por card/extra). `Counter`/`set` da el catálogo único.
- En la versión `gl=CO&curr=COP` los precios NO llevan `$` único: salen como números con puntos `4.216.320`, `5.657.720`, etc. Regex `[\d]{1,3}(?:\.\d{3})+` filtrando longitud 6-11 dígitos.

## 4. Mapear tarjeta → itinerario (aeropuertos/demand)

Estructura observada (agosto 2026) dentro del bloque de datos principal:

- `data[2]` y `data[3]`: contenedores de opciones (económica). Cada opción `data[2][i]` es una lista con varias "legs".
- Cada leg cae bajo el subtree `[2]` de la opción, p.ej. para opción 0: `data[2][0][0][2][j]` describe el tramo j-ésimo:
  - `[j][4]` / `[j][5]` → nombres de aeropuertos (ej. "El Dorado International Airport", "Boston Logan International Airport")
  - `[j][11]` → duración del tramo en minutos
- Los nombres de aerolínea no están en el mismo listado limpio (JSON interno usa iniciales "A", "B", "S"...), pero el HTML crudo sí trae los nombres ("Avianca", "Etihad", "United"...). Combinar: nombre de aerolínea del HTML crudo + estructura de tramos del JSON.
- Mapeo verificado para BOG→MEL 1-way (27-oct-2026, gl=US):
  - $1,373 → Avianca+Etihad, BOG→Boston→Abu Dhabi→MEL (2 stops, trazos 385+735+800 min)
  - $2,265 → LATAM vía Santiago (1 stop, 333+860 min)
  - $1,843 + $1,951 + $2,545 + $2,635 + $3,651 → opciones 2-3 stops vía IAH/SFO, Toronto/Vancouver/Sydney, DFW/Sydney, ATL/LAX, MIA/DFW.

## 5. Comparación de locales (VPN / país)

Misma query con `gl=US&curr=USD` vs `hl=es&gl=CO&curr=COP`. Verificado 2026-08-23 para BOG→MEL: la tarifa más barata salió **$1,373 USD** (~$4.216.320 COP = US$1,385 a TRM 3.045) — mismo fare, solo convertido. Conclusión reusable: Google Flights NO aplica geo-pricing visible entre locales; no inventar "descuento VPN".

## 6. Moneda / TRM

Fuentes que funcionan cuando otras fallan:
```bash
curl -s https://open.er-api.com/v6/latest/USD | python3 -c "import sys,json;d=json.load(sys.stdin);print(d['rates']['COP'])"
curl -sL https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/usd.json | python3 -c "import sys,json;print(json.load(sys.stdin)['usd']['cop'])"
```
Fallidas en la iteración: `datos.gov.co` (404), `frankfurter.app` (301 a veces), `api.currency-api.appspot` (quedó deprecado).

## 7. Verificación del giro del caso real (referencia de precios)

Ejemplo salida (BOG→MEL, 2026-10-27, 1 way, 1 pax, gl=US):
- Más barato: US$1,373 (2 stops, Avianca+Etihad)
- 1 sola escala: US$2,265 (LATAM)
- BOG→HNL (25-oct): desde $577 (2 stops), $767-$806 (1 stop United/American)
- HNL→MEL (27-10): desde $718 (2 stops); 1 stop $841-875; Jetstar directo no salió en la fecha
- Combo split "via Hawaii": ~$1,295/pax → prácticamente igual al bucket único, sin protección. Recomendación: NO split-ticket salvo que quieras parar en Hawái.

## Nota de mantenimiento
El índice de Google Flights no es API pública y la estructura cambia. Este parseo es de julio-agosto 2026; antes de depender d target para otra fecha, re-validar en un par de queries que los counts/posiciones siguen cuadrando.