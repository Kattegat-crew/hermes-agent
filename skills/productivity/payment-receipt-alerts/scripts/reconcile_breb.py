#!/usr/bin/env python3
"""Conciliación y recuperación autónoma de pagos Bre-B (BBVA) en Google Sheets.

Compara las notificaciones de pago recibidas en Gmail (de notificacionesBreB@bbva.com)
contra las filas registradas en las hojas de cálculo de Lucky Brothers y Golden Game.
Detecta pagos caídos por cortes en ActivePieces o errores de hoja, sanea filas corruptas
e inyecta de forma idempotente los pagos faltantes ordenados cronológicamente.

Uso:
  python3 reconcile_breb.py [--tenant golden|lucky|all] [--since YYYY/MM/DD] [--month YYYY-MM] [--apply]
  Default: --tenant all --dry-run (modo seguro de auditoría)
"""
import argparse
import base64
import csv
import html as ihtml
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

COL = timezone(timedelta(hours=-5))

TENANTS = {
    "lucky": {
        "name": "Lucky Brothers",
        "gmail_secret": "/opt/data/secrets/lucky-gmail.json",
        "drive_secret": "/opt/data/secrets/lucky-drive.json",
        "spreadsheet_id": "1bAcrcBjddAAqxo8V3xnwmOElk_9bAay5G-w1ZREUfGo",
    },
    "golden": {
        "name": "Golden Game",
        "gmail_secret": "/opt/data/secrets/golden-gmail.json",
        "drive_secret": "/opt/data/secrets/golden-drive.json",
        "spreadsheet_id": "1j0vsPs4R4owvm_gisidizO0j0xckeZpK4z-Mev2xYu0",
    },
}

FECHA_PATTERN = re.compile(r"^\d{4}/\d{2}/\d{2} \d{2}:\d{2}$")


def get_access_token(secret_path):
    if not os.path.exists(secret_path):
        raise FileNotFoundError(f"Archivo de credenciales no encontrado: {secret_path}")
    with open(secret_path, "r", encoding="utf-8") as f:
        sec = json.load(f)
    body = urllib.parse.urlencode({
        "client_id": sec["client_id"],
        "client_secret": sec["client_secret"],
        "refresh_token": sec["refresh_token"],
        "grant_type": "refresh_token",
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://oauth2.googleapis.com/token",
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))["access_token"]


def http_get(url, token, timeout=30, retries=5):
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"}, method="GET")
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code in (403, 429, 500, 502, 503) and i < retries - 1:
                wait_sec = min(60, 2 ** i * 3)
                time.sleep(wait_sec)
                continue
            raise
        except Exception:
            if i == retries - 1:
                raise
            time.sleep(2 * (i + 1))
    raise RuntimeError("Petición HTTP fallida tras reintentos")


def list_gmail_messages(token, query):
    msg_ids = []
    page = None
    while True:
        params = {"q": query, "maxResults": "500"}
        if page:
            params["pageToken"] = page
        url = f"https://gmail.googleapis.com/gmail/v1/users/me/messages?{urllib.parse.urlencode(params)}"
        res = json.loads(http_get(url, token).decode("utf-8"))
        msg_ids.extend([m["id"] for m in res.get("messages", [])])
        page = res.get("nextPageToken")
        if not page:
            break
    return msg_ids


def walk_parts(payload):
    parts_out = []

    def rec(part):
        mt = part.get("mimeType", "")
        body = part.get("body", {})
        data = body.get("data")
        if data and mt in ("text/html", "text/plain"):
            parts_out.append((mt, data))
        for child in part.get("parts", []) or []:
            rec(child)

    rec(payload)
    return parts_out


