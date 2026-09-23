# F6 · Lote 3 — pares duplicados reales y declaración de falsos positivos

| Campo | Valor |
|---|---|
| Documento | `docs/skills/F6-LOTE3-EJECUCION.md` |
| Fecha | 2026-09-23 |
| Comando | `python3 scripts/f6_lote3_ejecutar.py --firma <TOKEN>` |
| Motor | `scripts/f6_lote3_ejecutar.py` (candado en código) |

## Absorbido (2)

| Absorbida | Superviviente | Hash antes | Reversible desde |
|---|---|---|---|
| `specialists/marketing/paid-ads` | `specialists/marketing/ads` | `87351be1779ec4f0` | `data/archive/F6_lote3_20260923-155847/absorbidas/specialists/marketing/paid-ads` |
| `devops/open-design-selfhost-ops` | `devops/open-design-deployment` | `496aa8e96650d4d1` | `data/archive/F6_lote3_20260923-155847/absorbidas/devops/open-design-selfhost-ops` |

## Declarado FALSO POSITIVO (no se fusiona)

La métrica agrupa por parecido, y el parecido no siempre es duplicación. Estos grupos
quedan **declarados en `data/state/f6_falsos_positivos.json`** para que no se vuelvan a
litigar ni los fusione un lote automático:

### `autonomous-ai-agents/sdd-*` (10 miembros, sim máx 0.6135)

Son FASES de un flujo (init, explore, propose, spec, design, tasks, apply, verify, onboard) con disparador propio y distinto: el orquestador las lanza por nombre. El parecido viene del andamiaje compartido (## Execution Role, ## Language Domain Contract, ## Purpose, ## What You Receive), que además ya está factorizado en specialists/hermes-internal/_shared/sdd-phase-common.md. Tamaños de 4.164 a 14.949 B: no son plantilla repetida. chained-pr entró al grupo sólo por el encabezado. Fusionarlas rompería disparadores legítimos.

**Acción:** NO fusionar

### `specialists/ai-ml/pytorch-fsdp <-> specialists/ai-ml/unsloth` (2 miembros, sim máx 0.6850)

Herramientas distintas: FSDP (entrenamiento distribuido con sharding) frente a Unsloth (fine-tuning LoRA/QLoRA acelerado). El solape es del andamiaje de skills de ML. Cada una arrastra su propio references/ (486 KB y 1,86 MB).

**Acción:** NO fusionar

## Diferido con evidencia (no descartado)

- `software-development/amazon-sp-api` → `software-development/amazon-spapi-integration`: DIFERIDO: mismo objeto (SP-API = SPAPI) pero AMBAS cargan scripts/ propios (21 KB y 39 KB) con riesgo de colisión de nombres, y amazon-sp-api tiene una referencia entrante desde specialists/marketing/amazon-sp-api-listings. Antes de absorber hay que revisar qué invoca cada script.

- `productivity/colombia-juegos-promocionales` → `specialists/marketing-ads/colombia-promociones-legales`: DIFERIDO: no son duplicadas, son complementarias (juegos promocionales vs marco legal de promociones) y el paraguas core/colombia-legal-ops ya guarda copia de ambas como referencias. Además las dos tienen la descripción VACÍA: es una limpieza de R5, no una fusión.

## Verificación

| Comprobación | Resultado |
|---|---|
| Aduana | **SUPERADA** · 0 errores críticos |
| Métrica oficial | 714 → **712** skills · 63 → **61** pares · 35 → **33** grupos · 11,76 % → **11,24 %** |
| Puntero en la superviviente | `## Referencias absorbidas` añadida en las dos (lección del lote 2) |
| Extras vivos | Los `references/` del absorbido se copian a `references/<absorbido>/` |
| Dueño (I5) | `hermes:hermes` 2775/664 |
| Ledger | `data/state/f6_lote3_ledger.jsonl` |

## Reversión

```bash
mv data/archive/F6_lote3_<ts>/absorbidas/<ruta>/ skills/<ruta>/
git revert <commit del lote 3>
```
