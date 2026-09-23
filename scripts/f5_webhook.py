#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F5 · crea un webhook TEMPORAL en #sistema-servers para probar la entrega de
report.py sin publicar nada en el canal del cliente."""
import json
import re
import urllib.request
from pathlib import Path

CANAL = '1552059363500228618'  # #sistema-servers
NOMBRE = 'vigia-ops-test-f5'
ENV = Path('/opt/data/.env')
SALIDA = Path('/tmp/ops_webhook.txt')


def token():
    for l in ENV.read_text(encoding='utf-8').splitlines():
        if l.startswith('DISCORD_BOT_TOKEN='):
            return l.split('=', 1)[1].strip().strip('"\'')
    raise SystemExit('no encuentro DISCORD_BOT_TOKEN')


def api(url, payload=None, metodo='GET', tk=None):
    req = urllib.request.Request(url, method=metodo)
    req.add_header('Authorization', 'Bot %s' % (tk or token()))
    req.add_header('Content-Type', 'application/json')
    req.add_header('User-Agent', 'DiscordBot (https://example.org, 1.0)')
    data = json.dumps(payload).encode() if payload is not None else None
    try:
        with urllib.request.urlopen(req, data=data, timeout=30) as r:
            return r.status, json.loads(r.read().decode() or '{}')
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:300]
    except Exception as e:
        return 0, str(e)


BASE = 'https://discord.com/api/v10'
tk = token()

# ¿ya existe?
st, hooks = api('%s/channels/%s/webhooks' % (BASE, CANAL), tk=tk)
existente = None
if isinstance(hooks, list):
    for h in hooks:
        if h.get('name') == NOMBRE:
            existente = h
    print('webhooks en el canal: %d (existentes con ese nombre: %s)'
          % (len(hooks), bool(existente)))
else:
    print('no pude listar webhooks:', st, hooks)

if existente:
    url = '%s/webhooks/%s/%s' % (BASE, existente['id'], existente['token'])
else:
    st, res = api('%s/channels/%s/webhooks' % (BASE, CANAL), {'name': NOMBRE}, 'POST', tk)
    if st not in (200, 201):
        print('❌ no se pudo crear el webhook (status %s): %s' % (st, str(res)[:200]))
        raise SystemExit(2)
    url = '%s/webhooks/%s/%s' % (BASE, res['id'], res['token'])
    print('✅ webhook temporal creado (id %s)' % res['id'])

SALIDA.write_text(url, encoding='utf-8')
print('url temporal escrita en %s' % SALIDA)
print('canal destino del webhook:', re.search(r'/webhooks/(\d+)/', url).group(1))