def strip_html(html_str):
    t = str(html_str)
    t = re.sub(r"<style[\s\S]*?</style>", " ", t, flags=re.I)
    t = re.sub(r"<script[\s\S]*?</script>", " ", t, flags=re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    t = ihtml.unescape(t)
    t = re.sub(r"&[a-z]+;", " ", t, flags=re.I)
    return t


def b64_decode(data_str):
    padding = "=" * (-len(data_str) % 4)
    return base64.urlsafe_b64decode(data_str + padding).decode("utf-8", "replace")


def parse_gmail_message(full_msg):
    payload = full_msg.get("payload", {})
    parts = walk_parts(payload)
    html_txt = ""
    plain_txt = ""
    for mt, d in parts:
        try:
            txt = b64_decode(d)
        except Exception:
            continue
        if mt == "text/html" and len(txt) >= 20 and not html_txt:
            html_txt = txt
        if mt == "text/plain" and len(txt) >= 20 and not plain_txt:
            plain_txt = txt

    if html_txt and len(html_txt) >= 20:
        raw = strip_html(html_txt)
    elif plain_txt and len(plain_txt) >= 20:
        raw = plain_txt
    else:
        raw = full_msg.get("snippet", "")

    text = re.sub(r"\s+", " ", str(raw))

    def pick(rx):
        m = re.search(rx, text, flags=re.I)
        return m.group(1).strip() if m else "N/D"

    return {
        "fecha": pick(r"Fecha y hora\s+(.+?)\s+Valor recibido"),
        "valor": pick(r"Valor recibido\s+([^A-Za-z]+?)\s+Persona"),
        "remitente": pick(r"Persona que env[ií]a\s+(.+?)\s+Tipo de llave"),
        "cuenta": pick(r"Cuenta destino\s+(\*+\d+)"),
        "codigo": pick(r"C[oó]digo de operaci[oó]n\s+(\d+)"),
    }


def export_sheet_csv(token, spreadsheet_id):
    url = f"https://www.googleapis.com/drive/v3/files/{spreadsheet_id}/export?mimeType=text%2Fcsv"
    return http_get(url, token, timeout=60).decode("utf-8")


def patch_sheet_csv(token, spreadsheet_id, csv_text):
    url = f"https://www.googleapis.com/upload/drive/v3/files/{spreadsheet_id}?uploadType=media"
    req = urllib.request.Request(
        url,
        data=csv_text.encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "text/csv; charset=utf-8",
        },
        method="PATCH",
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def reconcile_tenant(tenant_key, cfg, query, cache_dir, apply_changes=False):
    print(f"\n==================================================")
    print(f"Conciliando: {cfg['name']} ({tenant_key.upper()})")
    print(f"==================================================")

    gmail_token = get_access_token(cfg["gmail_secret"])
    drive_token = get_access_token(cfg["drive_secret"])

    # 1. Obtener y parsear estado actual del Sheet
    raw_csv = export_sheet_csv(drive_token, cfg["spreadsheet_id"])
    reader = list(csv.reader(io.StringIO(raw_csv)))
    if not reader:
        print(f"[{tenant_key}] ERROR: La hoja de cálculo está vacía.")
        return

    header = reader[0]
    raw_rows = reader[1:]

    existing_codes = set()
    clean_rows = []
    corrupt_rows = 0

    for r in raw_rows:
        if len(r) >= 5 and r[4].strip() and r[0].strip() and r[1].strip():
            code = r[4].strip()
            if code not in existing_codes:
                existing_codes.add(code)
                clean_rows.append(r)
        else:
            corrupt_rows += 1

    print(f"[{tenant_key}] Filas actuales en Sheet: {len(raw_rows)} (Válidas: {len(clean_rows)}, Corruptas/Vacías detectadas: {corrupt_rows})")

    # 2. Consultar mensajes en Gmail
    msg_ids = list_gmail_messages(gmail_token, query)
    print(f"[{tenant_key}] Mensajes encontrados en Gmail con filtro '{query}': {len(msg_ids)}")

    # 3. Manejo de caché
    os.makedirs(cache_dir, exist_ok=True)
    cache_path = os.path.join(cache_dir, f"breb_cache_{tenant_key}.json")
    cache = {}
    if os.path.exists(cache_path):
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                cache = json.load(f)
        except Exception:
            cache = {}

    missing_payments = []
    seen_in_batch = set()
    cache_dirty = False

    for idx, mid in enumerate(msg_ids):
        if mid in cache:
            item = cache[mid]
        else:
            time.sleep(0.15)
            url = f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{mid}?format=full&fields=payload,snippet"
            full_msg = json.loads(http_get(url, gmail_token, timeout=45).decode("utf-8"))
            item = parse_gmail_message(full_msg)
            cache[mid] = item
            cache_dirty = True
            if (idx + 1) % 50 == 0:
                with open(cache_path, "w", encoding="utf-8") as f:
                    json.dump(cache, f, ensure_ascii=False)

        if "N/D" in item.values() or not FECHA_PATTERN.match(item["fecha"]):
            continue

        code = item["codigo"]
        if code in existing_codes or code in seen_in_batch:
            continue

        seen_in_batch.add(code)
        missing_payments.append([
            item["fecha"],
            item["valor"],
            item["remitente"],
            item["cuenta"],
            item["codigo"],
        ])

    if cache_dirty:
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False)

    print(f"[{tenant_key}] Pagos huérfanos / faltantes identificados: {len(missing_payments)}")

    if missing_payments:
        print(f"\n--- Muestra de pagos faltantes ({tenant_key.upper()}) ---")
        for row in missing_payments[:10]:
            print(f"  {row[0]} | {row[1]:>14} | {row[2][:25]:<25} | Cod: {row[4]}")
        if len(missing_payments) > 10:
            print(f"  ... y {len(missing_payments) - 10} pagos adicionales.")

    # 4. Aplicar cambios si se solicitó
    if apply_changes:
        if not missing_payments and corrupt_rows == 0:
            print(f"\n[{tenant_key}] ✅ Hoja 100% al día y limpia. Nada que aplicar.")
            return

        merged_rows = clean_rows + missing_payments
        merged_rows.sort(key=lambda x: x[0])

        out = io.StringIO()
        writer = csv.writer(out)
        writer.writerow(header)
        writer.writerows(merged_rows)

        patch_sheet_csv(drive_token, cfg["spreadsheet_id"], out.getvalue())
        print(f"\n[{tenant_key}] 🚀 APLICADO CON ÉXITO: {len(missing_payments)} pagos inyectados, {corrupt_rows} filas corruptas purgadas.")
        print(f"[{tenant_key}] Total de filas actualizadas en Google Sheet: {len(merged_rows)}")
    else:
        if missing_payments or corrupt_rows > 0:
            print(f"\n[{tenant_key}] ℹ️ Modo DRY-RUN. Ejecutá con --apply para escribir estos {len(missing_payments)} pagos y sanear la tabla.")
        else:
            print(f"\n[{tenant_key}] ✅ Hoja 100% cuadrada. No requiere cambios.")


