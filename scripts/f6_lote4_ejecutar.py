#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F6 · Lote 4 — pares duplicados del tramo 0,51-0,59 + declaración de falsos positivos
====================================================================================
Método y candado idénticos a los lotes anteriores (2/2 revisiones limpias + firma;
absorción sin pérdida con puntero en la superviviente y extras vivos).
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
FECHA = time.strftime('%Y-%m-%d')

PLAN = [
    ('creative/neuralcrew-bot-avatars', 'creative/bot-avatar-config',
     'Misma tarea (instalar/actualizar el avatar de un bot). La absorbida tenía "dónde viven '
     'los assets (fuente de verdad)"; la superviviente, el refresco de Desktop y Discord.'),
    ('specialists/hermes-internal/hermes-desktop-windows-troubleshooting',
     'specialists/hermes-internal/hermes-windows-install',
     'Mismo problema (fallo de instalación de Hermes Desktop en Windows). Superviviente = la '
     'que trae el arreglo paso a paso y references/.'),
    ('specialists/hermes-internal/hermes-provider-fallback',
     'specialists/hermes-internal/hermes-provider-resilience',
     'Misma clase (redundancia/fallback multi-proveedor LLM). Superviviente = el concepto mayor '
     '(5.553 B, con references/); la absorbida aporta la cascada concreta y B.AI/OpenCode-Go.'),
    ('specialists/hermes-internal/client-agent-soul-survey',
     'specialists/hermes-internal/client-agent-onboarding',
     'Mismo proceso (/soul para perfilar clientes y armar su SOUL.md) y mismo despliegue del '
     'comando en el perfil. Superviviente = la que trae templates/ y el ciclo posterior.'),
    ('specialists/hermes-internal/hermes-desktop-remote-setup',
     'specialists/hermes-internal/hermes-desktop-remote-gateway',
     'Mismo asunto en dos fases (montaje / diagnóstico), igual que el par backend+diagnóstico '
     'del lote 2. Superviviente = la que trae el modelo correcto y la URL.'),
]

FALSOS = [
    {'grupo': 'specialists/devops/aws-solution-architect <-> gcp-cloud-architect',
     'miembros': 2, 'similitud_max': 0.5087,
     'razon': 'Proveedores distintos (AWS vs GCP): mismo andamiaje de skill de arquitectura, '
              'arquitecturas distintas. Fusionarlas borraría la mitad de la cobertura.',
     'accion': 'NO fusionar'},
    {'grupo': 'specialists/marketing/3-statement-model <-> lbo-model',
     'miembros': 2, 'similitud_max': 0.5419,
     'razon': 'Modelos financieros distintos (integrado IS/BS/CF vs LBO con IRR/MOIC). '
              'El parecido es del andamiaje de modelado en Excel.',
     'accion': 'NO fusionar'},
    {'grupo': 'specialists/marketing/form-cro <-> signup',
     'miembros': 2, 'similitud_max': 0.5199,
     'razon': 'Separación DELIBERADA: la descripción de form-cro dice "cualquier formulario que '
              'NO sea signup/registro" y la de signup cubre justo ese caso. Se cruzaron para no '
              'solaparse; fusionarlas reintroduce el solape que sus autores evitaron.',
     'accion': 'NO fusionar'},
]

