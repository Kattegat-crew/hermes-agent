#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F0 · Rescate direccional de ediciones de agentes (23-sep-2026)
==============================================================

PROBLEMA QUE RESUELVE
  El motor existente (`sync_skills_sync.py --adopt-drift`) promueve al canon el
  contenido del contenedor para TODAS las divergencias, sin mirar la dirección.
  Con el estado del 23-sep eso revertiría `creative/hermes-multiprofile-gateway-ops`,
  cuyo canon es MÁS NUEVO (Ley 5 del gateway multiprofile, commit del 21-sep).

  Este script rescata SOLO las divergencias donde el espejo es más nuevo
  (ediciones de agentes que hoy no existen en git) y deja intactas las que el
  canon tiene más nuevas; esas las resuelve el despliegue posterior.

GATE DE FIRMA (bloqueo duro en código, no en la disciplina del agente)
  `--apply` exige `--firma TOKEN`. El token se valida por sha256 contra
  /root/.sync-firma.sha256 (creado por el dueño, chmod 600). Un agente NUNCA
  debe crear ni leer ese archivo. Sin token → exit 1, cero escrituras.

USO
  python3 scripts/f0_rescate_direccional.py                  # dry-run (default)
  python3 scripts/f0_rescate_direccional.py --apply --firma TOKEN
  python3 scripts/f0_rescate_direccional.py --apply --firma TOKEN --push
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
sys.path.insert(0, str(REPO / 'scripts'))
import sync_skills_sync as motor  # noqa: E402  (reutiliza el código probado del motor)

FIRMA_SHA = Path('/root/.sync-firma.sha256')


def log(msg=''):
    print(msg, flush=True)


def run(cmd, cwd=None, check=True):
    out = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if check and out.returncode != 0:
        log('❌ falló: %s\n%s\n%s' % (cmd, out.stdout[-800:], out.stderr[-800:]))
        raise SystemExit(1)
    return out


