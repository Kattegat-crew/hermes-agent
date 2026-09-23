#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F6 · Arnés de verificación para el revisor INDEPENDIENTE (R8) — v2
================================================================

v2 responde a los dos reparos del revisor (Ragnar, 23-sep):
  · A1 comparaba solo los primeros 400 caracteres  -> ahora compara el CONTENIDO
    ÍNTEGRO (normalizado), en cualquier *.md de references/.
  · A5 solo comprobaba "menor que la referencia"   -> ahora el cambio se DERIVA
    DEL PROPIO GIT: se compara el catálogo vivo contra el commit anterior al
    primer lote. Todo lo desaparecido tiene que estar en un ledger de absorción,
    y todo lo nuevo tiene que existir. Nada se cree de las actas.

  python3 scripts/f6_verifica_revision.py

Salida: PASS/FAIL por afirmación + veredicto. Código de salida 0 = todo PASS.
"""
import json
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


def norm(s):
    return re.sub(r'\s+', ' ', s).strip()


def ledger(lote):
    f = DATA / 'state' / ('f6_lote%d_ledger.jsonl' % lote)
    if not f.is_file():
        return []
    return [json.loads(l) for l in f.read_text(encoding='utf-8').splitlines() if l.strip()]


absorbidas = {}
for lote in LOTES:
    for e in ledger(lote):
        absorbidas[e['absorbida']] = {'lote': lote, 'sup': e['superviviente'],
                                      'rev': e.get('reversible_desde', ''),
                                      'hash': e.get('hash_absorbida_antes', '')}

# ── Base independiente: el catálogo tal como estaba antes del primer lote ────
c0 = sh("git log --format=%H --grep='F6 lote 0' | tail -1").stdout.strip()
base = sh("git rev-parse %s^" % c0).stdout.strip() if c0 else ''
def skills_en(rev):
    out = sh("git ls-tree -r --name-only %s -- skills | grep -c 'SKILL.md$'" % rev).stdout.strip()
    return int(out or 0)
antes = skills_en(base) if base else 0
paths_antes = set(sh("git ls-tree -r --name-only %s -- skills | grep 'SKILL.md$'" % base)
                  .stdout.split())
vivo = len(list(CANON.rglob('SKILL.md')))
paths_ahora = {str(p.relative_to(REPO)) for p in CANON.rglob('SKILL.md')}
def rel_skill(path):
    # de 'skills/creativo/x/SKILL.md' a 'creativo/x' (misma forma que el ledger)
    return path.replace('skills/', '', 1).replace('/SKILL.md', '')


desaparecidos = {rel_skill(p) for p in paths_antes - paths_ahora}
nuevos = {rel_skill(p) for p in paths_ahora - paths_antes}

# ── A1: nada perdido — contenido ÍNTEGRO, no una muestra ────────────────────
sin_archivo, sin_referencia = [], []
for rel, info in absorbidas.items():
    orig = REPO / info['rev'] / 'SKILL.md' if info['rev'].startswith('data/') else None
    if orig is None or not orig.is_file():
        sin_archivo.append(rel)
        continue
    refs_dir = CANON / info['sup'] / 'references'
    contenido = norm(orig.read_text(encoding='utf-8', errors='ignore'))
    hallado = refs_dir.is_dir() and any(
        contenido in norm(f.read_text(encoding='utf-8', errors='ignore'))
        for f in refs_dir.rglob('*.md'))
    if not hallado:
        sin_referencia.append(rel)
ok('A1 · contenido ÍNTEGRO de las %d absorbidas' % len(absorbidas),
   bool(absorbidas) and not sin_archivo and not sin_referencia,
   'íntegras ok=%d | sin original=%s | sin integral=%s'
   % (len(absorbidas) - len(sin_referencia), sin_archivo[:2] or 'ninguna',
      sin_referencia[:2] or 'ninguna'))

# ── A2: el catálogo vivo es el que está en git ──────────────────────────────
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
    motores = [x for x in sorted(REPO.glob('scripts/f6_lote%d_*.py' % lote)) if 'ejecutar' in x.name]
    if not motores:
        bloquean.append('lote %d: sin motor' % lote)
        continue
    n0 = len(list(CANON.rglob('SKILL.md')))
    p = sh('python3 %s 2>&1 | head -3' % motores[0], timeout=300)
    if 'BLOQUEADO' not in p.stdout or n0 != len(list(CANON.rglob('SKILL.md'))):
        bloquean.append('lote %d NO bloquea' % lote)
ok('A4 · los 5 motores abortan sin firma', not bloquean, str(bloquean or 'ninguno'))

# ── A5: el cambio DERIVADO DEL GIT, cuadro a cuadro ─────────────────────────
faltan_en_ledger = sorted(desaparecidos - set(absorbidas))
sobran_en_ledger = sorted(set(absorbidas) - desaparecidos)
M = json.loads((DATA / 'state' / 'f6_metrica.json').read_text(encoding='utf-8'))
aritmetica = (vivo == antes - len(desaparecidos) + len(nuevos))
ok('A5 · cambio derivado del git y cuadra con los ledgers',
   not faltan_en_ledger and not sobran_en_ledger and aritmetica
   and len(M['skills']) == vivo,
   'antes=%d vivo=%d desaparecidos=%d nuevos=%d | fuera del ledger=%s | en ledger sin desaparecer=%s | métrica.skills=%d'
   % (antes, vivo, len(desaparecidos), len(nuevos), faltan_en_ledger[:3] or 'ninguno',
      sobran_en_ledger[:3] or 'ninguno', len(M['skills'])))

bajo = (M['pares'] < REF_22SEP['pares'] and M['grupos'] < REF_22SEP['grupos']
        and M['skills_implicadas'] < REF_22SEP['implicadas'])
ok('A6 · la métrica bajó frente al 22-sep (valores exactos abajo)', bool(bajo),
   'pares %d→%d · grupos %d→%d · implicadas %d→%d (%.2f %%)'
   % (REF_22SEP['pares'], M['pares'], REF_22SEP['grupos'], M['grupos'],
      REF_22SEP['implicadas'], M['skills_implicadas'], M['porcentaje_implicado']))

# ── EXTRA: puntero en las supervivientes ────────────────────────────────────
sin_puntero = []
for rel, info in absorbidas.items():
    md = CANON / info['sup'] / 'SKILL.md'
    if not md.is_file() or 'Referencias absorbidas' not in md.read_text(encoding='utf-8', errors='ignore'):
        sin_puntero.append(info['sup'])
ok('EXTRA · puntero en las supervivientes', not sin_puntero, str(sorted(set(sin_puntero))[:3] or 'todas'))

print('\n%s' % ('=' * 100))
print('F6 · VERIFICACIÓN INDEPENDIENTE (v2) — commit %s' % sh('git rev-parse --short HEAD').stdout.strip())
print('base: catálogo en %s = %d SKILL.md | vivo = %d' % (base[:9], antes, vivo))
print('=' * 100)
for n, v, d in filas:
    print('%-58s %-8s %s' % (n, v, d))
print('=' * 100)
print('desaparecidos (%d): %s' % (len(desaparecidos), ', '.join(sorted(desaparecidos))[:400]))
print('nuevos (%d): %s' % (len(nuevos), ', '.join(sorted(nuevos))))
print('VEREDICTO: %s  (%d de %d en PASS)'
      % ('TODO PASA' if fallos == 0 else 'HAY %d FALLO(S)' % fallos, len(filas) - fallos, len(filas)))
print('Nota: comprueba los hechos del repo y de git; no sustituye la firma del revisor.')
sys.exit(0 if fallos == 0 else 1)
