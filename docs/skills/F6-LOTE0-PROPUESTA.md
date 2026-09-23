# F6 · Lote 0 — pares duplicados por nombre (propuesta)

| Campo | Valor |
|---|---|
| Motivo | F6 del plan Rev. 6: la fusión trivial de arranque |
| Fecha | 2026-09-23T13:43:12-0500 |
| Métrica | `docs/skills/METRICA-CONSOLIDACION.md` (TF-IDF 0,45) |
| **Estado** | **PROPUESTA — no ejecutada** |
| Candado | exige 2 revisiones limpias + firma del CTO (R8) |

**Nada de este documento se ha aplicado.** La fusión exige el candado de
F6 (dos revisiones limpias del curador) y firma del CTO lote por lote.

## Los pares

| A | B | Similitud | Idénticos | Líneas solo en A | Líneas solo en B | Riesgo |
|---|---|---|---|---|---|---|
| `productivity/oauth-multi-tenant-integration` | `productivity/oauth-multi-tenant-integrations` | 0.4774 | False | 27 | 36 | bajo |
| `specialists/hermes-internal/brain-graph-operations` | `specialists/hermes-internal/brain-graph-ops` | 0.5661 | False | 68 | 40 | bajo |
| `specialists/marketing/analytics` | `specialists/marketing/analytics-tracking` | 0.4451 | False | 286 | 357 | bajo |
| `specialists/data-vector/pinecone` | `specialists/data-vector/pinecone-research` | 0.4265 | False | 339 | 66 | bajo |

## Propuesta por par

### `productivity/oauth-multi-tenant-integration`  ⇄  `productivity/oauth-multi-tenant-integrations`

- **Similitud oficial:** 0.4774
- **Tamaños:** A 2827 bytes / 37 líneas · B 3267 bytes / 46 líneas
- **Hashes:** A `474f7c41006d9aad` · B `7329f22ccea04d98`
- **Propuesta:** Integrar las 27 líneas exclusivas del más pobre en el que absorbe, y archivar el absorbido
- **Riesgo:** bajo

### `specialists/hermes-internal/brain-graph-operations`  ⇄  `specialists/hermes-internal/brain-graph-ops`

- **Similitud oficial:** 0.5661
- **Tamaños:** A 6198 bytes / 89 líneas · B 3860 bytes / 61 líneas
- **Hashes:** A `7b8524ecea1b44d8` · B `522c533270155e85`
- **Propuesta:** Integrar las 40 líneas exclusivas del más pobre en el que absorbe, y archivar el absorbido
- **Riesgo:** bajo

### `specialists/marketing/analytics`  ⇄  `specialists/marketing/analytics-tracking`

- **Similitud oficial:** 0.4451
- **Tamaños:** A 8633 bytes / 310 líneas · B 15021 bytes / 381 líneas
- **Hashes:** A `3eda97d96b2329da` · B `e5ac8c8f9826ff62`
- **Propuesta:** Integrar las 286 líneas exclusivas del más pobre en el que absorbe, y archivar el absorbido
- **Riesgo:** bajo

### `specialists/data-vector/pinecone`  ⇄  `specialists/data-vector/pinecone-research`

- **Similitud oficial:** 0.4265
- **Tamaños:** A 8524 bytes / 381 líneas · B 3051 bytes / 108 líneas
- **Hashes:** A `7947f49681dd4107` · B `540dafd300c1ea3c`
- **Propuesta:** Integrar las 66 líneas exclusivas del más pobre en el que absorbe, y archivar el absorbido
- **Riesgo:** bajo

## Procedimiento de ejecución (cuando se firme)

1. `git status` limpio y `git pull` en el repositorio.
2. Respaldo: `tar czf data/archive/F6_lote0_<ts>.tar.gz skills/<rutas>` + sha256.
3. Integrar el contenido exclusivo en la skill que absorbe (patch).
4. `git mv` del absorbido a `data/archive/F6_lote0_<ts>/`.
5. Aduana (`scripts/verify_skills.py`) y métrica oficial de nuevo: el
   porcentaje implicado debe **bajar** y el diff, ser solo el esperado.
6. Commit con el ledger: hash antes/después por skill.
7. Revisor independiente por lote (R8).

## Ledger

El detalle con hashes queda en `data/state/f6_lote0.json`. Al ejecutar,
cada par añade su entrada antes/después en el ledger del lote.
