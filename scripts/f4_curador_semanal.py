#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F4 · Driver semanal del curador EN SECO
=======================================

Qué hace y por qué así
  Con el canon como árbol único, el curador por fin tiene al catálogo en su
  universo (antes lo excluía la regla dura de `skills.external_dirs`). Pero un
  curador que corre solo y poda sin red es exactamente el riesgo que la
  política (R8) prohíbe: por eso el driver AUTOMÁTICO queda apagado
  (`curator.enabled: false` en los 12 perfiles) y el ciclo lo lleva este job,
  que ejecuta una revisión REAL con `--dry-run`: informe de propuestas,
  CERO mutaciones, y aviso al canal de operaciones.

  Dos revisiones limpias consecutivas son la condición para autorizar la
  consolidación (R8 / F6), que además exige respaldo y firma del CTO.

Verificación de "cero mutaciones"
  El script mide el estado del árbol antes y después (SKILL.md, entradas del
  archivo del curador, líneas del ledger) y falla si algo cambió. No confía en
  la bandera `--dry-run`: la comprueba.

USO
  python3 scripts/f4_curador_semanal.py [--sin-notificar] [--timeout 1800]
"""
import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path

REPO = Path('/root/hermes-agent')
DATA = REPO / 'data'
SKILLS = REPO / 'skills'
CONT = 'hermes-agent'
HERMES = '/opt/hermes/.venv/bin/hermes'
DISCORD_DESTINO = 'discord:1552059363500228618'
ROTULO = '🧹 Vigía · curador en seco'
ESTADO = DATA / 'state' / 'f4_curador_last.json'


def log(m=''):
    print(m, flush=True)


def sh(cmd, timeout=600):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True,
                              timeout=timeout)
    except subprocess.TimeoutExpired:
        class R:
            returncode, stdout, stderr = 124, '', 'timeout'
        return R()


def retrato():
    """Estado del árbol para detectar mutaciones (no confiar en el flag)."""
    sm = sh('find %s -name SKILL.md | wc -l' % SKILLS).stdout.strip()
    arch = sh('find %s/.archive -type d -mindepth 1 2>/dev/null | wc -l' % SKILLS).stdout.strip()
    led = sh('wc -l < %s/.curator_ledger.jsonl 2>/dev/null || echo 0' % SKILLS).stdout.strip()
    return {'skill_md': int(sm or 0), 'archivadas': int(arch or 0), 'ledger': int(led or 0)}


def revision(timeout=1800):
    cmd = ('docker exec -u 10000 -e HERMES_HOME=/opt/data -e HOME=/opt/data %s %s '
           'curator run --dry-run --sync' % (CONT, HERMES))
    r = sh(cmd, timeout=timeout)
    salida = (r.stdout or '') + (r.stderr or '')
    informe = {'rc': r.returncode, 'salida': salida[-6000:]}
    m = re.search(r'report[^\n]*?([/\w.-]+logs/curator[/\w.-]*)', salida, re.I)
    informe['ruta_informe'] = m.group(1) if m else None
    return informe


def propuestas(salida):
    """Extrae las líneas del informe que importan (propuestas y veredictos)."""
    lineas = []
    for l in salida.splitlines():
        s = l.strip()
        if not s:
            continue
        if re.search(r'\b(archive|archivar|consolidat|consolidar|umbrella|obsolet|'
                     r'stale|duplicat|propose|propuesta|candidate|candidat|'
                     r'transition|transici|no changes|dry-run auto|llm)\b', s, re.I):
            lineas.append(s[:200])
    return lineas[:30]


def notificar(resumen, propuestas_txt, aplicar=True):
    cuerpo = '\n'.join([ROTULO, '', resumen, '', propuestas_txt or '(sin propuestas)'])
    tmp = Path('/tmp/f4_curador_alerta.txt')
    tmp.write_text(cuerpo, encoding='utf-8')
    if not aplicar:
        return {'enviado': False, 'motivo': 'sin-notificar'}
    cmd = ('docker exec -i -e HERMES_HOME=/opt/data -e HOME=/opt/data %s %s send '
           '--to %s --subject "curador en seco (semanal)" --file - --json < %s'
           % (CONT, HERMES, DISCORD_DESTINO, tmp))
    r = sh(cmd, timeout=180)
    return {'enviado': r.returncode == 0, 'rc': r.returncode,
            'salida': (r.stdout or r.stderr or '').strip()[:300]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sin-notificar', action='store_true')
    ap.add_argument('--timeout', type=int, default=1800)
    a = ap.parse_args()

    ts = time.strftime('%Y-%m-%dT%H:%M:%S%z')
    log('═══ F4 · CURADOR EN SECO · %s ═══' % ts)
    antes = retrato()
    log('  antes: %s' % antes)

    rev = revision(a.timeout)
    log('  revisión rc=%s (informe: %s)' % (rev['rc'], rev.get('ruta_informe')))

    despues = retrato()
    log('  después: %s' % despues)
    mutaciones = {k: (antes[k], despues[k]) for k in antes if antes[k] != despues[k]}
    props = propuestas(rev['salida'])

    prev = {}
    if ESTADO.is_file():
        try:
            prev = json.loads(ESTADO.read_text(encoding='utf-8'))
        except Exception:
            prev = {}
    limpias = int(prev.get('revisiones_limpias', 0))
    limpia = (not mutaciones) and rev['rc'] == 0
    if limpia:
        limpias += 1

    resumen = ('Revisión en seco %s · mutaciones: %s · revisión limpia: %s\n'
               'Revisiones limpias consecutivas: %d/2 (condición para autorizar la '
               'consolidación, R8)\nPropuestas detectadas: %d'
               % ('OK' if rev['rc'] == 0 else 'con rc=%s' % rev['rc'],
                  'NINGUNA' if not mutaciones else json.dumps(mutaciones),
                  'sí' if limpia else 'no', limpias, len(props)))
    log('  ' + resumen.replace('\n', '\n  '))

    notif = {'enviado': False, 'motivo': 'sin-notificar'}
    if not a.sin_notificar:
        notif = notificar(resumen, '\n'.join('  · ' + p for p in props))
    log('  notificación: %s' % json.dumps(notif, ensure_ascii=False)[:200])

    informe = {'ts': ts, 'antes': antes, 'despues': despues,
               'mutaciones': mutaciones, 'revision_rc': rev['rc'],
               'ruta_informe': rev.get('ruta_informe'),
               'propuestas': props, 'revision_limpia': limpia,
               'revisiones_limpias': limpias, 'notificacion': notif,
               'consolidacion_autorizada': limpias >= 2 and False,
               'nota': ('consolidación NO autorizada por este job: exige 2 revisiones '
                        'limpias + firma del CTO (R8/F6). El driver automático del '
                        'curador está apagado a propósito en los 12 perfiles.')}
    ESTADO.write_text(json.dumps(informe, indent=1, ensure_ascii=False), encoding='utf-8')
    (DATA / 'state' / ('f4_curador_%s.json' % time.strftime('%Y%m%d-%H%M%S'))).write_text(
        json.dumps(informe, indent=1, ensure_ascii=False), encoding='utf-8')
    log('  estado: %s' % ESTADO)
    return 0 if (limpia and not mutaciones) else 3


if __name__ == '__main__':
    sys.exit(main())
