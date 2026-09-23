#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bateria v2 del gate: capa dura determinista + capa de consulta."""
import json
import subprocess
import sys

HOOK = '/root/hermes-agent/scripts/hooks/guard_autoskill_create.py'


def caso(titulo, tool, ops, esperado):
    payload = {"hook_event_name": "pre_tool_call", "tool_name": tool,
               "tool_input": {"operations": ops}, "session_id": "test", "cwd": "/root/hermes-agent"}
    out = subprocess.run([sys.executable, HOOK], input=json.dumps(payload),
                         capture_output=True, text=True, timeout=180)
    if out.returncode == 2:
        try:
            msg = (json.loads(out.stdout).get('message') or '').split('\n')[0][:100]
        except Exception:
            msg = out.stdout[:100]
        if 'fallo interno' in msg:
            ver = 'BLOQUEA*'          # bloqueo por error propio, no por veredicto
        else:
            ver = 'BLOQUEA'
    else:
        ver = 'PERMITE'
        msg = 'digest de clase entregado: %d lineas' % len(out.stdout.splitlines()) if out.stdout else ''
    print('%s %-58s -> %s' % ('OK ' if ver == esperado else 'FALLO', titulo, ver))
    if msg:
        print('        %s' % msg)


print('=' * 104)
print('BATERIA DEL GATE (capa dura + capa de consulta)')
print('=' * 104)
caso('otra tool', 'terminal', None, 'PERMITE')
caso('D1: nombre de un references existente', 'skill_manage',
     [{"name": "meta-ads-operations", "action": "create", "content": "x"}], 'BLOQUEA')
caso('D2: nombre de una clase de core/', 'skill_manage',
     [{"name": "meta-ads-ops", "action": "create", "content": "x"}], 'BLOQUEA')
caso('D3: plural de una clase (video-reel-pipelines)', 'skill_manage',
     [{"name": "video-reel-pipelines", "action": "create", "content": "x"}], 'BLOQUEA')
caso('D3: plural de un objeto real (oauth-multi-tenant-integrations)', 'skill_manage',
     [{"name": "oauth-multi-tenant-integrations", "action": "create", "content": "x"}], 'BLOQUEA')
caso('tema cubierto por un reference (CAPI) -> capa de consulta', 'skill_manage',
     [{"name": "capi-events-diagnostico", "action": "create",
       "content": "---\ndescription: Diagnostica pixels y datasets de Meta en Events Manager, dedup pixel CAPI.\n---\nEnriquecer user_data con ln ct st y auditar el eventID."}], 'PERMITE')
caso('tema ajeno (telescopio) -> permitido', 'skill_manage',
     [{"name": "calibracion-telescopio-andino", "action": "create",
       "content": "---\ndescription: Calibrar montura ecuatorial.\n---\nAlineacion polar y refraccion atmosferica."}], 'PERMITE')
caso('patch: el gate no estorba el enriquecimiento', 'skill_manage',
     [{"name": "meta-ads-ops", "action": "patch", "content": "..."}], 'PERMITE')
