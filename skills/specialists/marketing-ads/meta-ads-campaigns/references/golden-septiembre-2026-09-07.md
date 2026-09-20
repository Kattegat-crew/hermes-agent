# Golden Septiembre — campaña + ad sets (07/09/2026)

## Resultado
Campaña `Golden Septiembre. Amor y Amistad` (id `120251536257860347`, OUTCOME_TRAFFIC, PAUSED) + 7 ad sets PAUSED. Geo verificada con GET_OBJECT.

> ⚠️ La sesión terminó con 2 asuntos pendientes conocidos (no bloqueantes al estar PAUSED):
> (1) Los ad sets de sede quedaron con daily_budget de $4.665/día (error de centavos) cuando debían ~$1.555/día. Hay que corregir en la UI al activar.
> (2) El radio quedó en 16km (mínimo de Meta) en lugar de los 5-8km pedidos — Meta no permite radio menor por API.

## Ad sets creados
| Ad set | ID | Geo (real) | daily_budget | Estado |
|---|---|---|---|---|
| Golden General Septiembre | 120251536273800347 | 6 municipios (Tunja, Pacho, Cachipay, Anolaima, El Carmen, San Francisco) | 400000 ($4.000) | PAUSED |
| Golden Tunja Septiembre | 120251536275530347 | Tunja | 466500 ⚠️ | PAUSED |
| Golden El Carmen Septiembre | 120251536276100347 | Carmen de Apicalá | 466500 ⚠️ | PAUSED |
| Golden San Francisco Septiembre | 120251536277530347 | San Francisco de Sales | 466500 ⚠️ | PAUSED |
| Golden Cachipay Septiembre | 120251536278370347 | Cachipay | 466500 ⚠️ | PAUSED |
| Golden Anolaima Septiembre | 120251536279510347 | Anolaima | 466500 ⚠️ | PAUSED |
| Golden Pacho Septiembre | 120251536280950347 | Pacho | 466500 ⚠️ | PAUSED |

## Geo keys de sedes Golden (ids numéricos de Meta)
- Tunja: 480932
- Pacho: 475293
- Cachipay: 2712446 (usar el city principal; hay otro 458580)
- Anolaima: 457023
- Carmen de Apicalá: 459356
- San Francisco de Sales: 478567

## Parámetros del plan confirmados por Jonathan
- Campaña ÚNICA `Golden Septiembre. Amor y Amistad`.
- 2 conceptos de ad set: **General** (1) + **por sede** (6). Agua de Dios NO entra (decisión de Jonathan).
- Presupuesto total **$400K COP/mes** → 30% general ($4.000/día) / 70% sedes (~$1.555/día c/u).
- General con los 6 municipios de sedes, 8km (resultó 16km por mínimo de Meta).
- Tunja 15km (confirmado), resto 8km (resultó 16km).
- Objetivo LINK_CLICKS (tráfico). "People living in". Edad 18-55/65. Español.
- No reutilizar públicos guardados viejos (General/El Carmen/Anolaima de julio tenían geo vacía — solo interés).

## Públicos guardados detectados (todos "Listo")
Publico Agua de Dios · Publico El Carmen · Publico San Francisco · Publico Pacho · Publico anolaima · Publico Cachipay · Publico Golden General · Publico Tunja. Algunos con geo vacía (por eso se crearon ad sets con targeting directo y no se reutilizaron).

## Siguiente paso
Crear los anuncios (creativos) ad set por ad set — el usuario pidió "anuncio por anuncio". El pixel + CAPI ya están activos para atribución.
