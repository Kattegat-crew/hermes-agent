#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F6 · Arnés de verificación para el revisor INDEPENDIENTE (R8)
============================================================

El revisor no debe creerle al ejecutor ni a las actas: este script re-deriva los
hechos del repositorio y del archivo, y emite PASS/FAIL por afirmación y por lote.

  python3 scripts/f6_verifica_revision.py

Afirmaciones:
  A1  No se perdió contenido      (original en el archivo + íntegro en references/)
  A2  El catálogo en git = árbol  (SKILL.md contadas contra git ls-files)
  A3  La calidad no bajó          (aduana: 0 errores críticos)
  A4  El candado bloquea          (los motores abortan sin firma)
  A5  La métrica bajó             (contra la referencia del 22-sep)

Salida: tabla y veredicto. Código de salida 0 = todo PASS; 1 = algo falló.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

REPO = Path('/root/hermes-agent')
DATA = REPO / 'data'
CANON = REPO / 'skills'
LOTES = range(5)
REF_22SEP = {'pares': 85, 'grupos': 45, 'implicadas': 115}
filas = []
fallos = 0


def ok(nombre, bien, detalle):
    global fallos
    if not bien:
        fallos += 1
    filas.append((nombre, 'PASS' if bien else '**FAIL**', detalle))


def sh(cmd, timeout=600):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True,
                          cwd=str(REPO), timeout=timeout)


def ledger(lote):
    f = DATA / 'state' / ('f6_lote%d_ledger.jsonl' % lote)
    if not f.is_file():
        return []
    return [json.loads(l) for l in f.read_text(encoding='utf-8').splitlines() if l.strip()]


# ── A1: nada perdido ────────────────────────────────────────────────────────
sin_archivo, sin_referencia = [], []
absorbidas = 0
for lote in LOTES:
    for e in ledger(lote):
        absorbidas += 1
        rel = e['absorbida']
        arc = Path(e.get('reversible_desde') or '') if e.get('reversible_desde', '').startswith('data/') \
            else Path(e.get('reversible_desde', ''))
        arc = REPO / arc
        orig = arc / 'SKILL.md'
        if not orig.is_file():
            sin_archivo.append('%s (lote %d)' % (rel, lote))
        # el contenido íntegro debe estar en el references/ de la superviviente
        nombre = rel.split('/')[-1]
        # El contenido debe estar ÍNTEGRO en algún references/ de la superviviente.
        # No se exige el nombre exacto: el lote 1 nombró las referencias por toolkit
        # (slackbot.md) y el resto por skill (paid-ads.md). Lo que importa es el contenido.
        refs_dir = CANON / e['superviviente'] / 'references'
        if not refs_dir.is_dir():
            sin_referencia.append('%s: la superviviente no tiene references/ (lote %d)' % (rel, lote))
        elif orig.is_file():
            clave = orig.read_text(encoding='utf-8', errors='ignore').strip()[:400]
            hallado = any(clave in f.read_text(encoding='utf-8', errors='ignore')
                          for f in refs_dir.rglob('*.md'))
            if not hallado:
                sin_referencia.append('%s: contenido no hallado en references/' % rel)
ok('A1 · nada perdido (%d absorbidas, 5 lotes)' % absorbidas,
   not sin_archivo and not sin_referencia,
   'sin original en archivo: %s | sin referencia íntegra: %s'
   % (sin_archivo[:2] or 'ninguna', sin_referencia[:2] or 'ninguna'))

# ── A2: catálogo en git = árbol vivo ────────────────────────────────────────
vivo = len(list(CANON.rglob('SKILL.md')))
en_git = len([l for l in sh("git ls-files 'skills/**/SKILL.md'").stdout.splitlines() if l.strip()])
ok('A2 · catálogo en git = árbol vivo', vivo == en_git, 'vivo=%d git=%d' % (vivo, en_git))

# ── A3: aduana ──────────────────────────────────────────────────────────────
r = sh('python3 scripts/verify_skills.py')
m = re.search(r'Errores críticos:\s*(\d+)', r.stdout)
err = int(m.group(1)) if m else -1
ok('A3 · aduana sin errores críticos', err == 0, 'errores críticos=%s' % err)

# ── A4: el candado bloquea sin firma ────────────────────────────────────────
bloquean = []
for lote in LOTES:
    motores = sorted(REPO.glob('scripts/f6_lote%d_*.py' % lote))
    motores = [x for x in motores if 'ejecutar' in x.name]
    if not motores:
        bloquean.append('lote %d: sin motor' % lote)
        continue
    antes = len(list(CANON.rglob('SKILL.md')))
    p = sh('python3 %s 2>&1 | head -3' % motores[0], timeout=300)
    despues = len(list(CANON.rglob('SKILL.md')))
    if 'BLOQUEADO' not in p.stdout or antes != despues:
        bloquean.append('lote %d NO bloquea' % lote)
ok('A4 · los 5 motores abortan sin firma', not bloquean, str(bloquean or 'ninguno'))

# ── A5: la métrica bajó ─────────────────────────────────────────────────────
M = json.loads((DATA / 'state' / 'f6_metrica.json').read_text(encoding='utf-8'))
bajo = (M['pares'] < REF_22SEP['pares'] and M['grupos'] < REF_22SEP['grupos']
        and M['skills_implicadas'] < REF_22SEP['implicadas'])
ok('A5 · la métrica bajó frente al 22-sep', bool(bajo),
   'pares %d→%d · grupos %d→%d · implicadas %d→%d (%.2f %%)'
   % (REF_22SEP['pares'], M['pares'], REF_22SEP['grupos'], M['grupos'],
      REF_22SEP['implicadas'], M['skills_implicadas'], M['porcentaje_implicado']))

# ── extras: puntero y ledger por lote ───────────────────────────────────────
sin_puntero = []
for lote in LOTES:
    for e in ledger(lote):
        md = CANON / e['superviviente'] / 'SKILL.md'
        if not md.is_file() or 'Referencias absorbidas' not in md.read_text(encoding='utf-8', errors='ignore'):
            sin_puntero.append('%s (lote %d)' % (e['superviviente'], lote))
ok('EXTRA · puntero en las supervivientes', not sin_puntero, str(sin_puntero[:3] or 'todas'))

print('\n%s' % ('=' * 96))
print('F6 · VERIFICACIÓN INDEPENDIENTE — %s' % os.popen('date -Is').read().strip())
print('=' * 96)
for n, v, d in filas:
    print('%-52s %-8s %s' % (n, v, d))
print('=' * 96)
print('VEREDICTO: %s   (%d de %d en PASS)'
      % ('TODO PASA' if fallos == 0 else 'HAY %d FALLO(S)' % fallos, len(filas) - fallos, len(filas)))
print('Commit verificado: %s' % sh('git rev-parse --short HEAD').stdout.strip())
print('Nota: esto comprueba los hechos del repo, no sustituye la firma del revisor.')
sys.exit(0 if fallos == 0 else 1)
