#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F6 · Lote 2 — pares de solape alto con absorción limpia
=======================================================

  ABSORBE   creative/social-content -> specialists/marketing/social            (0,7729)
  ABSORBE   software-development/hermes-desktop-ssh-diagnostico
            -> software-development/hermes-desktop-ssh-backend                 (0,7261)
  DIFIERE   specialists/hermes-internal/hermes-bible-study -> specialists/marketing/hermes-bible
            (0,9994) — casi idénticas, PERO arrastran 3,2 MB de bundles cada una y
            el script `hermes-bible-study/scripts/hermes-bible-updater.py` referencia
            a `hermes-bible`: acoplamiento que exige un lote propio.

Método sin pérdida (R15): el SKILL.md íntegro del absorbido va a
`references/<absorbido>.md` de la superviviente; sus ficheros extra (references/,
scripts/) se copian a `references/<absorbido>/` para que sigan vivos; y el
directorio completo queda en el archivo del lote.

CANDADO (en código): 2/2 revisiones limpias + firma del dueño.
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
ESTADO_CURADOR = DATA / 'state' / 'f4_curador_last.json'
FIRMA_SHA = Path('/root/.sync-firma.sha256')
TS = time.strftime('%Y%m%d-%H%M%S')

PLAN = [
    {'absorbida': 'creative/social-content',
     'superviviente': 'specialists/marketing/social',
     'motivo': 'Descripción IDÉNTICA al carácter ("when the user wants help creating, '
               'scheduling, or optimizing social media content"). Superviviente = el cuerpo '
               'mayor (14.880 B / 413 líneas vs 11.212 B / 323). Ninguno carga scripts y las '
               'menciones entrantes son prosa.'},
    {'absorbida': 'software-development/hermes-desktop-ssh-diagnostico',
     'superviviente': 'software-development/hermes-desktop-ssh-backend',
     'motivo': 'El diagnóstico (70 líneas) es el caso concreto del backend (175 líneas, con '
               'scripts). El paraguas core/hermes-desktop-ops ya guardaba su propia copia como '
               'referencia, así que retire la entrada suelta no pierde nada.'},
]
DIFERIDOS = [
    {'absorbida': 'specialists/hermes-internal/hermes-bible-study',
     'superviviente': 'specialists/marketing/hermes-bible',
     'motivo': 'DIFERIDO: SKILL.md casi idénticos (6 bytes de diferencia, 240 líneas) pero cada '
               'directorio arrastra ~3,2 MB (bundles/ + references/) y '
               '`hermes-bible-study/scripts/hermes-bible-updater.py` referencia a `hermes-bible`. '
               'Antes de absorber hay que decidir dónde viven los bundles y quién invoca ese '
               'script. Lote propio.'},
]


def sh(cmd, timeout=900):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True,
                          cwd=str(REPO), timeout=timeout)


def sha16(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]


def puerta(firma=None, ensayo=False):
    rev = 0
    if ESTADO_CURADOR.is_file():
        try:
            rev = int(json.loads(ESTADO_CURADOR.read_text(encoding='utf-8'))
                      .get('revisiones_limpias', 0))
        except Exception:
            rev = 0
    if rev < 2:
        return False, 'el curador acumula %d/2 revisiones limpias' % rev, {}
    if not ensayo:
        if not firma:
            return False, 'falta --firma', {}
        try:
            esperado = FIRMA_SHA.read_text().strip()
        except Exception as e:
            return False, 'no se pudo leer el archivo de firma: %s' % e, {}
        if hashlib.sha256(firma.strip().encode()).hexdigest() != esperado:
            return False, 'la firma no coincide con /root/.sync-firma.sha256', {}
    return True, 'candado satisfecho', {'revisiones_limpias': rev}


