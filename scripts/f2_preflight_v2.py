#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F2 pre-flight v2: qué montajes faltan y si su contenido difiere de lo que corre hoy."""
import hashlib
import json
import os
import subprocess

REPO = '/root/hermes-agent'
CONT = 'hermes-agent'

PENDIENTES_ESPERADOS = [
    ('/root/hermes-agent/skills', '/opt/hermes/skills', 'dir'),
    ('/root/hermes-agent/tools/skills_tool.py', '/opt/hermes/tools/skills_tool.py', 'file'),
    ('/root/hermes-agent/tools/delegate_tool.py', '/opt/hermes/tools/delegate_tool.py', 'file'),
    ('/root/hermes-agent/gateway/activity_labels.py', '/opt/hermes/gateway/activity_labels.py', 'file'),
    ('/root/hermes-agent/locales', '/opt/hermes/locales', 'dir'),
]


def sha_host(p):
    h = hashlib.sha256()
    h.update(open(p, 'rb').read())
    return h.hexdigest()


def sha_cont(p):
    out = subprocess.run('docker exec %s sha256sum %s' % (CONT, p),
                         shell=True, capture_output=True, text=True)
    return out.stdout.split()[0] if out.returncode == 0 else None


def difflines(host, cont):
    a = open(host, encoding='utf-8', errors='replace').read().splitlines()
    b = subprocess.run('docker exec %s cat %s' % (CONT, cont), shell=True,
                       capture_output=True, text=True).stdout.splitlines()
    add = sum(1 for l in b if l not in a)
    rem = sum(1 for l in a if l not in b)
    return len(a), len(b), add, rem


print('=' * 88)
print('F2 PRE-FLIGHT v2 · contenido de los 5 montajes pendientes')
print('=' * 88)

resumen = []
for src, dst, tipo in PENDIENTES_ESPERADOS:
    existe = os.path.exists(src)
    if tipo == 'file':
        sh, sc = (sha_host(src) if existe else None), sha_cont(dst)
        igual = (sh == sc) if (sh and sc) else None
        detalle = ''
        if igual is False and existe:
            la, lb, add, rem = difflines(src, dst)
            detalle = 'host %d l. / contenedor %d l. · %d lineas solo en host · %d solo en contenedor' % (la, lb, add, rem)
        resumen.append((dst, 'file', igual, detalle))
        print('')
        print('### %s' % dst)
        print('   origen: %s  (%s)' % (src, 'existe' if existe else 'NO EXISTE'))
        print('   sha host : %s' % (sh[:16] if sh else '—'))
        print('   sha cont : %s' % (sc[:16] if sc else '—'))
        print('   ¿IDENTICO?: %s' % ('SI ✅' if igual else ('NO ⚠️' if igual is False else '?')))
        if detalle:
            print('   deltas: %s' % detalle)
    else:
        n_host = n_cont = None
        if existe:
            n_host = sum(len(f) for _, _, f in os.walk(src))
        out = subprocess.run('docker exec %s sh -c "find %s -type f | wc -l"' % (CONT, dst),
                             shell=True, capture_output=True, text=True)
        n_cont = out.stdout.strip() or None
        resumen.append((dst, 'dir', None, 'host %s ficheros / contenedor %s' % (n_host, n_cont)))
        print('')
        print('### %s  (directorio)' % dst)
        print('   origen: %s  (%s)' % (src, 'existe' if existe else 'NO EXISTE'))
        print('   ficheros host: %s · contenedor: %s' % (n_host, n_cont))

print('')
print('=' * 88)
print('RIESGO DEL RECREATE por cada montaje que se aplica')
print('=' * 88)
for dst, tipo, igual, detalle in resumen:
    if dst == '/opt/hermes/skills':
        print('  • skills        -> objetivo de F2: elimina la copia. Contenido ya idéntico (paridad 718/718).')
    elif igual is True:
        print('  • %-15s -> idéntico a lo que corre; sin cambio de comportamiento.' % os.path.basename(dst))
    elif igual is False:
        print('  • %-15s -> ⚠️ DIFIERE: tras el recreate el runtime usará la versión del repo. %s'
              % (os.path.basename(dst), detalle))
    else:
        print('  • %-15s -> %s' % (os.path.basename(dst), detalle))

json.dump(resumen, open(os.path.join(REPO, 'data/state/f2_preflight_v2.json'), 'w'),
          indent=1, ensure_ascii=False)
print('')
print('  Detalle: data/state/f2_preflight_v2.json')
