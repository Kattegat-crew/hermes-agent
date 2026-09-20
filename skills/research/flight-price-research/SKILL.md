---
name: flight-price-research
description: Use when researching flight prices or VPN/geo fares.
---

# Flight Price Research (búsquedas de vuelos, comparación geo/VPN)

## Triggers
- "¿cuánto cuesta un vuelo de X a Y?", "busca vuelos baratos", "tarifa ida/vuelta", "qué aerolíneas cubren X→Y", "¿es más barato comprar con VPN desde EE.UU. / otro país?", "cotización de viaje para N personas".

## Flujo de trabajo

1. **Checar la IP/geo de salida primero** (responde la pregunta VPN casi siempre):
   ```bash
   curl -s --max-time 15 https://ipinfo.io/json
   ```
   El VPS de NeuralCrew sale desde **Contabo, Orangeburg NY (EE.UU.)** — tus búsquedas web ya se ven como EE.UU. Sin VPN para eso. Si el usuario pide "simular otro país", usa `gl=CO`/`gl=XX` + `curr=` en Google Flights (ver paso 3) o un proxy/VPN solo si es imprescindible.

2. **Investigación de rutas con web_search primero**: qué aerolíneas operan la ruta, si hay rutas estacionales (ej. Qantas MEL↔HNL), qué hubs se usan (BOG→MEL suele pasar por Boston/Abu Dhabi/IAH/SFO/Santiago/Sydney). Esto da el mapa mental para interpretar los precios del paso 3.

3. **Sacar precios en vivo con curl a Google Flights** (sin browser; los parámetros `q`, `hl`, `gl`, `curr` sí cambian el resultado):
   ```bash
   UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
   CK="CONSENT=YES+cb.20260601-13-p0.en+FX+111"
   curl -sL --max-time 60 "https://www.google.com/travel/flights?q=Flights%20from%20Bogota%20to%20Melbourne%20on%202026-10-27%20one-way&hl=en&gl=US&curr=USD" \
     -H "User-Agent: $UA" -H "Accept-Language: en-US,en;q=0.9" -H "Cookie: $CK" -o gf.html
   ```
   Parsing detallado (bloques `AF_initDataCallback`, mapeo tarjeta→itinerario, dedupe de precios): ver `references/google-flights-parsing.md`. Fallback si el browser-use/CDP de Brave está caído: este pipeline curl SIEMPRE es el plan B y suele ser suficiente.

4. **Comparación de locales (pregunta VPN/país):** lanza la MISMA ruta dos veces — `gl=US&curr=USD` y `hl=es&gl=CO&curr=COP` — y convierte con el TRM del día. **Regla aprendida:** Google Flights muestra la MISMA matriz de tarifas en cualquier locale; la diferencia es solo conversión de moneda (y eventual fee local). No afirmes que la VPN da descuento salvo que filtres tarifas que realmente difieran por mercado de emisión.

5. **Moneda (TRM) — usar 2 fuentes** (datos.gov.co a veces da 404; frankfurter.app a veces 301):
   ```bash
   curl -s https://open.er-api.com/v6/latest/USD | python3 -c "import sys,json;print(json.load(sys.stdin)['rates']['COP'])"
   curl -sL https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/usd.json | python3 -c "import sys,json;print(json.load(sys.stdin)['usd']['cop'])"
   ```

6. **Validar y entregar:**
   - El precio en Google Flights es índice de búsqueda; verificar siempre en la web de la aerolínea/OTA antes de recomendar comprar.
   - Multi-persona: precio por persona × N (y avisar si la tarifa es por pax).
   - Rutas "pasando por Y" con tiquetes separados (split-ticket): dar el total pero SIEMPRE avisar del riesgo (sin protección si el primer tramo se atrasa, equipaje no conectado, doble entrada).
   - Diferenciar opción mínima por precio vs mínima por tiempo (1 escala sule costar 2× pero ahorra horas) y dar reconendación con criterio.

## Pitfalls
- El HTML de Google Flights es gigante (1-2 MB) y el precio aparece repetido ~6× por tarjeta (embedded JS). Dedupe con `Counter`/`set`, no confíes en la primera ocurrencia.
- Números COP en la página CO salen como `4.216.320` (puntos como miles), USD como `$1,373`. No mezcles.
- La estructura exata de bloques JSON de Google camia con el tiempo; el parser es *best-effort* — si no dan resulado en un mes, inspecciona el HTML cruido para re-mapear.
- Si browser_exec da `BU_CDP_URL unreachable`, pasa directo a curl — no pierdas tiempo con reinstalacines.
- No prometas precios como oferta firme; di "al feha de hoy en el índice de Google Flights".

## Related
- `product-price-monitor` — para VIGILAR precios (alertas/recurrencia) en vez de búsqueda puntal.
- `web-fetch` / `blocked-page-recovery` — si Google bloquea el curl (WAF/ccaptcha).