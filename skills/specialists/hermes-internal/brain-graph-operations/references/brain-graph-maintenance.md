# Caso trabajado — mantenimiento del grafo del brain (2026-09-11)

Sesión completa: automatizar que el brain crezca solo y que su grafo se actualice incrementalmente, sin gastar de más. Cuatro bugs reales, dos incidentes de artefacto dañado, todo recuperado.

## Estado de partida

- `/opt/data/brain/`: 377 notas `.md` (sin `archive/`).
- Grafo: 40.928 nodos / 42.536 aristas, **root:root**, construido por el cron nocturno.
- Cron `brain-graph-update-noche` (3:30, `no_agent`) → `brain_graph_update_wrapper.sh` → `docker exec hermes-agent bash -c '…'` con `graphify extract --force` (todo el brain, cada noche).

## Incidentes y recuperación

| # | Qué pasó | Causa raíz | Recuperación |
|---|---|---|---|
| 1 | extract incremental abortó con `ValueError: deduplicate_entities: nodes span multiple repos ['data_brain','data_brain-2']` | el incremental nativo de graphify no soporta este grafo acumulado | ninguna pérdida: el fallo ocurrió antes de escribir (verificado: grafo idéntico al backup) |
| 2 | el grafo bajó a **10.232** nodos | se disparó el modo completo y el merge leyó/escribió el mismo path | `cp merged-20260911.json graph.json` (root, vía `ssh dev`) |
| 3 | el grafo subió a **81.912** nodos (=2×40.956) | `--force` devuelve el grafo completo y se fusionó con el backup | ídem, restauración desde el snapshot |

Tras cada restauración: `chown hermes:10000 graph.json` y conteo de nodos por lectura del JSON.

## Bugs propios (del wrapper nuevo)

1. **Escapado anidado**: la lógica dentro de `docker exec ... bash -c "…"` no evaluó la salida temprana → se disparó el camino caro. Fix: wrapper fino en el host + `brain_graph_update_inner.sh` dentro del contenedor.
2. **`grep -c .` en archivo vacío** (imprime `0` y exit 1) → `$( … || echo 0 )` dejó `"0\n0"` → `integer expression expected` → rama equivocada. Fix: `awk 'NF' f | wc -l`.
3. **Detector de éxito laxo** (`grep -q "merged|done"`) → reportaba `DONE` con el extract reventado: el grafo se habría quedado congelado en silencio. Fix: buscar `Traceback|Error|ValueError` y reportar `FALLO`.
4. **Sin guardas de invariante**: no había verificación antes/después. Fix: si el incremental baja nodos o sube >1,3x → restaurar desde `.pre-run` y reportar `EXTRACT_ERROR`.

## Mediciones (para presupuestar)

- **3 notas nuevas** → 28 nodos, `tokens: 3.004 in / 12.551 out`, **`est. cost (~openai): $0,0213`**.
- Modo completo: ~479 archivos reprocesados por noche ⇒ extrapolando, del orden de **~$3/noche**.
- Escaneo incremental nativo (para diagnóstico): `0 code, 30 docs, 20 papers, 1 images changed; 428 unchanged`.
- **0 cambios ⇒ 0 llamadas a la API** (verificado en la vía real: `nodes before=40956 after=40956`).

## Verificación del flujo diario (cómo se cerró)

1. Sembrar el manifest a mano (`sha1` de las 377 notas) para que la primera corrida no reprocesara todo.
2. Correr el wrapper **por la vía real** (`ssh dev 'bash …/brain_graph_update_wrapper.sh'`) — no solo el inner: valida `docker exec`, permisos y conteo.
3. Comprobar `sin cambios: 0 notas nuevas → no se llamó a la API (coste 0)` y `nodes before=40956 after=40956`.
4. Comprobar que la consulta encuentra las notas nuevas: `graphify query "gate de gasto firma" …` → nodos con `src=concepts/gate-de-gasto.md` y `src=ops/revision-independiente-de-codigo.md`.

## Pendiente al cierre de la sesión

- La corrida real del ciclo completo (23:00 escribe nota → 3:30 la indexa) quedó **sin verificar** en el momento del cierre: es lo primero a comprobar en la sesión siguiente (conteo de nodos + línea de coste del log).
- Propuestas abiertas: excluir `raw/` y `archive/` del grafo (`.graphifyignore`), y usar `save-result`/`reflect` para el `LESSONS.md`.