DIFERIDOS = [
    ('autonomous-ai-agents/writing-plans', 'specialists/hermes-internal/plan',
     'DIFERIDO: disparadores distintos (metodología de planificación antes de tocar código vs '
     'escribir un markdown en .hermes/plans/ sin ejecución). Además `plan` genera el comando '
     '/plan, que COLISIONA con un comando núcleo de Hermes (el log registra que se omitió su '
     'auto-registro): decidirlo es del dueño, no del lote.'),
    ('specialists/marketing-ads/meta-ads-campaigns',
     'specialists/marketing-ads/meta-ads-operations',
     'DIFERIDO: 21,8 KB frente a 9,7 KB y papeles distintos (construir campañas/adsets/pixel vs '
     'operar campañas, geo e insights). Ambas las referencia el paraguas core/meta-ads-ops con '
     'su propia copia. Exige lectura fina antes de fusionar.'),
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
    for abs_r, sup_r, _ in PLAN:
        print('  ABSORBE %-52s -> %s' % (abs_r.split('/', 1)[-1], sup_r.split('/', 1)[-1]))
    for f in FALSOS:
        print('  FALSO+  %s' % f['grupo'])
    for d in DIFERIDOS:
        print('  DIFIERE %s' % d[0].split('/', 1)[-1])
    if a.ensayo:
        print('\n(ENSAYO: sin escrituras)')
        return 0

    arch = DATA / 'archive' / ('F6_lote4_%s' % TS)
    (arch / 'absorbidas').mkdir(parents=True, exist_ok=True)
    res = {'ts': TS, 'lote': 4, 'absorbidas': [], 'revisiones_limpias': det.get('revisiones_limpias')}
    ledger = []

    for rel, sup_rel, motivo_item in PLAN:
        p_abs, p_sup = CANON / rel, CANON / sup_rel
        md = p_abs / 'SKILL.md'
        if not md.is_file() or not p_sup.is_dir():
            res['absorbidas'].append({'skill': rel, 'estado': 'ABORTADO: no existe'})
            print('  !! no existe: %s' % rel)
            continue
        h_antes = sha16(md)
        nombre = rel.split('/')[-1]
        extras = [x for x in p_abs.iterdir() if x.name != 'SKILL.md']
        ref_dir = p_sup / 'references'
        ref_dir.mkdir(exist_ok=True)
        ref = ref_dir / ('%s.md' % nombre)
        ref.write_text('<!-- Caso absorbido por F6 lote 4 el %s desde `%s`.\n'
                       '     Contenido íntegro; original en\n'
                       '     `data/archive/F6_lote4_%s/absorbidas/`. -->\n\n%s'
                       % (FECHA, rel, TS, md.read_text(encoding='utf-8', errors='ignore')),
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

        sup_md = p_sup / 'SKILL.md'
        txt = sup_md.read_text(encoding='utf-8')
        add = ('\n- `references/%s.md` — absorbida desde `%s` el %s (F6 lote 4, R15: condensar '
               'sin borrar).\n' % (nombre, rel, FECHA))
        marca = '## Referencias absorbidas'
        txt = (txt.rstrip('\n') + ('\n' + add if marca in txt
                                   else '\n\n## Referencias absorbidas\n' + add))
        sup_md.write_text(txt, encoding='utf-8')
        fijar_dueno(ref_dir)
        fijar_dueno(sup_md)
        res['absorbidas'].append({'skill': rel, 'superviviente': sup_rel, 'hash_antes': h_antes,
                                  'referencia': str(ref.relative_to(REPO)),
                                  'extras_copiados': copiados,
                                  'archivada_en': str(dest_arch.relative_to(REPO)),
                                  'motivo': motivo_item, 'estado': 'absorbida'})
        ledger.append({'ts': time.strftime('%Y-%m-%dT%H:%M:%S%z'), 'lote': 4, 'absorbida': rel,
                       'superviviente': sup_rel, 'hash_absorbida_antes': h_antes,
                       'reversible_desde': str(dest_arch.relative_to(REPO))})
        print('  absorbida %-52s -> references/%s.md %s'
              % (nombre, nombre, ('(+%d extras)' % len(copiados)) if copiados else ''))

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
                              'declarados': previos + FALSOS}, ensure_ascii=False, indent=1),
                  encoding='utf-8')
    res['falsos_positivos'] = FALSOS

    with (DATA / 'state' / 'f6_lote4_ledger.jsonl').open('a', encoding='utf-8') as f:
        for e in ledger:
            f.write(json.dumps(e, ensure_ascii=False) + '\n')
    (DATA / 'state' / ('f6_lote4_%s.json' % TS)).write_text(
        json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')

    print('\n=== ADUANA ===')
    print((sh('python3 scripts/verify_skills.py', 600).stdout or '')[-280:])
    print('=== MÉTRICA OFICIAL ===')
    print(sh('python3 scripts/f6_metrica_oficial.py', 600).stdout[:240])
    return 0


if __name__ == '__main__':
    sys.exit(main())
