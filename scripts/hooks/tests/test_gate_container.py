#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bateria del gate EJECUTADA DENTRO del contenedor como uid 10000 (el uid del gateway)."""
import json
import subprocess
import sys

HOOK = '/host/root/hermes-agent/scripts/hooks/guard_autoskill_create.py'
PY = '/opt/hermes/.venv/bin/python3'


def caso(titulo, tool, ops, esperado):
    payload = {"hook_event_name": "pre_tool_call", "tool_name": tool,
               "tool_input": {"operations": ops}, "session_id": "test-container",
               "cwd": "/opt/data"}
    cmd = 'cd /opt/data && %s %s' % (PY, HOOK)
    out = subprocess.run(['docker', 'exec', '-i', '-u', '10000', 'hermes-agent', 'sh', '-c', cmd],
                         input=json.dumps(payload), capture_output=True, text=True, timeout=300)
    if out.returncode == 2:
        try:
            msg = (json.loads(out.stdout).get('message') or '').split('\n')[0][:95]
        except Exception:
            msg = (out.stdout or out.stderr)[:95]
        ver = 'BLOQUEA*' if 'fallo interno' in msg else 'BLOQUEA'
    else:
        ver = 'PERMITE'
        msg = 'digest: %d lineas' % len(out.stdout.splitlines()) if out.stdout else (out.stderr[:80] or '')
    print('%s %-56s -> %s' % ('OK ' if ver == esperado else 'FALLO', titulo, ver))
    print('        %s' % msg)


print('=' * 100)
print('BATERIA DENTRO DEL CONTENEDOR (uid 10000, corpus = canon montado)')
print('=' * 100)
caso('D1: nombre de un references existente', 'skill_manage',
     [{"name": "meta-ads-operations", "action": "create", "content": "x"}], 'BLOQUEA')
caso('D2: nombre de una clase de core/', 'skill_manage',
     [{"name": "meta-ads-ops", "action": "create", "content": "x"}], 'BLOQUEA')
caso('D3: plural de un objeto real', 'skill_manage',
     [{"name": "oauth-multi-tenant-integrations", "action": "create", "content": "x"}], 'BLOQUEA')
caso('tema cubierto (CAPI) -> capa de consulta', 'skill_manage',
     [{"name": "capi-events-diagnostico", "action": "create",
       "content": "---\ndescription: Diagnostica pixels y datasets de Meta, dedup CAPI.\n---\nx"}], 'PERMITE')
caso('tema ajeno -> permitido', 'skill_manage',
     [{"name": "calibracion-telescopio-andino", "action": "create",
       "content": "---\ndescription: Montura ecuatorial.\n---\nx"}], 'PERMITE')
