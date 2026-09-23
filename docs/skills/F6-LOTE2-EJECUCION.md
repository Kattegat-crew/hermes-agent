# F6 · Lote 2 — pares de solape alto con absorción limpia

| Campo | Valor |
|---|---|
| Documento | `docs/skills/F6-LOTE2-EJECUCION.md` |
| Fecha | 2026-09-23 |
| Comando | `python3 scripts/f6_lote2_ejecutar.py --firma <TOKEN>` |
| Motor | `scripts/f6_lote2_ejecutar.py` (candado en código) |

## Resultado

| Absorbida | Superviviente | Hash antes | Reversible desde |
|---|---|---|---|
| `creative/social-content` | `specialists/marketing/social` | `02008f95432fd0c9` | `data/archive/F6_lote2_20260923-154924/absorbidas/creative/social-content` |
| `software-development/hermes-desktop-ssh-diagnostico` | `software-development/hermes-desktop-ssh-backend` | `229a96b7c310b2fc` | `data/archive/F6_lote2_20260923-154924/absorbidas/software-development/hermes-desktop-ssh-diagnostico` |

**Diferido con evidencia:** `hermes-bible-study` → `hermes-bible` (0,9994). Los
`SKILL.md` son casi idénticos (6 bytes, 240 líneas) pero cada directorio arrastra
~3,2 MB de `bundles/` + `references/`, y `hermes-bible-study/scripts/hermes-bible-updater.py`
referencia a `hermes-bible`: hay que decidir dónde viven los bundles y quién invoca el
script antes de tocar nada. Lote propio.

## Verificación

| Comprobación | Resultado |
|---|---|
| Aduana | **SUPERADA** · 0 errores críticos |
| Métrica oficial | 716 → **714** skills · 66 → **63** pares · 37 → **35** grupos · 12,43 % → **11,76 %** |
| Puntero en la superviviente | Añadida la sección `## Referencias absorbidas` (faltaba: el lote creó la referencia sin enlazarla) |
| Dueño (I5) | `hermes:hermes` 2775/664 + write-probe como uid 10000 |
| Ledger | `data/state/f6_lote2_ledger.jsonl` |

## Reversión

```bash
mv data/archive/F6_lote2_<ts>/absorbidas/<ruta>/ skills/<ruta>/
git revert <commit del lote 2>
```
