# F6 · Paquete de revisión independiente (R8)

**Para:** **Ragnar** (Discord `Ragnar#4498`, id `1493385610797252758`) — revisor independiente de la consolidación. Alternativa válida: Plon (Admin).
**De:** Roshi — operativo de Chucho
**Fecha:** 23-sep-2026
**Estado:** 5 lotes ejecutados, consolidación mecánica **cerrada**

---

## 1. Qué se te pide

Revisar los **cinco lotes** de consolidación del catálogo de skills (F6) y decir, por cada uno,
si el trabajo es correcto o si hay que revertirlo. La política de la casa (R8) exige **revisor
independiente por lote**: quien ejecuta no se firma a sí mismo. El ejecutor fui yo.

## 2. Qué se hizo, en una línea por lote

| Lote | Absorbe | Acta |
|---|---|---|
| 0 | 3 pares duplicados por nombre (`oauth-…integration(s)`, `brain-graph-ops`, `analytics`) | `docs/skills/F6-LOTE0-EJECUCION.md` |
| 1 | 4 casos de una misma plantilla bajo el paraguas nuevo `productivity/rube-mcp-api-automation` | `docs/skills/F6-LOTE1-EJECUCION.md` |
| 2 | 2 pares de solape alto (`social-content`→`social`, `ssh-diagnostico`→`ssh-backend`) | `docs/skills/F6-LOTE2-EJECUCION.md` |
| 3 | 2 duplicados reales (`paid-ads`→`ads`, `open-design-selfhost-ops`→`open-design-deployment`) | `docs/skills/F6-LOTE3-EJECUCION.md` |
| 4 | 5 pares del tramo 0,51-0,59 (avatares, Windows, proveedores, `/soul`, Desktop remoto) | `docs/skills/F6-LOTE4-EJECUCION.md` |

**Método (idéntico en los cinco):** la skill absorbida **no se borra**. Su `SKILL.md` íntegro pasa
a `references/<absorbida>.md` dentro de la superviviente (con sección `## Referencias absorbidas`
que lo enlaza), sus ficheros extra (`scripts/`, `references/`) se copian a
`references/<absorbida>/` para que sigan vivos, y el directorio completo queda en
`data/archive/F6_loteN_<ts>/absorbidas/`.

**Candado en código:** cada motor aborta **sin escribir nada** si el curador no acumula 2/2
revisiones limpias o si falta la firma del dueño. Probado en negativo en los cinco lotes.

## 3. Las cinco afirmaciones que debes intentar falsificar

**Un solo comando las comprueba todas** (re-deriva los hechos del repo, no se
cree las actas; emite PASS/FAIL por afirmación y por lote):

```bash
python3 scripts/f6_verifica_revision.py
```


Todas son reproducibles con un comando. No te pido que confíes: te pido que compruebes.

1. **No se perdió contenido.** Para cada skill absorbida debe existir (a) su `SKILL.md` original
   en el archivo del lote y (b) su contenido en el `references/` de la superviviente.
2. **El catálogo en git cuadra con el árbol vivo.** `python3 scripts/f3_higiene_diaria.py --dry-run --sin-notificar`
   → `V4_catalogo: en_git == alcanzables`.
3. **La calidad no bajó.** `python3 scripts/verify_skills.py` → `Errores críticos: 0`.
4. **El candado funciona.** `python3 scripts/f6_lote4_ejecutar.py` (sin `--firma`) → `BLOQUEADO`
   y cero escrituras.
5. **La métrica bajó de verdad.** `python3 scripts/f6_metrica_oficial.py` → pares 85 → 56,
   grupos 45 → 29, implicadas 115 → 71 (16,0 % → 10,04 %) sobre un catálogo 722 → 707.

**Reversión de un lote (una línea por skill):**

```bash
mv data/archive/F6_loteN_<ts>/absorbidas/<ruta>/ skills/<ruta>/
git revert <commit del lote>
```

Commits: `f3a3a1df9a` (lote 0) · `7c1f8809a6` (acta) · `9595147fd2` (lote 1) · `9ff5b2033b` (lote 2)
· `dd489879d6` (lote 3) · `e16b0d4c3f` (lote 4).

## 4. Las decisiones que NO debe tomar el ejecutor (juicio tuyo)

1. **6 diferidos** (`data/state/f6_diferidos.json`): par bíblico (bundles de 3,2 MB + updater
   acoplado), `pinecone-research` (instalación de hub + `scripts/`), `amazon-sp-api` (scripts en
   ambos lados), `colombia-*` (complementarias y con descripción vacía), `microsoft-clarity`
   (otra clase), `meta-ads-campaigns` ⇄ `meta-ads-operations`, `writing-plans` ⇄ `plan`
   (y la **colisión del comando `/plan`** con un comando núcleo de Hermes).
   → ¿Están bien diferidos o alguno debería fusionarse ya?
2. **4 falsos positivos declarados** (`data/state/f6_falsos_positivos.json`): familia `sdd-*` (10),
   `pytorch-fsdp` ⇄ `unsloth`, `aws-*` ⇄ `gcp-*`, `3-statement-model` ⇄ `lbo-model`,
   `form-cro` ⇄ `signup`. → ¿Estás de acuerdo en que **no** se fusionan?
3. **19 grupos pendientes** (`docs/skills/F6-REGISTRO-GRUPOS.md`, todos por debajo de 0,62):
   ¿se triajan ahora, o se dejan como están?
4. **El fin del contenido absorbido:** hoy vive en `references/` (íntegro) y en el archivo.
   ¿Es el destino correcto, o prefieres que el `SKILL.md` de la superviviente lo integre en línea?

## 5. Firma del revisor

| Campo | Valor |
|---|---|
| Revisor | Ragnar (`1493385610797252758`), solicitado el 23-sep-2026 |
| Fecha | |
| Lote 0 / 1 / 2 / 3 / 4 | aprobado · con reservas · revertir |
| Reservas u objeciones | |

---

*El paquete se apoya en `docs/skills/POLITICA-ARBOL-CANONICO.md` y en el plan Rev. 6 (§F6).
Los datos crudos están en `data/state/` (métrica, ledger por lote, falsos positivos, diferidos,
registro de grupos).*
