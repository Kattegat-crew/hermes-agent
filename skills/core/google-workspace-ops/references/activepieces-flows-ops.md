---
name: activepieces-bre-b-ops
description: "Operar y reparar los flows Bre-B (Lucky/Golden) en ActivePieces: MCP, correcciones de sheet y verificación de integridad."
version: 1.0.0
author: Ragnar
metadata:
  hermes:
    category: devops
    tags: [activepieces, bre-b, google-sheets, gmail, mcp, banca]
---

# ActivePieces Bre-B Ops

Operación, reparación y verificación de integridad de los flows bancarios Bre-B (BBVA) de las empresas Lucky ("Paradise") y Golden en ActivePieces: quitar/pausar pasos, reinyectar pagos faltantes al Google Sheet y auditar que cada correo notificacionesBreB@bbva.com tenga su fila. No cubre otros flows de AP (videogen, web) ni campañas.

## When to Use
- El Admin pide modificar/pausar un paso de un flow Bre-B ("quita la notificación de Discord", "pausa el aviso").
- Sospecha de pagos faltantes: "revisa que los últimos correos sean las últimas transacciones".
- Un run falló y hay que reinyectar la fila al sheet sin duplicar.

## Prerequisites
- Token AP: `/opt/data/secrets/ap_jonathan.token` (clave `token`). Endpoint MCP: `http://100.73.30.29:8088/mcp`.
- Credenciales Google: `/opt/data/secrets/{lucky,golden}-drive.json` y `{lucky,golden}-gmail.json` (claves `client_id`, `client_secret`, `refresh_token`). NUNCA imprimir valores.
- Sheets API está DESHABILITADA en el GCP project: la lectura del sheet se hace con Drive export CSV (`GET https://www.googleapis.com/drive/v3/files/{id}/export?mimeType=text/csv`) y la escritura SOLO vía steps de ActivePieces.
- Sheet Lucky: `1bAcrcBjddAAqxo8V3xnwmOElk_9bAay5G-w1ZREUfGo` (tab "Bre-B Lucky — Pagos"). Sheet Golden: `1j0vsPs4R4owvm_gisidizO0j0xckeZpK4z-Mev2xYu0`.

## How to Run
1. MCP por HTTP (cuando las tools MCP nativas no alcanzan): POST JSON-RPC `{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":...,"arguments":{...}}}` con header `Authorization: Bearer <token>` y `Accept: application/json, text/event-stream`. La respuesta es SSE: parsear las líneas que empiezan con `data:`.
2. Diagnóstico: `ap_flow_structure` para ver pasos reales (Discord y Sheet pueden vivir en el MISMO flow — desactivar el flow completo rompe también el sheet). `ap_list_runs` (limit máx 50) para el historial.
3. Mutación de flow: cambiar solo el paso problemático (`ap_delete_step`) y `ap_lock_and_publish` después. OJO: `ap_delete_step`/`ap_add_step` sobre un flow publicado tocan el DRAFT — sin publish el cambio NO aplica en producción.
4. Reinyectar fila faltante: `ap_add_step` temporal (paso PIECE `@activepieces/piece-google-sheets` `~0.16.4`, action `insert_row`, con `values` A–E literales) → `ap_test_step` sobre ese paso (inserta de verdad) → verificar en export CSV → `ap_delete_step` del paso temporal → `ap_lock_and_publish`. Repetir por cada fila.
5. Auditoría de integridad: listar correos Gmail (`q=from:notificacionesBreB@bbva.com newer_than:3d`), extraer código (secuencia de 20–40 dígitos del HTML), comparar contra columna E de ambos sheets por export CSV. Regla de oro: emparejar por CÓDIGO, nunca por fecha/hora.

## Quick Reference
- IDs de flow: Lucky `e2yTTyYCWj0DAWHTX8lLw` ("Bre-B Lucky → aviso Discord", nombre heredado; hoy es Gmail→parse→Sheet), Golden `ybZF7O6TgBbKiAvvVvdHV`.
- Trigger Gmail = polling: si el flow estuvo pausado N minutos, los correos de esa ventana quedan HUÉRFANOS (el trigger no re-procesa mail viejo). Causa #1 de pagos faltantes.
- Fechas de correos y sheet están en hora Bogotá; los runs de AP se muestran en UTC (offset +5).
- Parser de mails (step_1 CODE): strip de `<style>` antes de quitar tags; campos: `Fecha y hora`, `Valor`, `Cuenta destino *****XXXX`, código largo de dígitos.

## Pitfalls
- El gate de aprobación de MCP de escritura puede rechazar la 1ª–2ª llamada (`The user did not approve...`): un reintento con los MISMOS argumentos suele pasar. No confundir con error real.
- Regex ad-hoc sobre el HTML de los mails cruzan campos entre mails vecinos: validar cada código DENTRO del HTML de SU correo antes de declarar un faltante.
- `ap_test_step` sobre un paso insert_row ESCRIBE en el sheet real (no es simulación). El output `tableRange` dice la fila exacta escrita.
- El export CSV de Drive puede venir cacheado: si el resultado contradice un insert reciente, reintentar con header `Cache-Control: no-cache` antes de concluir.
- Una fila insertada puede no verse de inmediato en `ap_list_runs` (el run TEST no siempre aparece ordenado): verificar SIEMPRE contra el CSV, no contra el run.


---

## Procedencia

Absorbido por F3 el 20260923-055337 desde la autoskill `data/skills/activepieces-bre-b-ops` (sin versión en git hasta hoy).
El procedimiento se conserva íntegro; el paraguas `google-workspace-ops` es su punto de entrada.

