# Meta Ads — Session 2026-09-07 (Golden + Paradise)

Diagnóstico inicial del funnel Meta Ads de NeuralCrew para los casinos. Conexiones re-vinculadas y campaña Bingo Millonario (Amor y Amistad) planificada.

## Conexiones verificadas (status ACTIVE)

| Cliente | word_id | Ad Account |
|---|---|---|
| Golden Game | `metaads_tactic-vison` | `act_1581421999562187` |
| Lucky/Paradise | `metaads_moly-ponent` | `act_1525564931963110` |

## Re-vincular conexiones EXPIRADAS

El toolkit metaads traía 4 sesiones EXPIRED (derek-wadder, saul-elude, etc.). Patrón:

```bash
composio link metaads --no-browser --no-wait   # → redirect_url + connected_account_id
# el usuario abre la URL y autoriza en Meta; el link expira si no se completa a tiempo
composio connections list | jq '.metaads[]'    # confirmar ACTIVE
```

El link de autorización queda `INITIATED` y si no se completa pasa a `EXPIRED`. Hay que re-generar el link y que el usuario complete el flujo completo en Meta.

## Diagnóstico de campañas (inversión jun→sep 2026)

**Golden** — total $291.303 COP · 78.374 impr. · 3.307 clicks
| Campaña | Inversión | Clicks | Impr. | Alcance | Objetivo |
|---|---|---|---|---|---|
| Golden Julio Mundial | $199.981 | 2.418 | 50.274 | 31.280 | LINK_CLICKS |
| Golden Junio Mundial | $91.322 | 889 | 28.100 | 15.252 | LINK_CLICKS |
| Golden Mayo | $23.022 | 28 | 12.949 | 9.998 | AWARENESS |

**Paradise** — total $799.478 COP · 114.940 impr. · 9.597 clicks
| Campaña | Inversión | Clicks | Impr. | Alcance | Objetivo |
|---|---|---|---|---|---|
| Julio Lucky Mundial | $399.969 | 4.686 | 48.914 | 28.261 | LINK_CLICKS |
| Junio Lucky Mundial | $399.509 | 4.911 | 66.026 | 53.078 | LINK_CLICKS |
| Mayo Lucky | $400.000 | 7.396 | 92.735 | 70.271 | LINK_CLICKS |

Patrón: campañas mensuales "Mundial" (LINK_CLICKS), ad sets **por sede**. Todas las de julio en PAUSED. Septiembre aún sin campaña.

## Auditoría de geolocalización (via METAADS_GET_OBJECT)

Sedes oficiales Golden (7): Agua de Dios, Anolaima, Cachipay, El Carmen de Apicalá, Pacho, San Francisco, Tunja.

| Ad set | ¿Geo OK? |
|---|---|
| Golden General Julio | ❌ SIN municipio (solo interés) |
| Cachipay | ✅ Cachipay |
| San Francisco | ✅ San Francisco |
| Tunja | ✅ Tunja |
| Pacho | ✅ Pacho |
| El Carmen | ❌ SIN municipio |
| Anolaima | ❌ SIN municipio |
| **Agua de Dios** | ⚠️ NO existe ad set |

Paradise (Chiquinquirá 1&2, La Calera Centro + Calera Gardens, Tunja):
| Ad set | ¿Geo OK? |
|---|---|
| Julio-General | ✅ Chiquinquirá + Funza + Tunja |
| Julio-La Calera (+ La Calera 2) | ❌ SIN municipio |
| Julio-Funza | ❌ SIN municipio |

**Hallazgo:** varios ad sets "por sede" NO están geo-localizados — segmentan por interés (tragamonedas, casino, póker), el anuncio se muestra a cualquier parte. Y le falta ad set a Agua de Dios.

## Campaña planificada "Golden Septiembre. Amor y Amistad" (LINK_CLICKS)

- Presupuesto $400K COP/mes. 7 ad sets: 1 general (30%) + 6 por sede (El Carmen, Cachipay, Anolaima, San Francisco, Tunja, Pacho — Agua de Dios fuera este mes).
- Geo recomendado: ad set general con ubicaciones de sedes (radio 5-8 km por municipio); ad sets por sede radio ~5 km.
- Todo en pausado hasta OK del Admin.

## Pixel (diseño, NO ejecutado)

Plan completo en /opt/data/plans/PLAN-PIXEL-GOLDEN-META.md. Repo web: `/opt/data/ggl-repo` (SPA Vite/React, React Router, index.html con el <head>). Dominio servido real `goldengame.com.co`; pero el `index.html` aún apunta a `goldengameweb.netlify.app` en canonical/OG — corregir.

Webs verificadas sin pixel (fbq/fbevents = 0): goldengame.com.co, paradiseclubcasinos.com.co, reels.neuralcrewlabs.com (+ /v2, /goldie/bingo).

Repo tiene `RouteWatcher` en App.jsx (detecta location.pathname por navegación) → ideal para disparar PageView/ViewContent. Formulario `/bono` en Bono.jsx hace POST a `/webhook/golden-vip-signup` y setSubmitted(true) en éxito → ahí disparar Lead.
</persisted_file_content>