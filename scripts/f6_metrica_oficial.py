#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F6 · Métrica oficial de solapamiento del catálogo (TF-IDF coseno, umbral 0,45)
=============================================================================

Es el requisito de arranque de F6 (condición C3): la fase no empieza sin una
métrica única, publicada con comando, ruta y fecha, y reproducible.

Criterio (POLITICA-ARBOL-CANONICO.md §4):
  - documento por skill = nombre + descripción + cuerpo
  - vectorización TF-IDF, similitud coseno
  - umbral 0,45: dos skills por encima se consideran solapadas
  - grupos = componentes conexas del grafo de pares (no solo pares sueltos)

USO
  python3 scripts/f6_metrica_oficial.py                    # mide y publica
  python3 scripts/f6_metrica_oficial.py --canon /opt/data/skills
  python3 scripts/f6_metrica_oficial.py --umbral 0.45 --sin-escribir
"""
import argparse
import hashlib
import json
import re
import time
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

REPO = Path('/root/hermes-agent')
CANON_DEF = REPO / 'skills'
SALIDA = REPO / 'data' / 'state' / 'f6_metrica.json'
DOC = REPO / 'docs' / 'skills' / 'METRICA-CONSOLIDACION.md'
UMBRAL = 0.45


def frontmatter(txt):
    """Devuelve (nombre, descripción, cuerpo). Tolera frontmatter ausente."""
    nombre, desc = '', ''
    cuerpo = txt
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n', txt, re.S)
    if m:
        fm, cuerpo = m.group(1), txt[m.end():]
        for linea in fm.splitlines():
            mm = re.match(r'^\s*(name|title)\s*:\s*(.+)$', linea)
            if mm and not nombre:
                nombre = mm.group(2).strip().strip('\'"')
            md = re.match(r'^\s*description\s*:\s*(.+)$', linea)
            if md and not desc:
                desc = md.group(1).strip().strip('\'"')
    return nombre, desc, cuerpo


def documentos(canon):
    docs, metas = [], []
    for p in sorted(canon.rglob('SKILL.md')):
        txt = p.read_text(encoding='utf-8', errors='ignore')
        nombre, desc, cuerpo = frontmatter(txt)
        rel = str(p.parent.relative_to(canon))
        docs.append('%s %s %s' % (nombre or rel, desc, cuerpo))
        metas.append({'skill': rel,
                      'nombre': nombre or rel.split('/')[-1],
                      'descripcion': desc[:160],
                      'bytes': len(txt),
                      'sha256_16': hashlib.sha256(txt.encode()).hexdigest()[:16]})
    return docs, metas


def mide(canon, umbral):
    docs, metas = documentos(canon)
    vec = TfidfVectorizer(sublinear_tf=True, min_df=1)
    X = vec.fit_transform(docs)
    sim = cosine_similarity(X)
    np.fill_diagonal(sim, 0.0)
    idx = np.argwhere(np.triu(sim, k=1) >= umbral)
    pares = sorted(({'a': metas[i]['skill'], 'b': metas[j]['skill'],
                     'similitud': round(float(sim[i, j]), 4)} for i, j in idx),
                   key=lambda x: -x['similitud'])

    # componentes conexas (grupos)
    padre = {m['skill']: m['skill'] for m in metas}

    def find(x):
        while padre[x] != x:
            padre[x] = padre[padre[x]]
            x = padre[x]
        return x

    for p in pares:
        ra, rb = find(p['a']), find(p['b'])
        if ra != rb:
            padre[rb] = ra
    grupos = {}
    for m in metas:
        grupos.setdefault(find(m['skill']), []).append(m['skill'])
    grupos = {k: sorted(v) for k, v in grupos.items() if len(v) > 1}

    implicadas = sorted({s for g in grupos.values() for s in g})
    return {
        'comando': ('python3 scripts/f6_metrica_oficial.py --canon %s --umbral %s'
                    % (canon, umbral)),
        'metodo': ('TF-IDF (sublinear_tf, min_df=1) sobre nombre + descripción + '
                   'cuerpo; similitud coseno; grupos = componentes conexas'),
        'umbral': umbral,
        'total_skills': len(metas),
        'pares': len(pares),
        'grupos': len(grupos),
        'skills_implicadas': len(implicadas),
        'porcentaje_implicado': round(100.0 * len(implicadas) / max(1, len(metas)), 2),
        'top_pares': pares[:25],
        'pares_todos': pares,
        'detalle_grupos': {('grupo_%02d' % (n + 1)): g
                           for n, (k, g) in enumerate(sorted(grupos.items(),
                                                             key=lambda x: -len(x[1])))},
        'skills': metas,
    }


def publica(r, ruta_doc):
    L = ['# Métrica oficial de consolidación (F6)', '',
         '| Campo | Valor |', '|---|---|',
         '| Documento | `docs/skills/METRICA-CONSOLIDACION.md` |',
         '| Fecha de medición | %s |' % time.strftime('%Y-%m-%d %H:%M:%S%z'),
         '| Comando | `%s` |' % r['comando'],
         '| Umbral | **%s** |' % r['umbral'],
         '| Método | %s |' % r['metodo'],
         '| Catálogo medido | %d `SKILL.md` |' % r['total_skills'], '',
         '## Resultado', '',
         '| Métrica | Hoy | Referencia 22-sep-2026 |', '|---|---|---|',
         '| Pares sobre el umbral | **%d** | 85 |' % r['pares'],
         '| Grupos (componentes conexas) | **%d** | 45 |' % r['grupos'],
         '| Skills implicadas | **%d** | 115 |' % r['skills_implicadas'],
         '| Porcentaje del catálogo | **%.2f %%** | 16,0 %% |' % r['porcentaje_implicado'], '',
         'Objetivo de F6: bajar el porcentaje implicado **sin pérdida de contenido**,',
         'lote por lote, con ledger de hash antes/después por skill.', '',
         '## Top 25 de pares por similitud', '',
         '| # | A | B | Similitud |', '|---|---|---|---|']
    for n, p in enumerate(r['top_pares'], 1):
        L.append('| %d | `%s` | `%s` | %.4f |' % (n, p['a'], p['b'], p['similitud']))
    L += ['', '## Grupos detectados (%d)' % r['grupos'], '']
    for k, g in sorted(r['detalle_grupos'].items(), key=lambda x: -len(x[1])):
        L.append('- **%s** (%d): %s' % (k, len(g), ', '.join('`%s`' % s for s in g)))
    L += ['', '## Salida cruda', '',
          'El detalle completo —pares, grupos y el hash sha256 corto de cada skill—',
          'queda en `data/state/f6_metrica.json`, que es la fuente que consumen los',
          'lotes de consolidación y su ledger.', '']
    Path(ruta_doc).write_text('\n'.join(L), encoding='utf-8')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--canon', default=str(CANON_DEF))
    ap.add_argument('--umbral', type=float, default=UMBRAL)
    ap.add_argument('--sin-escribir', action='store_true')
    a = ap.parse_args()

    canon = Path(a.canon)
    if not (canon / 'core').exists() and not list(canon.glob('**/SKILL.md')):
        raise SystemExit('canon no encontrado: %s' % canon)

    t0 = time.time()
    r = mide(canon, a.umbral)
    r['ts'] = time.strftime('%Y-%m-%dT%H:%M:%S%z')
    r['segundos'] = round(time.time() - t0, 1)

    print('skills=%d  pares=%d  grupos=%d  implicadas=%d (%.2f %%)  en %.1fs'
          % (r['total_skills'], r['pares'], r['grupos'], r['skills_implicadas'],
             r['porcentaje_implicado'], r['segundos']))
    print('referencia 22-sep: pares=85  grupos=45  implicadas=115 (16,0 %)')
    for p in r['top_pares'][:8]:
        print('  %.4f  %s  <->  %s' % (p['similitud'], p['a'], p['b']))

    if not a.sin_escribir:
        SALIDA.parent.mkdir(parents=True, exist_ok=True)
        SALIDA.write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding='utf-8')
        publica(r, DOC)
        print('\nescrito: %s' % SALIDA)
        print('publicado: %s' % DOC)


if __name__ == '__main__':
    main()
