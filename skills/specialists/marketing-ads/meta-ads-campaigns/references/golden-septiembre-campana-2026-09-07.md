# Campaña Golden Septiembre. Amor y Amistad (07/09/2026)

## Estado
- **Campaña:** `Golden Septiembre. Amor y Amistad` (id `120251536257860347`) — OUTCOME_TRAFFIC, PAUSED.
- **Ad Account:** act_1581421999562187 (Golden Game).
- **7 ad sets** creados, TODOS PAUSED. Sin ads aún (creativos pendientes, anuncio por anuncio).

| Ad set | id | Geo (verificada) | daily_budget |
|---|---|---|---|
| Golden General Septiembre | 120251536273800347 | 6 municipios (Tunja, Pacho, Cachipay, Anolaima, Carmen de Apicalá, San Francisco) | 4000 (=$4.000) |
| Golden Tunja Septiembre | 120251536275530347 | Tunja | 466500 (⚠️ arreglar) |
| Golden El Carmen Septiembre | 120251536276100347 | Carmen de Apicalá | 466500 (⚠️) |
| Golden San Francisco Septiembre | 120251536277530347 | San Francisco | 466500 (⚠️) |
| Golden Cachipay Septiembre | 120251536278370347 | Cachipay | 466500 (⚠️) |
| Golden Anolaima Septiembre | 120251536279510347 | Anolaima | 466500 (⚠️) |
| Golden Pacho Septiembre | 120251536280950347 | Pacho | 466500 (⚠️) |

## Plan de presupuesto (Admin)
- Total: **$400K COP/mes**.
- General (30%): ~$4.000/día.
- Sedes (70%): ~$1.555/día c/u. **⚠️ Quedaron en 466500 centavos = $4.665/día (3x).** Corregir antes de activar (recrear ad set o UI).
- **Agua de Dios EXCLUIDA** de anuncios.

## Geo keys usados
- Tunja: 480932 · Pacho: 475293 · Cachipay: 2712446 · Anolaima: 457023 · Carmen de Apicalá: 459356 · San Francisco de Sales: 478567.

## Radio
Se usó `location_radius: 10` (millas, ~16km) porque es el mínimo que permite la API de Meta para cities (5/8/10 km rechazados con subcode 1487110).

## Pendientes
1. Ajustar presupuestos de sedes a ~$1.555/día.
2. Crear el AD (creativo) — anuncio por anuncio, gate del Admin.
3. Revisar/activar tras aprobación humana.

## Lecciones de esta iteración
- `daily_budget` en centavos (4000 = $4.000; 4665 → $466.500, 3x).
- `billing_event: IMPRESSIONS` (NO LINK_CLICKS) + `targeting_automation.advantage_audience: 0` + `age_max: 65`.
- Radio mín 10mi; geo keys numéricos; verificar con GET_OBJECT.
- Sin UPDATE/DELETE ad set por API.
