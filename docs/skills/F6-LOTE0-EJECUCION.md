# F6 · Lote 0 — ejecución

| Campo | Valor |
|---|---|
| Documento | `docs/skills/F6-LOTE0-EJECUCION.md` |
| Fecha | 2026-09-23 |
| Comando | `python3 scripts/f6_lote0_ejecutar.py --firma <TOKEN>` |
| Motor | `scripts/f6_lote0_ejecutar.py` (candado en código) |
| Commit | `1e256e10ec` → enmendado a `f3a3a1df9a` |
| Archivo del lote | `data/archive/F6_lote0_2026-09-23-150318/` |

## Candado (en código, no en la disciplina del agente)

El motor aborta sin escribir nada si falta cualquiera de estas condiciones:

1. `data/state/f4_curador_last.json` → **`revisiones_limpias >= 2`**
   (la segunda se corrió el 23-sep a las 15:00: `mutaciones: NINGUNA`, `rc=0`)
2. **Firma del dueño**: sha256 del token == `/root/.sync-firma.sha256`.
   Probado en la dirección negativa: con una firma falsa → `BLOQUEADO` y cero escrituras.
3. Pares declarados en `data/state/f6_lote0.json`.

## Método: absorción sin pérdida (R15)

La skill absorbida **no se borra**. Su contenido íntegro pasa a
`references/<absorbida>.md` de la superviviente, que gana una sección de
procedencia; y el directorio completo (con sus `scripts/`, si los hay) va al
archivo del lote. La entrada del catálogo baja en 1; el contenido queda 100 % accesible
y la reversión es un `mv` desde el archivo.

## Resultado

| Absorbida | Superviviente | Hash antes | Hash después |
|---|---|---|---|
| `productivity/oauth-multi-tenant-integration` | `productivity/oauth-multi-tenant-integrations` | `7329f22ccea04d98` | `4c2d6e9e6e1fb60f` |
| `specialists/hermes-internal/brain-graph-ops` | `specialists/hermes-internal/brain-graph-operations` | `7b8524ecea1b44d8` | `f6d270c6b4f4442f` |
| `specialists/marketing/analytics` | `specialists/marketing/analytics-tracking` | `e5ac8c8f9826ff62` | `6ebac6b0327e9b46` |

**Diferido con evidencia:** `pinecone-research` → `pinecone`. Está registrada en
`.hub/lock.json` (instalación de hub) y su directorio carga `scripts/`, que exigen
reubicación y revisar quién los invoca. Además el solape (0,5045) es de tema, no de
objeto: una es la skill de la base vectorial y la otra un caso aplicado de RAG.

## Verificación

| Comprobación | Resultado |
|---|---|
| Aduana (`verify_skills.py`) | **SUPERADA** · 0 errores críticos · 1 advertencia (R5, métrica) |
| Métrica oficial | **bajó**: 722 → **719** `SKILL.md` · 79 → **76** pares · 41 → **38** grupos · 13,85 % → **13,07 %** |
| R7 (nombres equivalentes) | baseline a 0 grupos: el único conocido quedó resuelto |
| Ledger | `data/state/f6_lote0_ledger.jsonl` con hash antes/después por skill |

## Reversión

```bash
# una skill absorbida se restaura con su directorio íntegro:
mv data/archive/F6_lote0_2026-09-23-150318/absorbidas/<ruta>/ skills/<ruta>/
# y se retira la referencia creada:
rm skills/<superviviente>/references/<absorbida>.md
git revert f3a3a1df9a   # o git checkout <hash> -- <rutas>
```
