#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Calibracion v3: corpus de registros CORTOS y densos (nombre + descripcion + encabezados)."""
import math
import re
import sys
from collections import Counter
from pathlib import Path
sys.path.insert(0, '/root/hermes-agent/scripts/hooks')
import guard_autoskill_create as g  # noqa: E402

CORE = Path('/opt/hermes/skills/core')


def registros():
    regs = []
    for u in sorted(d.name for d in CORE.iterdir() if d.is_dir() and (d / 'SKILL.md').is_file()):
        sm = (CORE / u / 'SKILL.md').read_text(encoding='utf-8', errors='replace')
        h2 = ' '.join(re.findall(r'^##\s+(.+)$', sm, re.M))
        regs.append(('paraguas', u, 'skills/core/%s/SKILL.md' % u,
                     '%s %s %s %s' % (u.replace('-', ' '), g.descripcion(sm), h2, sm[:600])))
        rd = CORE / u / 'references'
        if rd.is_dir():
            for r in sorted(rd.iterdir()):
                if r.is_file() and r.suffix == '.md':
                    t = r.read_text(encoding='utf-8', errors='replace')
                    titulo = (re.search(r'^#\s+(.+)$', t, re.M) or [None, ''])[1] if t else ''
                    desc = g.descripcion(t) or re.search(r'^description:\s*(.+)$', t, re.M)
                    desc = desc if isinstance(desc, str) else ''
                    regs.append(('reference', u, 'skills/core/%s/references/%s' % (u, r.name),
                                 '%s %s %s %s' % (r.stem.replace('-', ' '), titulo, desc, t[:400])))
    return regs


regs = registros()
docs_tk = [g.tokens(r[3]) for r in regs]
df = Counter()
for tk in docs_tk:
    df.update(set(tk))
N = len(regs)
IDF = {w: math.log((N + 1) / (c + 1)) + 1.0 for w, c in df.items()}


def cobertura(q, dt):
    q = set(q)
    dt = set(dt)
    if not q:
        return 0.0
    tot = sum(IDF.get(w, 1.0) for w in q)
    pres = sum(IDF.get(w, 1.0) for w in q if w in dt)
    return pres / tot if tot else 0.0


CASOS = {
    'CAPI tracking (meta-ads-ops)': ('capi-events-diagnostico',
        'Diagnostica pixels y datasets de Meta en Events Manager y arregla la deduplicacion pixel CAPI. '
        'Enriquecer user_data con ln ct st country zp, fbp fbc, auditar eventID y EMQ.'),
    'reel subtitulado (video-reel-pipeline)': ('reel-subtitulado-automatico',
        'Quemar subtitulos en un reel con ffmpeg. Transcribir con whisper, generar el vtt y quemar los '
        'subtitulos sobre el mp4 vertical 9:16.'),
    'gmail inbox audit (google-workspace-ops)': ('auditoria-inbox-gmail',
        'Auditar una bandeja de Gmail en modo solo lectura: listar hilos, clasificar por remitente y etiquetar sin borrar.'),
    'activepieces flows (google-workspace-ops)': ('activepieces-flows-ops',
        'Operar y reparar flows de ActivePieces: conectar por MCP, pausar pasos y reinyectar filas al Google Sheet.'),
    'AJENO: telescopio andino': ('calibracion-telescopio-andino',
        'Ajustar la montura ecuatorial, medir el error de alineacion polar y compensar la refraccion atmosferica.'),
    'AJENO: fisioterapia canina': ('fisioterapia-canina-postoperatoria',
        'Rehabilitacion postoperatoria en perros: crioterapia, movilizacion pasiva y propiocepcion con fitball.'),
    'AJENO: reposteria sourdough': ('masa-madre-sourdough',
        'Mantener una masa madre viva: hidratacion, alimentacion cada 12 horas y control de acidez por pH.'),
}

print('registros cortos: %d' % N)
for titulo, (nombre, cuerpo) in CASOS.items():
    q = g.tokens('%s %s' % (nombre.replace('-', ' '), cuerpo))
    pares = sorted(((cobertura(q, tk), c, u, d) for (c, u, d, _), tk in zip(regs, docs_tk)),
                   reverse=True)
    print('')
    print('### %s' % titulo)
    for s, c, u, d in pares[:3]:
        print('      %.3f  %-9s %-30s %s' % (s, c, u, d))
