# F6 · Lote 1 — paraguas de clase: automatización de APIs de terceros vía Rube MCP

| Campo | Valor |
|---|---|
| Documento | `docs/skills/F6-LOTE1-EJECUCION.md` |
| Fecha | 2026-09-23 |
| Comando | `python3 scripts/f6_lote1_ejecutar.py --firma <TOKEN>` |
| Motor | `scripts/f6_lote1_ejecutar.py` (candado en código, autónomo) |
| Familia | grupo_02 de la métrica oficial: 5 skills de UNA sola plantilla |
| Paraguas | `productivity/rube-mcp-api-automation` |

## Por qué esta familia

Los cinco son instancias del mismo texto (`# <Vendor> Automation via Rube MCP`,
mismo esqueleto de 91 líneas, cuatro de ellos casi calcados: 2.875–2.920 B).
Ninguno tenía `scripts/`, referencias entrantes ni uso desde crons. Es el caso
literal de «empaquetado de familias de una sola técnica» del plan Rev. 6.

## Anatomía del paraguas (política §4)

- `SKILL.md` = **clase** + criterio de decisión + checklist + patrón de trabajo común
- `references/<proveedor>.md` = procedimiento **íntegro** de cada caso absorbido
- Descripción con la clase de disparo en los primeros 57 caracteres (R5):
  `Automate a third-party API via Rube MCP (Composio).`

## Resultado

| Caso absorbido | Toolkit | Referencia | Hash antes |
|---|---|---|---|
| `productivity/slackbot-automation` | `slackbot` | `references/slackbot.md` | `e5169d33e85ccba2` |
| `productivity/zoho-automation` | `zoho` | `references/zoho.md` | `58c7c618c51261aa` |
| `software-development/onesignal_rest_api-automation` | `onesignal_rest_api` | `references/onesignal_rest_api.md` | `4d7825558b3f935f` |
| `specialists/marketing/metaads-automation` | `metaads` | `references/metaads.md` | `2a80980b0731a6b1` |

**Diferido con evidencia:** `microsoft-clarity-automation` (254 líneas, workflows
propios de exportación de analítica, sin Rube MCP): comparte el verbo «Automatizar»,
no la técnica. Entra en otro lote si se decide.

## Verificación

| Comprobación | Resultado |
|---|---|
| Aduana | **SUPERADA** · 0 errores críticos |
| Métrica oficial | 719 → **716** skills · 76 → **66** pares · 38 → **37** grupos · 13,07 % → **12,43 %** |
| Dueño del árbol (I5) | El paraguas nació `root:10000` — **corregido** a `hermes:hermes` (10000:10000, 2775/664) y **probado con write-probe** como uid 10000 |
| Ledger | `data/state/f6_lote1_ledger.jsonl` |

## Reversión

```bash
mv data/archive/F6_lote1_<ts>/absorbidas/<ruta>/ skills/<ruta>/
git revert <commit del lote 1>
```
