#!/usr/bin/env python3
"""
parse_gf.py — Parser de Google Flights (curl-scraped HTML) para extraer itinerarios.
Verificado 2026-08-23 con BOG->MEL, BOG->HNL, BOG->IAH->HNL.

Uso:
    python3 parse_gf.py gf_boghnl_27.html            # modo USD (precios $1,373)
    python3 parse_gf.py gf_boghnl_27_co.html --cop   # modo COP (precios 5.657.720)

Salida por tarjeta (dedupe por precio+itinerario):
    $783 | 1 escala | BOG 01:30 -> HNL 13:08 | conecta IAH George Bush | 13h53m en vuelo | lay ~2h45m

Reglas internas (estructura observada ago 2026, cambia con el tiempo):
- Elegir el bloque AF_initDataCallback MÁS GRANDE (>20000 chars) que contenga la ciudad:
  el bloque "header" (~1.5KB) tiene la ciudad pero NO tarjetas.
- Precios: `[[null, NNN]]` en el ANCESTRO de la tarjeta, no al mismo nivel que las legs.
- Leg: list con strings 'X International Airport'; o[3] dep code, o[4] dep name, o[5] arr name,
  o[6] arr code, o[8] [h,m] dep, o[10] [h,m] arr, o[11] duracion min.
"""
import re
import json
import sys

def load(fname):
    html = open(fname, encoding='utf-8', errors='replace').read()
    blocks = re.findall(r'AF_initDataCallback\((\{.*?\})\)', html, re.S)
    best = None
    for b in blocks:
        m = re.search(r"data:(\[.*\])(?:,\s*sideChannel|\))", b, re.S)
        if not m:
            continue
        try:
            d = json.loads(m.group(1))
            s = json.dumps(d)
            if 'Honolulu' in s and len(s) > 20000:
                if best is None or len(s) > len(best[0]):
                    best = (s, d)
        except Exception:
            pass
    return best[1] if best else None

def is_leg(o):
    return isinstance(o, list) and len(o) >= 12 and any(
        isinstance(x, str) and 'airport' in x.lower() for x in o)

def parse_leg(o):
    dep_c = o[3] if len(o) > 3 else None
    dep_n = o[4] if len(o) > 4 else None
    arr_n = o[5] if len(o) > 5 else None
    arr_c = o[6] if len(o) > 6 else None
    dep_t = o[8] if len(o) > 8 and isinstance(o[8], list) and len(o[8]) == 2 else None
    arr_t = o[10] if len(o) > 10 and isinstance(o[10], list) and len(o[10]) == 2 else None
    dur = o[11] if len(o) > 11 and isinstance(o[11], (int, float)) else None
    air = None
    if len(o) > 1:
        a = o[1]
        if isinstance(a, list) and a and isinstance(a[0], str):
            air = a[0]
        elif isinstance(a, str):
            air = a
    return (dep_c, dep_n, arr_n, arr_c, dep_t, arr_t, dur, air)

def find_cards(data):
    """Lista de (precio, [legs...]) en orden de árbol, agrupadas por precio de ancestro."""
    card = [None]

    def price_of(o):
        s = json.dumps(o)
        m = re.search(r'\[(?:null|None),\s*(\d{3,5})\]', s)
        return int(m.group(1)) if m else None

    collected = []

    def rec(o):
        saved = card[0]
        p = price_of(o)
        if p is not None and 300 < p < 8000:
            card[0] = p
        if isinstance(o, list):
            legs = []
            for v in o:
                if is_leg(v):
                    legs.append(parse_leg(v))
                elif isinstance(v, list):
                    for x in v:
                        if is_leg(x):
                            legs.append(parse_leg(x))
            if legs and card[0] is not None:
                collected.append((card[0], legs))
                for v in o:
                    if is_leg(v) or (isinstance(v, list) and any(is_leg(x) for x in v)):
                        continue
                    if isinstance(v, (list, dict)):
                        rec(v)
            else:
                for v in o:
                    if isinstance(v, (list, dict)):
                        rec(v)
        elif isinstance(o, dict):
            for v in o.values():
                if isinstance(v, (list, dict)):
                    rec(v)
        card[0] = saved

    rec(data)
    return collected

def chain(legs):
    """Cadena contigua: empieza en ORIG termina en DEST. Devuelve la más corta o None."""
    best = None
    for start in range(len(legs)):
        seq = [legs[start]]
        cur = legs[start]
        for nxt in legs[start + 1:]:
            if nxt[0] == cur[3] and (nxt[0] != nxt[3]):
                seq.append(nxt)
                cur = nxt
        if seq[0][0] == 'BOG' and seq[-1][3] == 'HNL':
            if best is None or len(seq) < len(best):
                best = seq
    return best

def fmt_t(x):
    if isinstance(x, list) and len(x) == 2 and isinstance(x[0], (int, float)):
        return f"{int(x[0]):02d}:{int(x[1]):02d}"
    return "?"

def clean(n):
    return re.sub(r' (International|Aeropuerto|International Airport)$', '', str(n or ''))

def main():
    cop = '--cop' in sys.argv
    files = [a for a in sys.argv[1:] if not a.startswith('--')]
    for fname in files:
        data = load(fname)
        print(f"=== {fname} ===")
        if not data:
            print("  no data"); continue
        rows = []
        seen = set()
        for price, legs in find_cards(data):
            c = chain(legs)
            if not c:
                continue
            key = (price, tuple((l[0], l[3], l[6]) for l in c))
            if key in seen:
                continue
            seen.add(key)
            rows.append((price, c))
        rows.sort(key=lambda x: x[0])
        for price, legs in rows:
            stops = len(legs) - 1
            conns = " -> ".join(f"{l[3]} {clean(l[2])}".strip() for l in legs[:-1])
            tot = sum((l[6] or 0) for l in legs)
            lay = None
            try:
                a = legs[0][5]; b = legs[1][4]
                if a and b and isinstance(a[0], (int, float)) and isinstance(b[0], (int, float)):
                    lay = (b[0] * 60 + b[1]) - (a[0] * 60 + a[1])
                    if lay < 0:
                        lay += 1440
            except Exception:
                lay = None
            price_str = f"${price:,}" if not cop else f"${price:,} COP"
            first = f"{legs[0][0]} {fmt_t(legs[0][4])} -> {legs[-1][3]} {fmt_t(legs[-1][5])}"
            extra = f" | lay {lay // 60}h{lay % 60:02d}m" if lay else ""
            print(f"  {price_str} | {stops} escala(s) | {first} | conecta {conns} | {tot // 60}h{tot % 60:02d}m volando{extra}")
        print()

if __name__ == '__main__':
    main()