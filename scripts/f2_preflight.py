#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F2 pre-flight: diferencia los montajes declarados del compose contra los vivos."""
import json
import os
import subprocess

REPO = '/root/hermes-agent'
CONT = 'hermes-agent'


def run(cmd):
    return subprocess.run(cmd, shell=True, cwd=REPO, capture_output=True, text=True)


print('=' * 78)
print('F2 PRE-FLIGHT · compose declarado vs montajes vivos')
print('=' * 78)

# 1) validacion de sintaxis del compose
ok = run('docker compose config -q')
print('docker compose config -q  -> exit %d %s' % (ok.returncode, ok.stderr.strip()[:200] or 'OK'))

# 2) volumenes declarados (via config --format json para no parsear yaml a mano)
cfg = run('docker compose config --format json')
declarados = []
if cfg.returncode == 0:
    data = json.loads(cfg.stdout)
    svc = data.get('services', {}).get('hermes-agent', {})
    for v in svc.get('volumes', []) or []:
        src = v.get('source') or v.get('src')
        dst = v.get('target') or v.get('dst')
        ro = v.get('read_only')
        declarados.append((src, dst, bool(ro)))

# 3) montajes vivos
insp = run('docker inspect %s --format "{{json .Mounts}}"' % CONT)
vivos = []
if insp.returncode == 0:
    for m in json.loads(insp.stdout):
        vivos.append((m.get('Source'), m.get('Destination'), m.get('RW') is False))
vivos_dst = {d for _, d, _ in vivos}

print('')
print('declarados en el compose: %d' % len(declarados))
print('vivos en el contenedor : %d' % len(vivos))
print('')
print('--- PENDIENTES (declarados y NO montados) ---')
pendientes = []
for src, dst, ro in declarados:
    if dst not in vivos_dst:
        existe = os.path.exists(src) if src else False
        marca = '✅ origen existe' if existe else '❌ ORIGEN NO EXISTE'
        tipo = 'dir' if src and os.path.isdir(src) else ('file' if src and os.path.isfile(src) else '?')
        pendientes.append((src, dst, ro, existe, tipo))
        print('   %-46s -> %-34s %s %s %s' % (src, dst, 'ro' if ro else 'rw', tipo, marca))

print('')
print('--- VIVOS que el compose NO declara (deriva inversa) ---')
decl_dst = {d for _, d, _ in declarados}
extra = [v for v in vivos if v[1] not in decl_dst]
print('   %d' % len(extra))
for src, dst, ro in extra:
    print('   %-46s -> %s' % (src, dst))

print('')
print('--- SLOTS s6 que el recreate reinicia ---')
slots = sorted(os.listdir('/root/hermes-agent/data/logs/gateways')) \
    if os.path.isdir('/root/hermes-agent/data/logs/gateways') else []
print('   %d: %s' % (len(slots), ', '.join(slots)))

print('')
print('--- ESTADO PREVIO DEL RUNTIME ---')
print('   ', run('docker exec %s /opt/hermes/.venv/bin/hermes skills list 2>&1 | tail -1' % CONT).stdout.strip()[:120])
par = json.load(open(os.path.join(REPO, 'data/state/skills_sync_alert.json')))
print('    paridad canon/espejo: %s (canon %s / espejo %s)' % (par.get('parity'), par.get('canon_count'), par.get('container_count')))

json.dump({'pendientes': pendientes, 'extra': extra, 'slots': slots},
          open('/root/hermes-agent/data/state/f2_preflight.json', 'w'), indent=1, ensure_ascii=False)
print('')
print('   Detalle: data/state/f2_preflight.json')
