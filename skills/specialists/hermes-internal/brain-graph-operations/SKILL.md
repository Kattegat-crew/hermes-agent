---
name: brain-graph-operations
description: "Use when maintaining or querying the brain knowledge graph."
version: 1.0.0
author: curator-ragnar
triggers:
  - "consultar el brain"
  - "grafo del brain"
  - "graphify"
  - "graph.json"
  - "memory_graph"
  - "indexar notas"
  - "el brain no se actualiza"
---

# Brain Graph Operations — consultar el grafo y mantenerlo actualizado

El brain (`/opt/data/brain/`, cientos de notas `.md`) se consulta por su **grafo**, no leyendo archivos: leer 377 notas es imposible y caro. Este skill cubre las dos mitades: **consultar** (barato) y **mantener el índice** (que crezca solo, sin gastar de más).

## 1. Consultar (siempre esto ANTES de leer notas)

```bash
graphify query "<tema>" --graph /opt/data/brain/graphify-out/graph.json --budget 2000
graphify explain "<nodo>"                         # contexto de un nodo y sus vecinos
graphify god-nodes --top 10                       # qué es estructural del brain
python3 /opt/data/tools/memory_graph.py "<tema>"  # helper local
```

- Los nodos traen `src=<carpeta>/<nota>.md`: **eso** decide si hace falta `read_file` de ESA nota (y no de otras).
- `TRUNCATED` en la salida ⇒ subir `--budget` o acotar el tema.
- **El helper local es sensible a acentos**: `"modulos neural"` → 0 resultados; `"Módulos Neural"` → nodos. Usar el término tal como aparece en la nota.
- Los ids de nodo **incrustan el directorio de extracción**: si se extrae desde `/tmp/brain-inc`, los ids salen `brain-inc::…`. Extraer siempre desde un subdir llamado `brain`.
- Feedback: `graphify save-result --question … --answer … --nodes … --outcome useful|dead_end|corrected` y `graphify reflect` → `graphify-out/reflections/LESSONS.md`. Sirve para que el grafo priorice lo que de verdad se consulta.

## 2. Mantener el índice (incremental por manifest)

**Nunca** reconstruir el grafo completo a mano: `graphify extract` **llama a un modelo de PAGO** (qwen3.6 vía NaN). Corrió completo cada noche hasta 2026-09-11 (≈479 archivos reprocesados, del orden de ~$3/noche).

Diseño vigente (dos archivos, a propósito):

```
HOST  /opt/data/scripts/brain_graph_update_wrapper.sh   <- lo llama el cron brain-graph-update-noche (3:30)
        └── docker exec hermes-agent bash /opt/data/scripts/brain_graph_update_inner.sh
CONT. /opt/data/scripts/brain_graph_update_inner.sh      <- TODA la lógica
```

Flujo del inner:
1. **Manifest sha1** (`graphify-out/.brain_manifest.json`) de las `.md` (excluye `graphify-out/` y `archive/`) → nuevas/cambiadas.
2. **0 cambios y no domingo** → salir sin llamar a la API (**coste 0**, verificado).
3. **Con cambios** → copiar SOLO esas notas a `/tmp/brain-inc/brain/` → `graphify extract` de ese dir → `graphify merge-graphs <grafo> <parcial> --out /tmp/brain_merged.json` → `mv` sobre el real.
4. **Domingo o `FULL=1`** → `--force` sobre el brain completo, que **REEMPLAZA** el grafo (no se fusiona).
5. **Guardas**: el incremental no debe bajar nodos ni subir >1,3x → restaurar desde `.pre-run` y reportar `EXTRACT_ERROR`.

Medición de referencia (3 notas nuevas): **$0,0213**, +28 nodos.

### Bugs de graphify en este brain — NO repetirlos

| Síntoma | Causa | Qué hacer |
|---|---|---|
| `ValueError: deduplicate_entities: nodes span multiple repos ['data_brain','data_brain-2']` | el incremental NATIVO (`extract` sin `--force`) mezcla tags de repo | no usar el incremental nativo; hacerlo por archivo con manifest |
| el grafo pasa de 40.956 a **81.912** nodos (2x) | `--force` ya devuelve el grafo COMPLETO y se fusionó con el backup | con `--force`: **reemplazar**, no fusionar |
| el grafo cae a 10.232 nodos | merge leyendo y escribiendo el MISMO path | `merge-graphs … --out <tercer archivo>` y luego `mv` |
| el job reporta `DONE` con el grafo congelado | el detector de éxito era `grep -q "merged\|done"` | buscar `Traceback\|Error` y reportar `FALLO` |

## 3. Scripts que mantienen artefactos (reglas transferibles)

Aprendidas construyendo lo de arriba; aplican a cualquier cron que reconstruya un artefacto:

1. **La lógica va en un ARCHIVO, no dentro de `docker exec ... bash -c "…"`**: las comillas anidadas rompen el escapado de forma invisible (aquí la salida temprana nunca se evaluó y se disparó el camino caro).
2. **`grep -c . archivo_vacio` imprime `0` Y devuelve exit 1**: con `|| echo 0` la variable queda `"0\n0"` y `[ "$N" -eq 0 ]` falla con `integer expression expected` → rama equivocada. Usar `awk 'NF' f | wc -l`.
3. **Guardas de invariante antes/después** con restauración desde copia: un artefacto solo debe cambiar dentro de un rango declarado.
4. **Salida temprana cuando no hay cambios** si el script llama a una API de pago; registrar el coste real en el log.
5. **Ownership root vs hermes**: el `docker exec` corre como root y deja artefactos `root:root`; el agente del contenedor (hermes) **crea** archivos nuevos en un dir escribible pero **no sobrescribe** los root-owned (`Permission denied`). Camino probado: escribir el nuevo con otro nombre y que root haga el `mv` (`ssh <host> 'cp $D/nuevo.json $D/graph.json'`), luego `chown hermes:10000`.
6. **Backup fechado antes de cada corrida destructiva** (`graph.json.pre-run`, `merged-<fecha>.json`): recuperar es un `cp`, no una reconstrucción.

## 4. Verificación de que el índice quedó bien

```bash
python3 -c "import json;print(len(json.load(open('/opt/data/brain/graphify-out/graph.json'))['nodes']))"
graphify query "<tema de la nota nueva>" --graph /opt/data/brain/graphify-out/graph.json --budget 300 | grep NODE
```

Contar por lectura del JSON, **nunca** por el tamaño del archivo. Y comparar antes/después: si el conteo no cuadra con lo que se escribió, el merge no aplicó.

## 5. Dónde vive el conocimiento de las notas

Este skill cubre el GRAFO. El ruteo de qué nota va en qué carpeta del brain y las reglas de escritura están en `brain/AGENTS.md` + `brain/folder-maps/brain.md` (carpetas nuevas autorizadas desde 2026-09-11 si son descriptivas, kebab-case y **registradas**). El mapa de capas de memoria (memoria nativa / Engram / brain / git) vive en la skill `memory-architecture`.

Detalle del caso completo (los cuatro bugs, mediciones e incidentes): `references/brain-graph-maintenance.md`.

## Referencias absorbidas

- `references/brain-graph-ops.md` — absorbida desde `specialists/hermes-internal/brain-graph-ops` el 2026-09-23 (F6 lote 0, R15: condensar sin borrar).
