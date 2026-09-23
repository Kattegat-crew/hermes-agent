#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F6 · Lote 3 — pares duplicados reales + declaración de falsos positivos
=======================================================================

  ABSORBE   specialists/marketing/paid-ads -> specialists/marketing/ads
            (descripción IDÉNTICA al carácter: duplicado real)
  ABSORBE   devops/open-design-selfhost-ops -> devops/open-design-deployment
            (el self-hosted es el caso concreto del deployment)
  FALSO +   specialists/ai-ml/pytorch-fsdp <-> unsloth (0,6850)
  FALSO +   autonomous-ai-agents/sdd-* (10 miembros, grupo_01)
  DIFIERE   software-development/amazon-sp-api <-> amazon-spapi-integration
  DIFIERE   productivity/colombia-juegos-promocionales <-> colombia-promociones-legales

Los falsos positivos se DECLARAN en `data/state/f6_falsos_positivos.json` con su
razón, para que no se vuelvan a litigar ni los fusione un lote automático.

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
    {'absorbida': 'specialists/marketing/paid-ads',
     'superviviente': 'specialists/marketing/ads',
     'fecha': '2026-09-23',
     'motivo': 'Descripción idéntica al carácter ("When the user wants help with paid '
               'advertising campaigns on Google Ads, Meta…"). Superviviente = el cuerpo mayor '
               '(28.338 B / 499 líneas vs 13.020 B / 357). Ninguno carga scripts.'},
    {'absorbida': 'devops/open-design-selfhost-ops',
     'superviviente': 'devops/open-design-deployment',
     'fecha': '2026-09-23',
     'motivo': 'El self-hosted (Docker+NPM+BYOK) es el caso concreto del deployment/operación '
               'de OpenDesign. Superviviente = el que tiene scripts/ y templates/ (11.630 B).'},
]

FALSOS = [
    {'grupo': 'autonomous-ai-agents/sdd-*', 'miembros': 10, 'similitud_max': 0.6135,
     'razon': 'Son FASES de un flujo (init, explore, propose, spec, design, tasks, apply, '
              'verify, onboard) con disparador propio y distinto: el orquestador las lanza por '
              'nombre. El parecido viene del andamiaje compartido (## Execution Role, '
              '## Language Domain Contract, ## Purpose, ## What You Receive), que además ya está '
              'factorizado en specialists/hermes-internal/_shared/sdd-phase-common.md. '
              'Tamaños de 4.164 a 14.949 B: no son plantilla repetida. chained-pr entró al grupo '
              'sólo por el encabezado. Fusionarlas rompería disparadores legítimos.',
     'accion': 'NO fusionar'},
    {'grupo': 'specialists/ai-ml/pytorch-fsdp <-> specialists/ai-ml/unsloth',
     'miembros': 2, 'similitud_max': 0.6850,
     'razon': 'Herramientas distintas: FSDP (entrenamiento distribuido con sharding) frente a '
              'Unsloth (fine-tuning LoRA/QLoRA acelerado). El solape es del andamiaje de skills '
              'de ML. Cada una arrastra su propio references/ (486 KB y 1,86 MB).',
     'accion': 'NO fusionar'},
]

