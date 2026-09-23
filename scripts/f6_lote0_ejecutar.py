#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F6 · Lote 0 — ejecución de la absorción de pares duplicados por nombre
=====================================================================

CANDADO EN CÓDIGO (no en la disciplina del agente). Este script ABORTA sin
escribir nada si no se cumplen las tres condiciones, en este orden:

  1. `data/state/f4_curador_last.json` → `revisiones_limpias >= 2`
  2. `--firma <token>` cuyo sha256 coincida con `/root/.sync-firma.sha256`
  3. los pares a ejecutar declarados en `data/state/f6_lote0.json`

MÉTODO (sin pérdida, R15: condensar sin borrar)
  Para cada par, la skill absorbida NO se borra: su directorio completo va al
  archivo del lote y su contenido íntegro se guarda como
  `references/<absorbida>.md` dentro de la superviviente, con una sección de
  procedencia en el `SKILL.md` de la superviviente. La entrada del catálogo baja
  en 1 y el contenido queda 100 % accesible.

USO
  python3 scripts/f6_lote0_ejecutar.py --ensayo
  python3 scripts/f6_lote0_ejecutar.py --firma <TOKEN>
"""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

REPO = Path('/root/hermes-agent')
DATA = REPO / 'data'
CANON = REPO / 'skills'
ARCHIVE_BASE = DATA / 'archive'
ESTADO_CURADOR = DATA / 'state' / 'f4_curador_last.json'
FIRMA_SHA = Path('/root/.sync-firma.sha256')
LEDGER = DATA / 'state' / 'f6_lote0_ledger.jsonl'
TS = time.strftime('%Y%m%d-%H%M%S')

# Decisión por par (con su criterio, del plan Rev.6 §F6 y la métrica oficial)
PLAN = [
    {'absorbida': 'productivity/oauth-multi-tenant-integration',
     'superviviente': 'productivity/oauth-multi-tenant-integrations',
     'motivo': 'Mismo disparador (conexiones OAuth multi-tenant). R7: integration(s) '
               'es el par sinónimo clásico. Superviviente = plural (clase, 3.267 B, ya '
               'referencia a la singular). Sin referencias entrantes reales.'},
    {'absorbida': 'specialists/hermes-internal/brain-graph-ops',
     'superviviente': 'specialists/hermes-internal/brain-graph-operations',
     'motivo': 'Abreviatura del mismo objeto (ops = operations). Superviviente = nombre '
               'completo (6.198 B, ya tiene references/). El paraguas '
               'core/brain-knowledge-ops conserva su propia copia.'},
    {'absorbida': 'specialists/marketing/analytics',
     'superviviente': 'specialists/marketing/analytics-tracking',
     'motivo': 'Mismo disparador literal ("set up, improve, or audit analytics '
               'tracking") y mismo dueño/fase. Superviviente = el nombre preciso y el '
               'cuerpo mayor (15.021 B). Las menciones de "analytics" en el catálogo '
               'son prosa, no referencias.'},
]

DIFERIDOS = [
    {'absorbida': 'specialists/data-vector/pinecone-research',
     'superviviente': 'specialists/data-vector/pinecone',
     'motivo': 'DIFERIDO: está registrada en `.hub/lock.json` (instalación de hub, '
               'identifier official/specialists/data-vector/pinecone-research) y su '
               'directorio carga scripts/, que exigen reubicación y revisar quien los '
               'invoca. Además el solape (0,5045) es de tema, no de objeto: una es la '
               'skill de la base vectorial y la otra un caso aplicado de RAG.'},
]


def sh(cmd, timeout=900):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True,
                          cwd=str(REPO), timeout=timeout)


def sha16(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]


def puerta(firma=None, ensayo=False):
    """Devuelve (ok, motivo, detalle). No escribe nada."""
    revisiones = 0
    if ESTADO_CURADOR.is_file():
        try:
            revisiones = int(json.loads(ESTADO_CURADOR.read_text(encoding='utf-8'))
                             .get('revisiones_limpias', 0))
        except Exception:
            revisiones = 0
    if revisiones < 2:
        return False, 'el curador acumula %d/2 revisiones limpias' % revisiones, {}
    if not ensayo:
        if not firma:
            return False, 'falta --firma', {}
        try:
            esperado = FIRMA_SHA.read_text().strip()
        except Exception as e:
            return False, 'no se pudo leer el archivo de firma: %s' % e, {}
        dado = hashlib.sha256(firma.strip().encode()).hexdigest()
        if dado != esperado:
            return False, 'la firma no coincide con /root/.sync-firma.sha256', {}
    return True, 'candado satisfecho', {'revisiones_limpias': revisiones}


def ejecuta(ensayo):
    arch = ARCHIVE_BASE / ('F6_lote0_%s' % TS)
    (arch / 'absorbidas').mkdir(parents=True, exist_ok=True)
    ledger, cambios, res = [], [], []

    for item in PLAN:
        abs_rel, sup_rel = item['absorbida'], item['superviviente']
        p_abs, p_sup = CANON / abs_rel, CANON / sup_rel
        r = {'absorbida': abs_rel, 'superviviente': sup_rel, 'motivo': item['motivo']}
        if not p_abs.is_dir() or not p_sup.is_dir():
            r['estado'] = 'ABORTADO: falta un directorio'
            res.append(r)
            continue
        sup_md = p_sup / 'SKILL.md'
        abs_md = p_abs / 'SKILL.md'
        r['hash_absorbida_antes'] = sha16(abs_md)
        r['hash_superviviente_antes'] = sha16(sup_md)
        extras = [x for x in p_abs.iterdir() if x.name != 'SKILL.md']
        r['archivos_extra_de_la_absorbida'] = [x.name for x in extras]

        if ensayo:
            r['estado'] = 'SIMULADO'
            res.append(r)
            continue

        # 1. contenido íntegro -> references/<absorbida>.md
        ref_dir = p_sup / 'references'
        ref_dir.mkdir(exist_ok=True)
        ref = ref_dir / ('%s.md' % abs_rel.split('/')[-1])
        cuerpo = abs_md.read_text(encoding='utf-8', errors='ignore')
        ref.write_text(
            '<!-- Absorbido por F6 lote 0 el %s desde `%s`.\n'
            '     Contenido íntegro de la skill absorbida; el original queda en\n'
            '     `data/archive/F6_lote0_%s/absorbidas/`. -->\n\n%s'
            % (time.strftime('%Y-%m-%d'), abs_rel, TS, cuerpo), encoding='utf-8')

        # 2. sección de procedencia en la superviviente
        marca = '\n## Referencias absorbidas\n'
        add = ('\n- `references/%s.md` — absorbida desde `%s` el %s (F6 lote 0, R15: '
               'condensar sin borrar).\n' % (abs_rel.split('/')[-1], abs_rel,
                                             time.strftime('%Y-%m-%d')))
        txt = sup_md.read_text(encoding='utf-8')
        if marca.strip() in txt:
            txt = txt.rstrip('\n') + '\n' + add
        else:
            txt = txt.rstrip('\n') + '\n' + marca + add
        sup_md.write_text(txt, encoding='utf-8')

        # 3. la absorbida completa al archivo
        destino = arch / 'absorbidas' / abs_rel
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(p_abs), str(destino))

        r['hash_superviviente_despues'] = sha16(sup_md)
        r['referencia_creada'] = str(ref.relative_to(REPO))
        r['archivada_en'] = str(destino.relative_to(REPO))
        r['estado'] = 'absorbida'
        cambios += [str(sup_md.relative_to(REPO)),
                    str(ref.relative_to(REPO)),
                    'skills/%s' % abs_rel.split('/', 1)[1]]
        ledger.append({'ts': time.strftime('%Y-%m-%dT%H:%M:%S%z'), 'lote': 0,
                       'absorbida': abs_rel, 'superviviente': sup_rel,
                       'hash_absorbida_antes': r['hash_absorbida_antes'],
                       'hash_superviviente_antes': r['hash_superviviente_antes'],
                       'hash_superviviente_despues': r['hash_superviviente_despues'],
                       'reversible_desde': r['archivada_en']})
        res.append(r)

    return arch, res, ledger, cambios


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ensayo', action='store_true')
    ap.add_argument('--firma', default='')
    a = ap.parse_args()

    ok, motivo, det = puerta(a.firma, a.ensayo)
    print('CANDADO: %s — %s %s' % ('OK' if ok else 'BLOQUEADO', motivo,
                                   json.dumps(det) if det else ''))
    if not ok:
        print('ABORTADO sin escribir nada.')
        return 1

    print('\nPLAN DEL LOTE 0 (%d pares, %d diferido)\n' % (len(PLAN), len(DIFERIDOS)))
    for i in PLAN:
        print('  ABSORBE  %s\n     -> %s' % (i['absorbida'], i['superviviente']))
    for d in DIFERIDOS:
        print('  DIFIERE  %s (%s)' % (d['absorbida'], d['motivo'][:70]))

    arch, res, ledger, cambios = ejecuta(a.ensayo)
    print()
    for r in res:
        print('  %-52s %s' % (r['absorbida'], r.get('estado')))
        if r.get('archivos_extra_de_la_absorbida'):
            print('     ⚠ archivos extra: %s' % r['archivos_extra_de_la_absorbida'])

    if a.ensayo:
        print('\n(ENSAYO: sin escrituras)')
        return 0

    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open('a', encoding='utf-8') as f:
        for e in ledger:
            f.write(json.dumps(e, ensure_ascii=False) + '\n')
    informe = {'ts': TS, 'lote': 0, 'archivo': str(arch.relative_to(REPO)),
               'resultados': res, 'diferidos': DIFERIDOS,
               'revisiones_limpias': det.get('revisiones_limpias')}
    (DATA / 'state' / ('f6_lote0_%s.json' % TS)).write_text(
        json.dumps(informe, ensure_ascii=False, indent=1), encoding='utf-8')

    print('\n=== ADUANA ===')
    r = sh('python3 scripts/verify_skills.py', timeout=600)
    print((r.stdout or r.stderr)[-400:])

    print('=== MÉTRICA OFICIAL (debe BAJAR) ===')
    r = sh('python3 scripts/f6_metrica_oficial.py', timeout=600)
    print(r.stdout[:400])
    return 0


if __name__ == '__main__':
    sys.exit(main())