def check_firma(firma):
    """Mismo mecanismo que el motor: sha256 del token contra el archivo del dueño."""
    if not FIRMA_SHA.exists():
        log('🔒 GATE CERRADO — no existe %s' % FIRMA_SHA)
        log('   Lo crea el dueño:  printf %%s \'TU_TOKEN\' | sha256sum | awk \'{print $1}\' > %s' % FIRMA_SHA)
        return False
    if not firma:
        log('🔒 GATE CERRADO — falta --firma TOKEN (el token lo aporta el dueño).')
        return False
    expected = FIRMA_SHA.read_text().strip()
    got = hashlib.sha256(firma.encode()).hexdigest()
    if got != expected:
        log('❌ FIRMA INVÁLIDA — el token no coincide con el autorizado por el dueño.')
        return False
    log('✅ Firma válida.')
    return True


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument('--apply', action='store_true', help='muta (exige --firma)')
    ap.add_argument('--firma', default='')
    ap.add_argument('--push', action='store_true', help='hace git push al cerrar el commit')
    ap.add_argument('--container', default='hermes-agent')
    ap.add_argument('--container-skills', default='/opt/hermes/skills')
    ap.add_argument('--json-out', default=str(REPO / 'data/state/f0_rescate_last.json'))
    a = ap.parse_args()

    host_root = REPO / 'skills'
    log('🔍 Inventariando canon y espejo (sha256 por skill)…')
    host = motor.host_inventory(host_root)
    cont = motor.container_inventory(a.container, a.container_skills)
    log('   canon: %d skills · espejo: %d skills' % (len(host), len(cont)))

    drift = sorted(k for k in (set(host) & set(cont))
                   if motor.as_digest(host[k]) != motor.as_digest(cont[k]))

    espejo_nuevo, canon_nuevo, ambiguo = [], [], []
    for rel in drift:
        hm, cm = motor.as_mtime(host[rel]), motor.as_mtime(cont[rel])
        if cm > hm + 1:
            espejo_nuevo.append(rel)
        elif hm > cm + 1:
            canon_nuevo.append(rel)
        else:
            ambiguo.append(rel)

    log('')
    log('📊 DIVERGENCIAS POR DIRECCIÓN')
    log('   espejo más nuevo  (RESCATE → canon) : %d' % len(espejo_nuevo))
    for r in espejo_nuevo:
        log('      ⬅️  %s' % r)
    log('   canon más nuevo   (intactas; las resuelve el deploy) : %d' % len(canon_nuevo))
    for r in canon_nuevo:
        log('      ➡️  %s' % r)
    if ambiguo:
        log('   misma fecha (NO se tocan) : %d' % len(ambiguo))
        for r in ambiguo:
            log('      ❓ %s' % r)

    report = {
        'ts': time.strftime('%Y-%m-%dT%H:%M:%S%z'),
        'mode': 'apply' if a.apply else 'dry-run',
        'canon_count': len(host), 'container_count': len(cont),
        'drift_total': len(drift),
        'rescatar_al_canon': espejo_nuevo,
        'intactas_canon_mas_nuevo': canon_nuevo,
        'ambiguas': ambiguo,
    }

    if not a.apply:
        log('')
        log('🧪 DRY-RUN — no se escribió nada. Manifiesto: %s' % a.json_out)
        Path(a.json_out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.json_out).write_text(json.dumps(report, indent=2, ensure_ascii=False))
        log('   Para ejecutar:  --apply --firma TOKEN [--push]')
        return 0

    if not check_firma(a.firma):
        return 1

    if not espejo_nuevo:
        log('✅ Nada que rescatar: ninguna divergencia con el espejo más nuevo.')
        return 0

    stamp = time.strftime('%Y%m%d-%H%M%S')
    archive = REPO / 'data' / 'archive' / ('F0_rescate_' + stamp)
    archive.mkdir(parents=True, exist_ok=True)
    log('')
    log('🗄️  Respaldo previo de esta corrida: %s' % archive)

    # 1) respaldo del contenido del espejo (lo que vamos a rescatar)
    for rel in espejo_nuevo:
        log('   💾 respaldando espejo: %s' % rel)
        motor.copy_from_container(a.container, '%s/%s' % (a.container_skills, rel),
                                  archive / 'espejo' / rel)

    # 2) respaldo del contenido del canon que se va a sustituir
    for rel in espejo_nuevo:
        dst = host_root / rel
        if dst.exists():
            (archive / 'canon_previo' / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(dst, archive / 'canon_previo' / rel, dirs_exist_ok=True)

    # 3) rescate: contenedor → canon (SOLO dirección espejo-más-nuevo)
    log('')
    for rel in espejo_nuevo:
        dst = host_root / rel
        log('   ⬅️  rescatando al canon: %s' % rel)
        motor.copy_from_container(a.container, '%s/%s' % (a.container_skills, rel), dst)

    # 4) permisos del canon (lo lee el runtime de uid 10000)
    run('find "%s" -type d -exec chmod 775 {} +' % host_root)
    run('find "%s" -type f -exec chmod 664 {} +' % host_root)

    # 5) commit
    msg = 'fix(skills): F0 rescata %d edicion(es) de agente que solo vivian en el espejo (%s)' % (
        len(espejo_nuevo), stamp)
    run('git add -A skills && git commit -m "%s"' % msg, cwd=REPO)
    head = run('git rev-parse HEAD', cwd=REPO).stdout.strip()
    log('   ✅ commit: %s  (%s)' % (msg, head[:12]))

    # 6) push (condición C1: HEAD = origin/main verificado)
    if a.push:
        run('git push origin HEAD:main', cwd=REPO)
        remote = run('git ls-remote origin refs/heads/main', cwd=REPO).stdout.split()[0]
        ok = (remote == head)
        log('   %s push verificado: HEAD=%s origin/main=%s' % ('✅' if ok else '❌', head[:12], remote[:12]))
        report['push'] = {'head': head, 'origin_main': remote, 'coincide': ok}
    else:
        log('   ⚠️  sin --push: el commit existe solo en el VPS (no cierra C1).')

    report['commit'] = {'head': head, 'mensaje': msg}
    report['archive'] = str(archive)
    Path(a.json_out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.json_out).write_text(json.dumps(report, indent=2, ensure_ascii=False))

    log('')
    log('➡️  SIGUIENTE PASO (despliegue del canon al espejo, resuelve la divergencia')
    log('    donde el canon es más nuevo y retira la baja del canon):')
    log('       ./scripts/sync_container_skills.sh --apply --firma <TOKEN>')
    return 0


if __name__ == '__main__':
    sys.exit(main())
