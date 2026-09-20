# Caso real: vigilante GTIN falló silenciosamente (2026-08-18)

## Contexto
Cron `watch-gtin-exemption-ps3058` (job 81d2cd95ee8f, `no_agent=True`, script `/opt/data/scripts/watch_exemption.py`, cada 60m × 12) que re-valida un preview de listing SP-API Amazon y avisa cuando la exención GTIN propaga (status → VALID).

## Síntoma
- El usuario preguntó "¿qué pasó con ese cron?" — nunca llegó mensaje del vigilante.
- `cronjob list` mostraba `last_run_at: 18:25`, `last_status: ok`, `repeat: 1/12` — parecía todo bien.
- El registro en `/opt/data/cron/output/81d2cd95ee8f/2026-08-18_18-25-31.md` revelaba: `⚠️ No se pudo parsear respuesta: Expecting value: line 1 column 1 (char 0)`.

## Causa raíz
El script viejo hacía:
```python
idx = raw.find("{", raw.find("HTTP"))
d = json.loads(raw[idx:])
```
Cuando el subprocess del preview fallaba (timeout/red) y devolvía stdout vacío, `raw.find` daba -1, `raw[-1:]` era `""`, y `json.loads("")` crasheaba. El except imprimía el error por stdout → **en no_agent, stdout no vacío = mensaje al usuario** → el usuario recibió basura técnica en vez de silencio (o el mensaje se perdió y solo quedó en el registro).

## Fix aplicado (v2 de watch_exemption.py)
1. **Reintentos**: 3 intentos con backoff (sleep 5×attempt) ante timeout/red — un fallo transitorio no mata el run.
2. **Parseo robusto**: `start = raw.find("{")`; si `start == -1` → registrar como fallo, reintentar; si no, `json.loads(raw[start:])`.
3. **Silencio en fallos técnicos**: tras agotar reintentos, escribe en `/opt/data/cron/output/<job_id>/last_error.log` y `sys.exit(0)` sin print — NO spamea al chat.
4. **Print SOLO en cambio real**: status == VALID, o INVALID con issue codes ≠ {90220}.

## Verificación
- `python3 /opt/data/scripts/watch_exemption.py` → sin salida, exit 0 (silencio esperado, exención aún no propaga).
- El preview manual `create_listing.py --sku PS-3058 --preview` funcionaba bien (HTTP 200, INVALID con 90220) — el fallo fue del subprocess, no de la API.

## Lección general
En cron `no_agent`, **stdout = mensaje**. Un watchdog jamás debe imprimir fallos técnicos transitorios; los registra en archivo y espera al siguiente tick. Solo imprime cambios de estado reales.
