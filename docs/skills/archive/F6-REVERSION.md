# F6 · Material de reversión (versionado)

Reserva del revisor independiente (Ragnar, 23-sep-2026): la reversibilidad de los
lotes de consolidación vivía solo en disco (`data/archive/`, gitignoreado).

| Campo | Valor |
|---|---|
| Paquete | `F6-reversibilidad-20260923-181049.tar.gz` |
| Tamaño | 46 KB |
| sha256 | `a55a981e54d15b82cca4c763ad9088c5f6f104907a82ee178a6b02cf03544964` |
| Originales absorbidos dentro | 16 `SKILL.md` |
| Ledgers dentro | 5 |

## Reversión de un lote

```bash
cd /root/hermes-agent
tar xzf docs/skills/archive/F6-reversibilidad-20260923-181049.tar.gz
mv data/archive/F6_loteN_<ts>/absorbidas/<ruta>/ skills/<ruta>/
git revert <commit del lote>
```

Verificación del paquete: `sha256sum -c docs/skills/archive/F6-reversibilidad-20260923-181049.tar.gz.sha256`
