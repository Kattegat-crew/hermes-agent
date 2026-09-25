---
name: informe-mensual-sheet-pdf
description: "Use when building a live monthly Sheet + PDF report."
tags: [informes, reports, google-sheet, cron, pdf, ventas]
version: 1.0.0
author: Ragnar
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [informes, google-sheet, cron, pdf, membretado, ventas, prod]
    category: productivity
    related_skills: [marketing-calendar-publishing, neuralcrew-letterhead]
---

# Informe mensual vivo (Sheet acumulativo + PDF de cierre)

Mantiene un Google Sheet que se actualiza solo cada dia con el dato diario y que, al
cerrar el mes, produce un PDF membretado del mes completo. Caso de referencia: ventas
Golden Game, perfil `helmer` en PROD. Detalle completo y evidencia en
`brain/ops/informe-mensual-ventas-golden.md`.

## When to Use

- El cliente pide "un sheet que se vaya actualizando solo" con datos diarios por sucursal/local.
- Hay que cerrar el mes con un entregable (PDF/Word) que salga del MISMO cuadro, no de un export manual.
- Aplica la regla "el mes nuevo NO borra el anterior".

## Prerequisites

- Un pipeline que ya **capture** el dato crudo y lo deje en un historico lineal
  (`historico.jsonl`), con el crudo archivado por dia (`crudo/<YYYY-MM-DD>/`) para reprocesar sin volver a la fuente.
- Python con `openpyxl`; `matplotlib` solo si el PDF lleva graficas.
- Chrome headless para HTML->PDF: `chrome --headless --disable-gpu --no-sandbox --print-to-pdf=salida.pdf file://entrada.html`.
- Credencial de Drive del dueño del archivo (aqui `/opt/data/secrets/<owner>-drive.json`, refresh por `urllib`).

## Procedure

1. **Un solo historico como fuente de verdad.** El Sheet y el PDF se generan del mismo
   `historico.jsonl`; nunca de una copia intermedia. El cron diario escribe **directo de la
   fuente original** (buzon/API), no del crudo, y con reintentos.
2. **El libro se construye con TODOS los meses** del historico, no solo el mes en curso
   (ver Decisiones #1). Nombra las pestanas con el mes: `2026-09 DATOS`, `2026-09 MATRIZ`, ...
3. **Publica con `files.update`** (multipart, `mimeType=application/vnd.google-apps.spreadsheet`)
   sobre el **mismo file_id**: conserva la URL y el historial de revisiones.
4. **Cron diario** (a hora fija, tras la ventana en que llega el dato): captura -> historico ->
   build -> publish. Debe avisar cuando faltan dias (`AVISO: HUECOS`), no fallar en silencio.
5. **Cron mensual** que arma el PDF del mes cerrado y lo entrega con una linea `MEDIA:<ruta>`
   (modo `no_agent`: el stdout se entrega verbatim). Va en el perfil **dueno del bridge**, no en
   el perfil dueno de los datos — ver Pitfalls.

## Decisiones que no son obvias

1. **No se rota: se acumula.** El contenido del Sheet queda EXACTAMENTE lo que traiga el XLSX,
   asi que la unica forma de conservar meses anteriores es que el XLSX los contenga todos.
2. **Cada mes autocontenido.** Formulas con comillas simples a su propia pestana:
   `'2026-09 DATOS'!$H:$H`. Asi añadir un mes no puede tocar los numeros del anterior.
3. **El cron de cierre va el dia 2, no el 1.** Los informes de origen suelen llegar con +1 dia
   (el del 30 entra el 1); el backfill del dia 2 garantiza el mes completo. Calcula el mes como
   **ultimo dia del mes anterior** (`hoy.replace(day=1) - 1 dia`) para no equivocarte de mes.
4. **El mes vivo primero** en el orden de pestanas.
5. **La pestana del mes nuevo existe vacia** desde el dia 1, sin errores de formula.

## Pitfalls

- **`files.update` reemplaza el contenido completo**: una pestana que no este en el XLSX desaparece.
- **Pestana vacia**: protege las divisiones (cobertura) con `IFERROR` y usa un rango minimo
  `max(n, 2)` al armar rangos tipo `A2:A<n>`.
- **`docker cp` deja `root:root`** y el usuario del contenedor no puede borrar: `chown` con
  `docker exec` **sin** `-u usuario`.
- **Rutas del PDF portables**: resuelve el binario de Chrome y el logo con una lista de candidatos
  + `CHROME_BIN`/`NCL_LOGO`, para que el mismo script corra en el equipo y en el contenedor.
- **`pdfinfo` puede no existir** en el contenedor: verifica con bytes/tamano o Python.
- **Un perfil NO puede entregar a chats ajenos.** La regla real: **cada chat lo entrega el
  perfil al que esta ruteado** en `profile_routes` (no existe un "perfil dueno del bridge").
  `platforms.<p>.enabled: false` **no** lo impide -- helmer entrega a diario con `enabled: false`.
  El mensaje `platform '<p>' not configured/enabled` es el *fallback fallido*: aparece cuando el
  perfil no es dueno de ese chat. Solucion: monta el job de cada destinatario en **su** perfil
  (si el mismo informe va a dos personas: dos jobs, dos perfiles, y **dedup por separado**, o el
  primero que corre deja al segundo en silencio); copia el script a los `scripts/` de ese perfil y
  usa rutas absolutas. El informe al Admin va en `default` porque su chat esta ruteado ahi.
- **`files.create`/`update` en Drive puede dar 403 mudo**: el cuerpo trae la causa real
  (`insufficientParentPermissions` = el token no es dueno de la carpeta). Imprime el cuerpo del
  error, y usa el secret de la cuenta duena, no el del cliente.
- **La hoja de apoyo de los charts se oculta, no se borra** (`sheet_state = 'hidden'`): los charts
  comen valores literales, no formulas, y sin esa hoja salen en blanco.
- **`cron run` (manual) NO valida una entrega**: corre fuera del gateway, asi que un job que SI
  entrega por el scheduler puede responder `Ran now: failed`. Prueba con un schedule temporal
  (`*/2 * * * *`) y lee `cron.scheduler: delivered to ...` en el log del perfil.
- **El adjunto `MEDIA:` en `no_agent` esta probado y funciona**: el stdout se entrega verbatim y la
  linea `MEDIA:<ruta>` produce el adjunto (`delivered ... via live adapter`, con `message_id`).

## Verification

- **Valor de las formulas** (no basta con que el archivo abra): recalcula con
  `soffice --headless --convert-to xlsx --outdir <out> <archivo>` y lee con `openpyxl(..., data_only=True)`.
- **El Sheet REAL**, no tu copia: exportalo y lee sus pestanas
  (`files.export?mimeType=...spreadsheetml.sheet`) -> `load_workbook().sheetnames`.
- **Caso mes vacio** forzando la lista de meses: debe dar 0 errores (`#DIV/0!`, `#REF!`).
- **Paridad de entorno**: el PDF generado en el contenedor debe pesar lo mismo que el local.