DIFERIDOS = [
    {'absorbida': 'software-development/amazon-sp-api',
     'superviviente': 'software-development/amazon-spapi-integration',
     'razon': 'DIFERIDO: mismo objeto (SP-API = SPAPI) pero AMBAS cargan scripts/ propios '
              '(21 KB y 39 KB) con riesgo de colisión de nombres, y amazon-sp-api tiene una '
              'referencia entrante desde specialists/marketing/amazon-sp-api-listings. Antes de '
              'absorber hay que revisar qué invoca cada script.'},
    {'absorbida': 'productivity/colombia-juegos-promocionales',
     'superviviente': 'specialists/marketing-ads/colombia-promociones-legales',
     'razon': 'DIFERIDO: no son duplicadas, son complementarias (juegos promocionales vs marco '
              'legal de promociones) y el paraguas core/colombia-legal-ops ya guarda copia de '
              'ambas como referencias. Además las dos tienen la descripción VACÍA: es una '
              'limpieza de R5, no una fusión.'},
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
        print('  DIFIERE %-56s' % d['absorbida'])
    for f in FALSOS:
        print('  FALSO+  %-56s (%s)' % (f['grupo'], f['accion']))
    if a.ensayo:
        print('\n(ENSAYO: sin escrituras)')
        return 0

    fecha = time.strftime('%Y-%m-%d')
    arch = DATA / 'archive' / ('F6_lote3_%s' % TS)
    (arch / 'absorbidas').mkdir(parents=True, exist_ok=True)
    res = {'ts': TS, 'lote': 3, 'absorbidas': [], 'diferidos': DIFERIDOS,
           'falsos_positivos': FALSOS, 'revisiones_limpias': det.get('revisiones_limpias')}
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
        nombre = rel.split('/')[-1]
        ref_dir = p_sup / 'references'
        ref_dir.mkdir(exist_ok=True)
        ref = ref_dir / ('%s.md' % nombre)
        ref.write_text('<!-- Caso absorbido por F6 lote 3 el %s desde `%s`.\n'
                       '     Contenido íntegro; original en\n'
                       '     `data/archive/F6_lote3_%s/absorbidas/`. -->\n\n%s'
                       % (fecha, rel, TS, md.read_text(encoding='utf-8', errors='ignore')),
                       encoding='utf-8')
        copiados = []
        for x in extras:
            destino = ref_dir / nombre / x.name
            destino.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(x, destino) if x.is_dir() else shutil.copy2(x, destino)
            copiados.append(x.name)
        dest_arch = arch / 'absorbidas' / rel
        dest_arch.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(p_abs), str(dest_arch))

        # puntero en la superviviente (lección del lote 2)
        sup_md = p_sup / 'SKILL.md'
        txt = sup_md.read_text(encoding='utf-8')
        marca = '## Referencias absorbidas'
        add = ('\n- `references/%s.md` — absorbida desde `%s` el %s (F6 lote 3, R15: condensar '
               'sin borrar).\n' % (nombre, rel, fecha))
        if marca in txt:
            txt = txt.rstrip('\n') + '\n' + add
        else:
            txt = txt.rstrip('\n') + '\n\n## Referencias absorbidas\n' + add
        sup_md.write_text(txt, encoding='utf-8')
        fijar_dueno(ref_dir)
        fijar_dueno(sup_md)
        res['absorbidas'].append({'skill': rel, 'superviviente': sup_rel, 'hash_antes': h_antes,
                                  'referencia': str(ref.relative_to(REPO)),
                                  'extras_copiados': copiados,
                                  'archivada_en': str(dest_arch.relative_to(REPO)),
                                  'estado': 'absorbida'})
        ledger.append({'ts': time.strftime('%Y-%m-%dT%H:%M:%S%z'), 'lote': 3,
                       'absorbida': rel, 'superviviente': sup_rel,
                       'hash_absorbida_antes': h_antes,
                       'reversible_desde': str(dest_arch.relative_to(REPO))})
        print('  absorbida %-54s -> references/%s.md %s'
              % (rel, nombre, ('(+%d extras vivos)' % len(copiados)) if copiados else ''))

    # declaración de falsos positivos (queda en estado, para que no se re-litigue)
    fp = DATA / 'state' / 'f6_falsos_positivos.json'
    previos = []
    if fp.is_file():
        try:
            previos = json.loads(fp.read_text(encoding='utf-8')).get('declarados', [])
        except Exception:
            previos = []
    fp.write_text(json.dumps({'ts': time.strftime('%Y-%m-%dT%H:%M:%S%z'),
                              'nota': 'Grupos que la métrica oficial agrupa pero NO se fusionan, '
                                      'con su razón. Evita re-litigar y frena una fusión automática.',
                              'declarados': previos + FALSOS},
                             ensure_ascii=False, indent=1), encoding='utf-8')

    with (DATA / 'state' / 'f6_lote3_ledger.jsonl').open('a', encoding='utf-8') as f:
        for e in ledger:
            f.write(json.dumps(e, ensure_ascii=False) + '\n')
    (DATA / 'state' / ('f6_lote3_%s.json' % TS)).write_text(
        json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')

    print('\n=== ADUANA ===')
    print((sh('python3 scripts/verify_skills.py', 600).stdout or '')[-300:])
    print('=== MÉTRICA OFICIAL ===')
    print(sh('python3 scripts/f6_metrica_oficial.py', 600).stdout[:260])
    return 0


if __name__ == '__main__':
    sys.exit(main())
