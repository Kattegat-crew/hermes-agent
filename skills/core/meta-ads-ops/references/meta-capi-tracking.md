---
name: meta-capi-tracking
description: "Diagnose Meta Events datasets and enrich CAPI lead events."
version: 1.1.0
author: Ragnar
metadata:
  hermes:
    category: marketing
    tags: [meta, capi, pixel, events-manager, emq, leads]
---

# Meta CAPI Tracking Skill

Diagnóstica píxeles y datasets de Meta en Events Manager, enriquece los eventos Lead que envía la Conversions API y asegura la deduplicación pixel↔CAPI en pipelines de leads (webhooks, chat widgets, formularios). No cubre creación de campañas ni publicación de contenido (ver meta-ads-ops, que vive en skills.external_dirs y por tanto no es editable aquí).

## When to Use
- El Admin reporta "el dataset/pixel aparece vacío" o el checklist de Events Manager pide campos (IP, teléfono, apellido) sobre un píxel que creíamos cubierto.
- Antes de escalar pauta sobre una cuenta cuyo tracking de leads no ha sido auditado (EMQ bajo, leads no atribuidos).
- Al construir o modificar un webhook de leads que emite eventos a CAPI (user_data, event_id, dedup).

## Prerequisites
- Credencial CAPI del cliente (tokens por contenedor webhook en PROD; nunca reproducirlos en chat ni reportes).
- Acceso SSH al host con los contenedores webhook-gateway (PROD 169.58.189.222).
- Tool de Composio `metaads_get_pixels_and_datasets_for_ad_account` para enumerar fuentes.

## How to Run
1. Enumerar las fuentes de eventos de la cuenta (datasets + píxeles) con el tool de Composio; clasificar por tipo (web vs app) y `last_fired_time`.
2. Verificar qué píxel init real tiene cada sitio (curl + grep sobre el HTML vivo, nunca desde memoria). OJO: el eventID/dedup del frontend NO está en el HTML — vive en los bundles JS compilados servidos en prod; grep los assets servidos, no el HTML (un grep de HTML hizo concluir mal que faltaba el dedup).
3. Trazar el payload CAPI en el contenedor que emite los eventos (grep del código vivo en el host).
4. Comparar el `user_data` real contra la tabla EMQ y cerrar los campos gratuitos server-side (ver references/events-manager-datasets.md).
5. Auditar dedup pixel↔CAPI (eventID en el frontend) según references/webhook-lead-capi-integration.md.
6. Los arreglos de Events Manager (archivar datasets huérfanos, fijar fuente de reporte) son MANUALES en EM o vía navegador con aprobación explícita del Admin.

## Quick Reference
- Dataset app vacío ≠ pipeline rota: casi siempre es contaminación de vista (dataset huérfano tipo `app1` creado por el wizard de fuentes).
- Casi todo lo que el checklist pide se cierra gratis server-side: `ln` (split del nombre), `ct`/`st`/`country`/`zp` (mapeo por sede), IP/UA (headers), `fbp`/`fbc` (cookies).
- `db` (fecha de nacimiento) y `ge` (sexo) solo por decisión de negocio; db además respalda la verificación +18.

## Pitfalls
- Events Manager abre el dataset "más reciente" como fuente de reporte de la cuenta: un dataset app vacío hace que TODO parezca muerto. Diagnosticar contra la lista completa de fuentes, no contra la vista por defecto.
- Graph directo `GET /act_<id>/event_sources` con token CAPI falla (2500 "Unknown path components" o #200): usar el tool de Composio; enumerar apps del Business exige `ads_management`, que el token de webhook suele no tener.
- No prometer arreglos de Events Manager desde el agente: archivar/eliminar datasets es acción manual con aprobación.
- Nunca imprimir tokens al comparar payloads; leer el código en el host y redactar credenciales.
- La normalización pre-hash es el hallazgo #1 de todo reviewer: fn/ln sin espacios internos (strip + lowercase), country ISO-3166-1 alpha-2, zp solo dígitos; hashear cada campo ya normalizado y OMITIR el campo si no hay dato (nunca hash de cadena vacía).
- Tabla geo por sede: CPs municipales reales verificados, nunca inventados; sede desconocida ⇒ omitir ct/st/zp en vez de enviar aproximaciones.

## Verification
- Lead de prueba real → pestaña Test Events del píxel correcto: IP/UA presentes + parámetros nuevos + eventID coincidente entre pixel y CAPI. El OK del tool de envío NO prueba el matching.
- El EMQ se lee en Events Manager tras acumular eventos; citar el delta solo con lectura en vivo, no con estimaciones de Meta.

## References
- `references/events-manager-datasets.md` — diagnóstico del dataset vacío, tabla user_data/EMQ y comandos de enumeración.
- `references/webhook-lead-capi-integration.md` — contrato del gateway de leads, dedup pixel↔CAPI y verificación E2E.
- `references/emq-enrichment-execution.md` — ejecución F1 del 22-sep: normalización pre-hash exacta, tabla geo por sede con CPs, patrón parcheo+deploy+E2E en host y loop reviewer deepseek.


---

## Procedencia

Absorbido por F3 el 20260923-055337 desde la autoskill `data/skills/marketing/meta-capi-tracking` (sin versión en git hasta hoy).
El procedimiento se conserva íntegro; el paraguas `meta-ads-ops` es su punto de entrada.