def main():
    parser = argparse.ArgumentParser(description="Conciliador autónomo de pagos Bre-B")
    parser.add_argument("--tenant", choices=["golden", "lucky", "all"], default="all", help="Empresa a conciliar")
    parser.add_argument("--since", help="Fecha inicial en formato YYYY/MM/DD (default: hace 30 días)")
    parser.add_argument("--month", help="Mes específico YYYY-MM (ej: 2026-10)")
    parser.add_argument("--cache-dir", default="/root/breb-reports", help="Directorio para almacenamiento de caché")
    parser.add_argument("--apply", action="store_true", help="Aplica la inyección y saneamiento en Google Sheets")
    args = parser.parse_args()

    now = datetime.now(COL)
    if args.month:
        try:
            y, m = map(int, args.month.split("-"))
            start_date = f"{y:04d}/{m:02d}/01"
            if m == 12:
                end_date = f"{y+1:04d}/01/01"
            else:
                end_date = f"{y:04d}/{m+1:02d}/01"
            query = f"from:notificacionesBreB@bbva.com after:{start_date} before:{end_date}"
        except Exception:
            print("Formato inválido de --month. Debe ser YYYY-MM.")
            sys.exit(1)
    elif args.since:
        query = f"from:notificacionesBreB@bbva.com after:{args.since}"
    else:
        # Por defecto, desde el 1 del mes anterior para cubrir cierre y mes en curso
        first_current = now.replace(day=1)
        prev_month = (first_current - timedelta(days=1)).replace(day=1)
        since_str = prev_month.strftime("%Y/%m/%d")
        query = f"from:notificacionesBreB@bbva.com after:{since_str}"

    targets = [args.tenant] if args.tenant != "all" else ["golden", "lucky"]
    for t in targets:
        reconcile_tenant(t, TENANTS[t], query, args.cache_dir, apply_changes=args.apply)


if __name__ == "__main__":
    main()
