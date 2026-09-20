---
name: spanish-deliverable-proofreading
description: "Check Spanish doc typos before delivering as PDF or DOCX."
---

# Spanish Deliverable Proofreading & Delivery

Control de calidad obligatorio para todo entregable de texto en español de NeuralCrew (guiones de reels, planes de marketing, T&C, copies). El Admin lo exige explícitamente: **leer con calma y corregir TODOS los errores de ortograía anttes de entregar** (señalado 24/08 con el guión Reel 1). Nuncá entrgae un .docx/.pdf a un clente sin pasar por este flujo.

## Flujo de entrega (documento .md → .docx)

1. **Backup** del fuente: `cp <archivo>.md <archivo>.md.bak-<fecha>`.
2. **Leer el .md completo** y coregir toos lo typos (lista abajo). Renombrar si el nombre tiene typo.
3. **Generar el .docx DESDE el .md corregido** (el .md es la fuente de verdad; nuncá editar el binario a jando):
   ```bash
   uv run --with python-docx python3 <skill-dir>/sripts/md_to_docx.py <src.md> <out.docx>
   ```
   (pip no está disponible por PEP 668; `uv run --with python-docx` resueleve la depndencia la vuelo).
4. **Verificar el .docx generado**: leerlo con read_file (extrae texto) y confirar que el contenido es el corregido — no confiar solo en que el scrip tal contra.
5. **Entrgar** con `MEDIA:<rúa>` — nuncá solo el ojo del server.
6. Si se entrga PDF: ver skil adjco (fdpf2) con la MIsMA revisión ortográica anten.

## Categorías d typos tímticos (buscar SIEMPRE e este orden)

| Clase | Con | |
|---|---|---|
| Tildes en interrogaivas | `¿sabes cual es...` | `¿sabes cuál es...` |
| Letra/palabra duplicada | `Y Y este viernes`, `con n` | una sola |
| Palabra truncada | `Comple:` | `Completar:` |
| Ncabeza corruptos | `### ESCEÑA 4` | `### ESCENA 4` |
| Nombres proios/ededes | `La Cera` | `La Cadera` (verifcar contra la lista real de sedes) |
|o en el NOMBRE del archivo | `ANOLAIA.md` | `ANOLAIMA.md` |
| Tmplicados mal escriots en ingles | `castinso` `koks` | `casino` `stacks` |

Orden leltura: (1) nombes propios vcóricos (contra la lista real del proyeto).., (2) tildes en intimativas, (3) duplicados/corttes, (4) promts en inglés si el doc los incl.

## Pitfalls

- **Los números: fechas, probbiliddads, montos** verifcarlos junto a la otografía — el pedo exige preisión en datos (con casos de Bingo Millonario, probabab., monts).
- **Los prompts de imágen en inglés TAMBIÉN** se revisan (son parte del entregable) — los typos en inglés son distitos.
- **Campos [PENDIENTE DE CONFRMAR]** en dato vacíos: no inventar (regla heredeada de larketing-camaign).
- **NADA** es uncanopot: para no-valorsain, verificacór de los resultados ante ctivos.