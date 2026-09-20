#!/usr/bin/env python3
"""
validate_listing_limits.py — Valida límites de campos de listings Amazon en un xlsx.

Uso:
    python3 validate_listing_limits.py /ruta/sheet.xlsx
    python3 validate_listing_limits.py /ruta/sheet.xlsx --limit generic_keywords 250 --bytes

Revisa por defecto: item_name (200), bullet_point1-5 (500), product_description (2000),
generic_keywords (250 bytes). Reporta por fila OK/EXCEDE.
Los nombres de columna se buscan por encabezado (funciona con cualquier sheet tipo
LISTINGS-SNUFFLE-MATS-AU.xlsx).
"""
import argparse
import openpyxl

DEFAULTS = {
    "item_name": 200,
    "bullet_point1": 500,
    "bullet_point2": 500,
    "bullet_point3": 500,
    "bullet_point4": 500,
    "bullet_point5": 500,
    "product_description": 2000,
    "generic_keywords": (250, "bytes"),
}


def main():
    ap = argparse.ArgumentParser(description="Valida límites de campos Amazon en xlsx")
    ap.add_argument("xlsx")
    ap.add_argument("--sheet", default=None)
    ap.add_argument("--bytes", action="store_true", help="Contar generic_keywords en bytes")
    args = ap.parse_args()

    wb = openpyxl.load_workbook(args.xlsx)
    ws = wb[args.sheet] if args.sheet else wb[wb.sheetnames[0]]

    # Mapa encabezado -> columna
    hdr = {}
    for c in range(1, ws.max_column + 1):
        v = ws.cell(row=1, column=c).value
        if v:
            hdr[v] = c

    limits = dict(DEFAULTS)
    if args.bytes:
        limits["generic_keywords"] = (250, "bytes")

    print(f"Hoja: {ws.title} | Filas data: {ws.max_row - 1}")
    all_ok = True
    for r in range(2, ws.max_row + 1):
        sku = ws.cell(row=r, column=2).value or f"Fila {r}"
        row_ok = True
        for field, lim in limits.items():
            col = hdr.get(field)
            if col is None:
                continue
            v = ws.cell(row=r, column=col).value or ""
            n = len(v.encode("utf-8")) if (isinstance(lim, tuple) or field == "generic_keywords" and args.bytes) else len(v)
            maxv = lim[0] if isinstance(lim, tuple) else lim
            status = "OK" if n <= maxv else f"EXCEDE ({n}/{maxv})"
            if status != "OK":
                all_ok = False
                row_ok = False
                print(f"  {sku} | {field}: {n}/{maxv} {status}")
        if row_ok:
            print(f"  {sku} | TODO OK")

    print("\nRESULTADO:", "TODO OK ✅" if all_ok else "HAY EXCEDIDOS ❌ — corregir antes de subir")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