def fijar_dueno(p):
    """I5: el runtime (uid 10000) debe poder editar lo que creamos."""
    for x in [p] + list(p.rglob('*')):
        sh('chown 10000:10000 %s' % x)
        sh('chmod %s %s' % ('2775' if x.is_dir() else '664', x))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ensayo', action='store_true')
    ap.add_argument('--firma', default='')
    a = ap.parse_args()

    ok, motivo, det = puerta(a.firma, a.ensayo)
    print('CANDADO: %s — %s %s' % ('OK' if ok else 'BLOQUEADO', motivo, det or ''))
    if not ok:
        print('ABORTADO sin escribir nada.')
        return 1
    for i in PLAN:
        print('  ABSORBE %-56s -> %s' % (i['absorbida'], i['superviviente']))
    for d in DIFERIDOS:
        print('  DIFIERE %s' % d['absorbida'])
    if a.ensayo:
        print('\n(ENSAYO: sin escrituras)')
        return 0

    fecha = time.strftime('%Y-%m-%d')
    arch = DATA / 'archive' / ('F6_lote2_%s' % TS)
    (arch / 'absorbidas').mkdir(parents=True, exist_ok=True)
    res = {'ts': TS, 'lote': 2, 'absorbidas': [], 'diferidos': DIFERIDOS,
           'revisiones_limpias': det.get('revisiones_limpias')}
    ledger = []

    for item in PLAN:
        rel, sup_rel = item['absorbida'], item['superviviente']
        p_abs, p_sup = CANON / rel, CANON / sup_rel
        md = p_abs / 'SKILL.md'
        if not md.is_file() or not p_sup.is_dir():
            res['absorbidas'].append({'skill': rel, 'estado': 'ABORTADO: no existe'})
            continue
        h_antes = sha16(md)
        extras = [x for x in p_abs.iterdir() if x.name != 'SKILL.md']
        ref_dir = p_sup / 'references'
        ref_dir.mkdir(exist_ok=True)
        ref = ref_dir / ('%s.md' % rel.split('/')[-1])
        ref.write_text('<!-- Caso absorbido por F6 lote 2 el %s desde `%s`.\n'
                       '     Contenido íntegro; original en\n'
                       '     `data/archive/F6_lote2_%s/absorbidas/`. -->\n\n%s'
                       % (fecha, rel, TS, md.read_text(encoding='utf-8', errors='ignore')),
                       encoding='utf-8')
        # extras vivos: se copian a references/<absorbido>/
        copiados = []
        for x in extras:
            destino = ref_dir / rel.split('/')[-1] / x.name
            destino.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(x, destino) if x.is_dir() else shutil.copy2(x, destino)
            copiados.append(destino.name)
        # el original completo al archivo
        dest_arch = arch / 'absorbidas' / rel
        dest_arch.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(p_abs), str(dest_arch))
        fijar_dueno(ref_dir)
        res['absorbidas'].append({'skill': rel, 'superviviente': sup_rel,
                                  'hash_antes': h_antes,
                                  'referencia': str(ref.relative_to(REPO)),
                                  'extras_copiados': copiados,
                                  'archivada_en': str(dest_arch.relative_to(REPO)),
                                  'estado': 'absorbida'})
        ledger.append({'ts': time.strftime('%Y-%m-%dT%H:%M:%S%z'), 'lote': 2,
                       'absorbida': rel, 'superviviente': sup_rel,
                       'hash_absorbida_antes': h_antes,
                       'reversible_desde': str(dest_arch.relative_to(REPO))})
        print('  absorbida %-54s -> references/%s.md %s'
              % (rel, rel.split('/')[-1], ('(+%d extras vivos)' % len(copiados)) if copiados else ''))

    with (DATA / 'state' / 'f6_lote2_ledger.jsonl').open('a', encoding='utf-8') as f:
        for e in ledger:
            f.write(json.dumps(e, ensure_ascii=False) + '\n')
    (DATA / 'state' / ('f6_lote2_%s.json' % TS)).write_text(
        json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')

    print('\n=== ADUANA ===')
    print((sh('python3 scripts/verify_skills.py', 600).stdout or '')[-320:])
    print('=== MÉTRICA OFICIAL ===')
    print(sh('python3 scripts/f6_metrica_oficial.py', 600).stdout[:280])
    return 0


if __name__ == '__main__':
    sys.exit(main())
