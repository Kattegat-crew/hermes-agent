---
name: brain-graph-ops
description: "Use when operando el grafo del brain."
version: 1.0.0
author: ragnar
triggers:
  - "consultar el brain"
  - "grafo de memoria"
  - "memory_graph"
  - "brain_graph"
  - "indexar el brain"
---

# Operar el grafo del brain (indexar + consultar + reparar)

El brain (`/opt/data/brain/`) es el conocimiento de negocio de la casa; su **grafo** (`brain/graphify-out/graph.json`) es el índice de consulta. Regla del Admin: **consultar el grafo, no leer los archivos** (377 notas y creciendo).

## Consultar (siempre antes de leer .md)

```bash
# Principal: recorrido BFS con presupuesto de tokens
graphify query "<tema>" --graph /opt/data/brain/graphify-out/graph.json --budget 2000
# Explicar un nodo y su entorno / nodos estructurales
graphify explain "<nodo>" --graph /opt/data/brain/graphify-out/graph.json
graphify god-nodes --top 10 --graph /opt/data/brain/graphify-out/graph.json
# Helper local (substring, SENSIBLE A ACENTOS)
python3 /opt/data/tools/memory_graph.py "<tema>"
```
Después leer el `.md` **solo** si hace falta el detalle de una nota concreta.

## Escritura de notas

- Carpetas: cliente/campaña → la existente; concepto transversal → `concepts/`; estándar operativo → `ops/`. **Carpetas nuevas: autorizadas por el Admin (11-sep-2026) si son kebab-case y quedan registradas** en `folder-maps/brain.md` + enlazadas en `index.md`.
- Si ya existe nota del tema: **actualizarla**, no duplicar. Código y estados temporales NO van al brain.
- El cron `guardar-diario-memoria` (23:00) hace esto solo al cierre del día.

## Automatización del índice

| Cron | Hora | Qué hace |
|---|---|---|
| `guardar-diario-memoria` | 23:00 | Engram + Diario wiki + **nota del brain del día** |
| `brain-graph-update-noche` | 3:30 | Indexa **solo lo nuevo/cambiado**; domingos = completo |

Diseño del indexado (`scripts/brain_graph_update_inner.sh` + wrapper que lo ejecuta con `docker exec`):
1. Manifest de hashes (`graphify-out/.brain_manifest.json`) → lista de notas nuevas/cambiadas.
2. Si no hay cambios y no es domingo → **exit 0 sin llamar a la API (coste 0)**.
3. Extracción **parcial** de solo lo cambiado a un dir temporal → `merge-graphs` con el principal (escribir a un TERCER path y luego `mv`).
4. Fallback y domingos: extracción con `--force`, que **REEMPLAZA** el grafo (fusionarla con el backup lo DUPLICA).

Medido el 11-sep-2026: 3 notas = **$0,0213** y +28 nodos; una corrida sin cambios = $0.

## Pitfalls (verificados)

- **NO quitar `--force` del wrapper** para "optimizar": el incremental nativo de graphify está roto con este brain (`deduplicate_entities: nodes span multiple repos ['data_brain','data_brain-2']`) y el wrapper reportaba `DONE` aunque fallara → el grafo quedaría congelado en silencio.
- **Nunca meta la lógica en un `docker exec bash -c "..."` anidado**: el escapado se rompe (el early-exit no se evaluó y se disparó el modo completo). La lógica va en archivo aparte.
- **`grep -c .` sobre un archivo VACÍO imprime `0` Y devuelve exit 1** → con `|| echo 0` la variable queda `"0\n0"` y `[ ... -eq 0 ]` revienta. Usar `awk 'NF' | wc -l`.
- **Guardas obligatorias tras indexar**: si el incremento ENCOGE el grafo o lo hace crecer >1,3x, restaurar desde copia y reportar `EXTRACT_ERROR`. (Pasó: 81.912 = 2×40.956 nodos duplicados.)
- **Copias de recuperación**: `graph.json.pre-run` / `.bak-last` / `merged-<fecha>.json`. El grafo es root-owned en algunos artefactos: para reemplazarlo hay que hacerlo desde el host (`ssh dev`), no desde el contenedor (hermes no puede sobrescribir archivos root).
- **IDs con guiones bajos** (`brain-inc::concepts_gate_de_gasto`): al filtrar por id usar `_`, no `-`.
- La consulta es **sensible a acentos** (`"modulos neural"` → 0; `"Módulos Neural"` → nodos).
- El grafo se construye con un **modelo de PAGO**: no reconstruirlo a mano sin autorización.
