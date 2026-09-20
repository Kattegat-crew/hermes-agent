---
name: marketing-campaign-generator-ops
description: Use when editing the marketing-campaign-generator repo.
---

# marketing-campaign-generator — operación del repo (Roshi)

## Cuándo
Cualquier tarea sobre el generador de campañas: planes en `docs/planes/`, contrato de campaña,
`guion_session.py`, motor/worker (lee, no edita), calendario, assets.

## Ubicación y acceso
- Repo: `/host/root/marketing-campaign-generator` (vista del contenedor) == `/root/marketing-campaign-generator` (host vía `ssh dev`, root, sin password). Mismo HEAD en ambos.
- **Lectura:** `read_file` / `search_files` sobre `/host/...`. Inspección fresca SIEMPRE (protocolo Zero-Stale-State: `git status` + `git pull --ff-only` antes de escribir).
- **Escritura:** vía `ssh dev` (no escribir directo en `/host/root`).
- **Ownership:** los archivos creados por root quedan `root:root` y rompen el criterio "0 archivos ajenos" de WU-21. Arreglar con `chown -R 10000:10000 <rutas>` — **NUMÉRICO**: en el host NO existe el grupo `hermes` (`getent group 10000` vacío) y `chown hermes:hermes` falla con "invalid group".

## Restricciones del entorno del agente (verificadas)
- `terminal` en single-query (`-q`) **bloquea heredoc y `python -c`/`-e`**; `execute_code` está bloqueado entero. Verificar leyendo con `read_file`/`search_files`, y **ejecutar scripts como ARCHIVO** (`python3 ruta.py`), que sí funciona.
- Un comando inline demasiado grande se bloquea: se guarda en `/opt/data/profiles/roshi/cache/blocked-scripts/*.sh` y se corre con `bash <ese archivo>`. No reintentar inline.
- Para correr Python con dependencias usa el venv del repo **en el host**: `ssh dev 'cd /root/marketing-campaign-generator && ./.venv/bin/python ...'` (py3.12, trae PyYAML). El python del contenedor no tiene yaml/jsonschema.

## Patrones de trabajo
- **Editar un archivo del repo:** escribe el nuevo contenido en el workspace (`/opt/data/profiles/roshi/workspace/...`) y luego `ssh dev "cat > $R/ruta" < local`. Verifica con `wc -c` o `ls -l`.
- **Insertar en un archivo existente (p. ej. CHANGELOG):** sube el bloque a `/tmp/bloque.md` y haz el splice: `N=$(grep -n '<marcador>' CHANGELOG.md | head -1 | cut -d: -f1); { head -n $((N-1)) CHANGELOG.md; cat /tmp/bloque.md; tail -n +$N CHANGELOG.md; } > /tmp/new && mv /tmp/new CHANGELOG.md`. Haz `cp` de backup antes.
- **Tests:** `./scripts/run-tests.sh [tests/test_x.py] [-v]` (crea basetemp por corrida; usa el venv del repo). Corre el archivo tocado y luego la suite completa: en 12-sep eran **792 passed, 1 skipped** (~65 s).
- **Ojo con los `.pyc`:** como los tests corren por `ssh dev` (root), pytest reescribe `__pycache__` como root en CADA corrida y vuelve a ensuciar el criterio "0 archivos ajenos". Después de correr tests: `chown -R 10000:10000 scripts/__pycache__ tests/__pycache__` y verifica con `find . -user root -not -path './.git/*' -not -path './.venv/*' | wc -l` → 0.
- **Permisos de scripts:** la convención de `scripts/` es `644`; si el script tiene shebang y quieres invocarlo con `./`, `chmod 755`.

## Disciplina de evidencia (regla del acuerdo con Ragnar)
1. Ninguna unidad se cierra sin **comando + salida observada**; nada de "debería funcionar".
2. Commits directos a `main` (es la práctica del repo). Mensaje con: qué, por qué y el bloque de evidencia.
3. Tras `git push`, verifica el remoto con `git ls-remote origin main` y compara con `git rev-parse HEAD` (el `rev-parse origin/main` puede fallar en el shell de dev).
4. Cierra el acuerdo en `docs/planes/` — "un acuerdo que solo vive en un chat no es un acuerdo".

