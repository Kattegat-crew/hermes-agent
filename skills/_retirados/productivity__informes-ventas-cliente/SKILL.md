---
name: informes-ventas-cliente
description: "Informes de ventas: Sheet con formato + PDF membreteado."
version: 1.0.0
author: Ragnar
metadata:
  hermes:
    tags: [informes, ventas, sheets, pdf, reports, clientes]
---

# Informes de Ventas de Cliente (Sheet + PDF)

Pipeline de clase para el informe mensual de ventas de un cliente (casino Golden es la
instancia viva): correos fuente → parser → históricos → hoja de Google con formato real →
PDF horizontal membreteado. Cubre reglas de datos, construcción del Sheet, layout del PDF
y el gate de revisión independiente. NO cubre envío de los correos ni las facturas.

## When to Use

- "Arma/actualiza el informe de ventas de <cliente>"
- Re-procesar un mes cerrado y regenerar Sheet y/o PDF
- Auditar un informe existente antes de entregarlo

## Pipeline (instancia viva: /opt/data/workspace/ventas)

1. **Fuente**: correos diarios KASSIUSS (ingresos, pagos, jackpot, neto POR SEDE).
2. **Parser** → `historico.jsonl` (una fila por sede-día). Es el SSOT: Sheet y PDF se
   generan de él, no pueden divergir.
3. **Sheet** con formato (negrita marca, encabezado congelado, gráficas ancladas).
4. **PDF** A4 horizontal con membrete: portada KPIs + consolidada, serie por local,
   totales, matriz día×local.

## Reglas de datos (verificadas 16-sep-2026)

- El **neto se LEE del correo**, no se calcula: `t.get('Neto')`. Si un valor sorprende
  (p.ej. negativos), confirmar el literal en el HTML crudo del correo antes de culpar al
  parser — Golden manda `Neto: $-3,504,382` en días con jackpot+pagos > ingresos y los
  negativos son reales: mostrarlos con signo.
- El neto del mes puede diferir de `ingresos − pagos − jackpot` (~0,015% en Golden):
  es definición del cliente, no error nuestro. Reportarlo como nota, no "arreglarlo".
- KPIs derivados: mejor/peor día deben llevar FECHA y coincidir con el máximo/mínimo de
  la gráfica; cobertura = reportes recibidos / (sedes × días).

## Sheet con formato real

- Sheets API habilitada → escribir con `values.update` y formatear con `batchUpdate`.
- **Adopción por nombre**: en re-procesamientos localizar la hoja existente
  (`q=name=<título> and trashed=false`) y actualizarla — NUNCA acuñar un duplicado
  (bifurca la fuente de verdad). Cotejar el folder leyendo `parents` de vuelta.
- El sheetId real se descubre con `GET spreadsheets/{id}` (no asumas 0). Recetas
  batchUpdate + charts: `references/sheets-formato-y-charts.md`.

## PDF: layout de gráficas matplotlib

- Presupuesto de página: A4 horizontal con márgenes ⇒ ~16,5 cm útiles de alto.
- La leyenda fuera del área (`bbox_to_anchor=(0.5,-0.07)`, ncol=N) consume alto de figura:
  bajar el alto de los ejes en compensación (iterado 7.2→6.1→5.5 in) o la página desborda
  y sobra una hoja en blanco.
- Paleta de N series en líneas cruzadas: tonos separados (azul/cian y amarillo/naranja se
  confundían).

## Gate de verificación y revisión

1. `pdfinfo`: conteo de páginas + `Page size: 841.92 x 594.96 pts (A4)` = horizontal.
2. `pdftoppm -png -r 110` + visión: leyenda sin tapar datos, colores distinguibles,
   eje X termina en el último día con datos, nada cortado.
3. Consistencia: promedio = venta/días; cobertura 100% cuando no hay huecos; KPI
   mejor/peor día = extremos de la gráfica.
4. **Reviewer independiente** (el Admin no acepta "100% verificado" propio): despachar
   un subagente reviewer con rúbrica (visual/fórmulas/construcción), LEER su informe
   completo antes de tocar nada, verificar la premisa de cada hallazgo contra el código,
   aplicar los válidos todos juntos y re-verificar. Premisas falsas documentadas:
   anchor que extiende el rango de impresión, backfill de un solo día, leyenda vacía.

## Pitfalls

- No dar por bueno un PDF por exit 0: el pipe `| tail` enmascara y el overflow de página
  no falla — se detecta con pdfinfo/pdftoppm.
- Correos con sedes homónimas o variantes de nombre: normalizar el nombre de sede en el
  parser (mismo local escrito distinto = fila duplicada en la matriz).
- Si el correo del día no llegó, NO rellenar con cero silencioso: marcar hueco y avisar.

## Verification

- pdfinfo (páginas + tamaño), pdftoppm + visión por página, y los 3 chequeos de
  consistencia del gate antes de declarar entregado.
- El PDF se adjunta con MEDIA: (preferencia de entrega del Admin) junto al link del Sheet.

## Skills relacionadas

`pdf-deliverables` y `google-drive-sheets-ops` cubren entregables PDF y mecanismos Drive
por separado; ambas son user-owned (no editables aquí) — si esta skill contradice algo,
mandar `hermes curator adopt <nombre>` y reconciliar.
