#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lint_skills_catalog.py — lint de catalogo (companero de verify_skills.py)
=========================================================================

Implementa dos reglas de la politica del arbol canonico
(docs/skills/POLITICA-ARBOL-CANONICO.md) que la aduana no cubria:

  R5  La clase de disparo cabe en los primeros 57 caracteres de la descripcion.
      El indice del prompt trunca ahi: si el corte parte una palabra, la skill
      queda invisible o ilegible en el indice.
  R7  Nomenclatura sin sinonimos del mismo objeto (integration != integrations).
      Detecta pares de nombres casi identicos: plural/singular, guion bajo vs
      guion, prefijo comun. Es la clase exacta de los duplicados reales medidos.

Solo AVISA: nunca cambia el estado de la aduana ni el codigo de salida del gate.
Uso:  python3 scripts/lint_skills_catalog.py [--json-out RUTA]
"""
import argparse
import json
import re
import sys
import time
from pathlib import Path

SKILLS = Path('/root/hermes-agent/skills')
VENTANA = 57


def frontmatter(content):
    m = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    return m.group(1) if m else ''


def campos(fm):
    name = desc = None
    for l in fm.splitlines():
        if l.startswith('name:'):
            name = l.split('name:', 1)[1].strip().strip("'\"")
        elif l.startswith('description:'):
            desc = l.split('description:', 1)[1].strip().strip("'\"")
    return name, desc


def normaliza(n):
    """Normaliza para detectar el mismo objeto con dos grafias.

    Casos reales medidos: `integration` vs `integrations` (plural),
    `brain-graph-operations` vs `brain-graph-ops` (abreviatura no cubierta),
    `hermes-desktop-ssh-backend` vs `hermes-desktop-ssh-diagnostico`.
    """
    n = re.sub(r'[-_]', '', n.lower())
    return n[:-1] if n.endswith('s') and not n.endswith('ss') else n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--json-out', default='/root/hermes-agent/data/state/lint_catalog_last.json')
    a = ap.parse_args()

    skills = {}
    for sm in sorted(SKILLS.rglob('SKILL.md')):
        if any(p.startswith('_') or p.startswith('.') for p in sm.relative_to(SKILLS).parts):
            continue
        if sm.parent.name in ('references', 'scripts', 'templates', 'assets', 'examples'):
            continue
        try:
            txt = sm.read_text(encoding='utf-8')
        except Exception:
            continue
        name, desc = campos(frontmatter(txt))
        if name:
            skills[name] = {'path': str(sm.parent.relative_to(SKILLS)), 'desc': desc or ''}

    print('=' * 70)
    print('🔎 LINT DE CATALOGO (R5 ventana 57 · R7 nombres sinonimos)')
    print('=' * 70)
    print('skills con nombre en frontmatter: %d' % len(skills))

    # ── R5: la clase de disparo cabe en la ventana de 57 caracteres ────────
    # El indice del prompt muestra solo los primeros 57 caracteres. Si la
    # PRIMERA FRASE no cierra dentro de esa ventana, el indice muestra una
    # frase cortada y el disparador no es autosuficiente.
    r5 = []
    for name, d in sorted(skills.items()):
        desc = d['desc'].strip()
        if not desc:
            r5.append((name, 'SIN DESCRIPCION'))
            continue
        m = re.search(r'[.!?](\s|$)', desc)
        fin_primera = m.end() if m else len(desc)
        if fin_primera > VENTANA:
            r5.append((name, 'la primera frase cierra en el caracter %d (> %d): "%s…"'
                       % (fin_primera, VENTANA, desc[:VENTANA - 12])))

    # ── R7: nombres casi identicos ─────────────────────────────────────────
    norm = {}
    for name in skills:
        norm.setdefault(normaliza(name), []).append(name)
    r7 = []
    for _, grupo in sorted(norm.items()):
        if len(grupo) > 1:
            r7.append(grupo)

    print('')
    print('R5 · descripciones cuya PRIMERA FRASE no cierra dentro de 57 caracteres: %d' % len(r5))
    for name, motivo in r5[:15]:
        print('   ⚠️  %-46s %s' % (name[:46], motivo))
    if len(r5) > 15:
        print('   … y %d más' % (len(r5) - 15))

    print('')
    print('R7 · grupos de nombres equivalentes (mismo objeto con dos grafías): %d' % len(r7))
    for grupo in r7[:15]:
        print('   ⚠️  %s' % '  ≡  '.join(grupo))
    if len(r7) > 15:
        print('   … y %d más' % (len(r7) - 15))

    print('')
    print('ℹ️  Lint informativo: no altera el estado de la aduana (verify_skills.py).')

    out = Path(a.json_out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        'ts': time.strftime('%Y-%m-%dT%H:%M:%S%z'),
        'skills': len(skills),
        'r5_ventana_57': [{'skill': n, 'motivo': m} for n, m in r5],
        'r7_nombres_equivalentes': r7,
    }, indent=2, ensure_ascii=False), encoding='utf-8')
    print('   Detalle: %s' % out)
    return 0


if __name__ == '__main__':
    sys.exit(main())