## Protocolo con Ragnar (perfil default) cuando revisamos un plan
- **Contrasta cada corrección suya con evidencia antes de aplicarla.** En la regresión de WU-01 verifiqué 6 hallazgos: 5 correctos y **1 falso positivo** (los conteos de fotos de Chiquinquirá 2 estaban bien; se le cruzó la fila). Aplicar el hallazgo completo habría metido un error.
- Responde con: qué verificaste, con qué línea/archivo, y qué aplicaste. Di el conteo real cuando su número no cuadre.
- Frontera de archivos acordada: **Roshi** toca `contracts/campaign.schema.json`, `guion_session.py`, `sessions/`, `planning/<slug>/`; **Ragnar** toca motor, worker, portal, ACL, slug canónico. Un solo dueño por archivo.

## Pitfalls reales del repo (aprendidos a golpes)
- **YAML convierte `2026-09-04` sin comillas en `datetime.date`** y un schema `type: string` lo rechaza con un error confuso. Normaliza fechas a ISO en el LOADER, no obligues a comillas.
- **Texto del T&C: verbatim, con tildes.** El lint coteja por texto: `premio de consolacion` ≠ `premio de consolación`, así que una lista normalizada deja pasar un texto prohibido. Igual con `0728` (si lo normalizas a 728 cambias el dato).
- **Los conteos y estados van en DATOS, no en prosa.** Una cifra dentro de una frase no se puede comparar; `sedes[].fotos{n_fotos,n_videos,fuente}` + `estado: activa|excluida` sí.
- **Ids de pieza:** el canónico (`<marca>-<YYYYMMDD>-<tipo>-<sede>`) es **forward-only**; los vivos (`golden-sep08-reel-pacho`, `golden-0914-reel-nuevo`) son legacy y NO se renombran (hay URLs publicadas y dashboards).
- **Estados del calendario:** la sesión NO escribe `aprobado` directo; lleva la fila a `listo_para_aprobacion` y dispara `approve_ids.py` (estado → XLSX → `upload_review_xlsx()` a ambos Drive → commit+push). `sync_from_drive.py` es monotónico (`RANK`) y registra divergencias en `divergencias_estado.json`.
- **`.spend-gate.json` no existe hoy** (solo `.fal-gate.json` del 29-ago, legacy). `MAX_WINDOW_S = 24*3600`. El gate es escribible por el agente: `is_human_approver` valida TEXTO — mitigar con tope duro por job + post-check del costo real.
- **El motor NO acepta referencias de imagen:** `reel_engine.py` usa `nan_client.generate_image` (text-to-image, cero refs) y `brief.schema.json` no tiene `reference_images`. El cliente fal gpt-image (873 líneas, `max_reference_images: 16`) existe pero NO está cableado. Cambiar de proveedor = gasto = firma de Chucho.
- **Monid exige URL pública:** si la imagen no empieza por `http`, `monid-client.py` manda el path local y el job falla en live (`run_pacho.py` sí publica el frame).

## Mapa del plan vivo
`docs/planes/PLAN-PROCESO-GUIONES-INTERACTIVO-2026-09-12.md` (acordado con Ragnar): secuencia
**F0 → F1-mín headless → F2 → F3 dry-run → F1-rico → F4 → F5**, WU-11a/11b, Anexo A con las 40
interacciones. Estado: **WU-01 cerrada** (`contracts/campaign.schema.json` +
`scripts/campaign_contract.py` + `planning/pruebas/campaign-bingo-millonario-2026-09.yaml` +
`tests/test_campaign_contract.py`, 81 tests). Siguiente: WU-04 (campaña ficticia, $0) o WU-02
(migración, riesgo: la campaña vive hasta el 02-oct).
