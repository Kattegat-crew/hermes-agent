#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F6 · Lote 0 — propuesta firmable (NO muta nada)
==============================================

Genera el expediente del lote 0 del plan de consolidación: los pares duplicados
POR NOMBRE. Para cada par mide similitud real (misma métrica oficial), tamaño,
hash y diferencias de contenido, y propone la dirección de fusión con su
justificación. El lote NO se ejecuta: exige el candado de F6 (2 revisiones
limpias del curador + firma del CTO) y se aplica con ledger de hash.

USO
  python3 scripts/f6_lote0_propuesta.py            # genera expediente
  python3 scripts/f6_lote0_propuesta.py --listar   # solo imprime
"""
import argparse
import difflib
import hashlib
import json
import re
import time
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

REPO = Path('/root/hermes-agent')
CANON = REPO / 'skills'
SALIDA = REPO / 'data' / 'state' / 'f6_lote0.json'
DOC = REPO / 'docs' / 'skills' / 'F6-LOTE0-PROPUESTA.md'

# pares confirmados por nombre (plan Rev.6, F6 · lote 0)
PARES = [
    ('productivity/oauth-multi-tenant-integration',
     'productivity/oauth-multi-tenant-integrations'),
    ('specialists/hermes-internal/brain-graph-operations',
     'specialists/hermes-internal/brain-graph-ops'),
    ('specialists/marketing/analytics',
     'specialists/marketing/analytics-tracking'),
    ('specialists/data-vector/pinecone',
     'specialists/data-vector/pinecone-research'),
]
# lote 4 del plan: los tres homónimos del caso ejemplar
LOTE4 = ['creative/hermes-multiprofile-gateway-ops']


def frontmatter(txt):
    """Igual que la métrica oficial: nombre + descripción + cuerpo."""
    nombre, desc = '', ''
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n', txt, re.S)
    if m:
        for linea in m.group(1).splitlines():
            mm = re.match(r'^\s*(name|title)\s*:\s*(.+)$', linea)
            if mm and not nombre:
                nombre = mm.group(2).strip().strip('\'"')
            md = re.match(r'^\s*description\s*:\s*(.+)$', linea)
            if md and not desc:
                desc = md.group(1).strip().strip('\'"')
    return nombre, desc


def lee(rel):
    p = CANON / rel / 'SKILL.md'
    if not p.is_file():
        return None
    txt = p.read_text(encoding='utf-8', errors='ignore')
    nombre, desc = frontmatter(txt)
    return {'ruta': rel, 'ruta_abs': str(p), 'bytes': len(txt),
            'lineas': len(txt.splitlines()),
            'sha256_16': hashlib.sha256(txt.encode()).hexdigest()[:16],
            'txt': txt,
            'doc': '%s %s %s' % (nombre or rel.split('/')[-1], desc, txt)}


def metrica_oficial():
    """Índice par->similitud de la métrica oficial (fuente única, R11).

    Recalcularla aquí con un vectorizador de dos documentos daría OTRA cifra: el
    TF-IDF depende del corpus. El lote 0 lee la medición publicada.
    """
    f = REPO / 'data' / 'state' / 'f6_metrica.json'
    if not f.is_file():
        return {}
    try:
        m = json.loads(f.read_text(encoding='utf-8'))
    except Exception:
        return {}
    return {tuple(sorted([p['a'], p['b']])): p['similitud']
            for p in (m.get('pares_todos') or [])}


def diff_resumen(a, b):
    da = a.splitlines()
    db = b.splitlines()
    sm = difflib.SequenceMatcher(None, da, db)
    solo_a = solo_b = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag in ('replace', 'delete'):
            solo_a += i2 - i1
        if tag in ('replace', 'insert'):
            solo_b += j2 - j1
    return {'lineas_solo_en_a': solo_a, 'lineas_solo_en_b': solo_b,
            'ratio_similitud_texto': round(sm.ratio(), 4)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--listar', action='store_true')
    a = ap.parse_args()

    global OFICIAL
    OFICIAL = metrica_oficial()
    informe = {'ts': time.strftime('%Y-%m-%dT%H:%M:%S%z'),
               'fase': 'F6', 'lote': 0,
               'muta': False,
               'candado': 'exige 2 revisiones limpias + firma del CTO (R8)',
               'pares': [], 'lote4': []}

    for relA, relB in PARES:
        A, B = lee(relA), lee(relB)
        item = {'a': relA, 'b': relB}
        if not A or not B:
            item['estado'] = 'falta una de las dos: %s' % ('A' if not A else 'B')
            informe['pares'].append(item)
            continue
        s = OFICIAL.get(tuple(sorted([relA, relB])))
        d = diff_resumen(A['txt'], B['txt'])
        identico = A['sha256_16'] == B['sha256_16']
        # dirección propuesta: absorbe el que aporta contenido al que ya es clase
        mas_largo = 'a' if A['bytes'] > B['bytes'] else 'b'
        item.update({
            'similitud_oficial': s,
            'pasa_umbral_oficial': bool(s is not None and s >= 0.45),
            'metodo_similitud': 'TF-IDF coseno sobre nombre + descripcion + cuerpo (metodo de la metrica oficial)',
            'identicos_por_hash': identico,
            'a_meta': {k: A[k] for k in ('bytes', 'lineas', 'sha256_16')},
            'b_meta': {k: B[k] for k in ('bytes', 'lineas', 'sha256_16')},
            'diff': d,
            'absorbe': ('el de nombre plural (clase)' if 'integration' in relA
                        else 'el de cuerpo más rico'),
            'propuesta': ('Contenido idéntico: archivar el duplicado y dejar el '
                          'nombre canónico' if identico else
                          'Integrar las %d líneas exclusivas del más pobre en el '
                          'que absorbe, y archivar el absorbido' %
                          (d['lineas_solo_en_b'] if mas_largo == 'a' else d['lineas_solo_en_a'])),
            'riesgo': 'nulo' if identico else 'bajo',
        })
        informe['pares'].append(item)
        print('%-62s sim=%s  identicos=%s  soloA=%d soloB=%d'
              % (relA.split('/')[-1] + ' <-> ' + relB.split('/')[-1],
                 ('%.4f' % s) if s is not None else 'bajo umbral',
                 identico, d['lineas_solo_en_a'], d['lineas_solo_en_b']))

    for rel in LOTE4:
        A = lee(rel)
        informe['lote4'].append({'skill': rel,
                                 'existe': bool(A),
                                 'meta': ({k: A[k] for k in ('bytes', 'lineas', 'sha256_16')}
                                          if A else None)})
        if A:
            print('lote4 %-50s %d lineas' % (rel, A['lineas']))

    if not a.listar:
        SALIDA.parent.mkdir(parents=True, exist_ok=True)
        SALIDA.write_text(json.dumps(informe, ensure_ascii=False, indent=1), encoding='utf-8')
        L = ['# F6 · Lote 0 — pares duplicados por nombre (propuesta)', '',
             '| Campo | Valor |', '|---|---|',
             '| Motivo | F6 del plan Rev. 6: la fusión trivial de arranque |',
             '| Fecha | %s |' % informe['ts'],
             '| Métrica | `docs/skills/METRICA-CONSOLIDACION.md` (TF-IDF 0,45) |',
             '| **Estado** | %s |' % ('**EJECUTADA** — ver `docs/skills/F6-LOTE0-EJECUCION.md`' if (REPO / 'data' / 'state' / 'f6_lote0_ledger.jsonl').is_file() else '**PROPUESTA — no ejecutada**'),
             '| Candado | %s |' % informe['candado'], '',
             '**Nada de este documento se ha aplicado.** La fusión exige el candado de',
             'F6 (dos revisiones limpias del curador) y firma del CTO lote por lote.',
             '', '## Los pares', '',
             '| A | B | Similitud | Idénticos | Líneas solo en A | Líneas solo en B | Riesgo |',
             '|---|---|---|---|---|---|---|']
        for it in informe['pares']:
            if 'similitud_oficial' not in it:
                L.append('| `%s` | `%s` | — | — | — | — | %s |'
                         % (it['a'], it['b'], it.get('estado')))
                continue
            L.append('| `%s` | `%s` | %s | %s | %d | %d | %s |'
                     % (it['a'], it['b'],
                        ('%.4f' % it['similitud_oficial']) if it['similitud_oficial'] is not None else 'bajo umbral',
                        it['identicos_por_hash'], it['diff']['lineas_solo_en_a'],
                        it['diff']['lineas_solo_en_b'], it['riesgo']))
        L += ['', '## Propuesta por par', '']
        for it in informe['pares']:
            if 'propuesta' not in it:
                continue
            L += ['### `%s`  ⇄  `%s`' % (it['a'], it['b']), '',
                  '- **Similitud oficial:** %s' % (
                      ('%.4f' % it['similitud_oficial'])
                      if it['similitud_oficial'] is not None
                      else 'por debajo del umbral (no está en la lista oficial)'),
                  '- **Tamaños:** A %d bytes / %d líneas · B %d bytes / %d líneas'
                  % (it['a_meta']['bytes'], it['a_meta']['lineas'],
                     it['b_meta']['bytes'], it['b_meta']['lineas']),
                  '- **Hashes:** A `%s` · B `%s`%s'
                  % (it['a_meta']['sha256_16'], it['b_meta']['sha256_16'],
                     '  ← idénticos' if it['identicos_por_hash'] else ''),
                  '- **Propuesta:** %s' % it['propuesta'],
                  '- **Riesgo:** %s' % it['riesgo'], '']
        L += ['## Procedimiento de ejecución (cuando se firme)', '',
              '1. `git status` limpio y `git pull` en el repositorio.',
              '2. Respaldo: `tar czf data/archive/F6_lote0_<ts>.tar.gz skills/<rutas>`'
              ' + sha256.',
              '3. Integrar el contenido exclusivo en la skill que absorbe (patch).',
              '4. `git mv` del absorbido a `data/archive/F6_lote0_<ts>/`.',
              '5. Aduana (`scripts/verify_skills.py`) y métrica oficial de nuevo: el',
              '   porcentaje implicado debe **bajar** y el diff, ser solo el esperado.',
              '6. Commit con el ledger: hash antes/después por skill.',
              '7. Revisor independiente por lote (R8).', '',
              '## Ledger', '',
              'El detalle con hashes queda en `data/state/f6_lote0.json`. Al ejecutar,',
              'cada par añade su entrada antes/después en el ledger del lote.', '']
        DOC.write_text('\n'.join(L), encoding='utf-8')
        print('\nescrito: %s' % SALIDA)
        print('publicado: %s' % DOC)


if __name__ == '__main__':
    main()
