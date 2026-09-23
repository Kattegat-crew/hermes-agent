#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F6 · Lote 1 — paraguas de clase: automatización de APIs de terceros vía Rube MCP
===============================================================================

Familia del grupo_02 de la métrica oficial: 5 skills generadas de UNA sola
plantilla ("# <Vendor> Automation via Rube MCP", mismo esqueleto de 91 líneas).

Se crea el paraguas de clase y se absorben los 4 casos que comparten técnica,
sin perder nada (R15): cada caso queda íntegro en `references/<proveedor>.md` y
su directorio completo va al archivo del lote.

  ABSORBE   productivity/slackbot-automation
            productivity/zoho-automation
            software-development/onesignal_rest_api-automation
            specialists/marketing/metaads-automation
  DIFIERE   specialists/marketing/microsoft-clarity-automation (otra clase:
            exportación de analítica, 254 líneas, sin Rube MCP)

CANDADO (en código): 2/2 revisiones limpias del curador + firma del dueño.
Sin ambas, aborta sin escribir nada.

USO
  python3 scripts/f6_lote1_ejecutar.py --ensayo
  python3 scripts/f6_lote1_ejecutar.py --firma <TOKEN>
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
LEDGER_L0 = DATA / 'state' / 'f6_lote0_ledger.jsonl'
TS = time.strftime('%Y%m%d-%H%M%S')

PARAGUAS = 'productivity/rube-mcp-api-automation'
ABSORBER = [
    ('productivity/slackbot-automation', 'slackbot', 'Slackbot'),
    ('productivity/zoho-automation', 'zoho', 'Zoho'),
    ('software-development/onesignal_rest_api-automation', 'onesignal_rest_api', 'OneSignal'),
    ('specialists/marketing/metaads-automation', 'metaads', 'MetaAds'),
]
DIFERIDO = ('specialists/marketing/microsoft-clarity-automation',
            'Otra clase: exportación de analítica de comportamiento (254 líneas, '
            'workflows propios, sin Rube MCP en el título ni en el cuerpo). Comparte '
            'el verbo "Automatizar" pero no la técnica.')

SKILL_MD = '''---
name: rube-mcp-api-automation
description: "Automate a third-party API via Rube MCP (Composio). Cubre Zoho, Slackbot, OneSignal y MetaAds; busca las herramientas antes de ejecutar."
requires:
  mcp: [rube]
---

# Automatización de APIs de terceros vía Rube MCP — paraguas de clase

Clase de skill para automatizar **cualquier** API de terceros que tenga toolkit en
Composio, usando Rube MCP. Los casos concretos por proveedor viven en
`references/`, cada uno con su procedimiento íntegro.

## Criterio de decisión

| Si la tarea es… | Usa |
| --- | --- |
| Operar una API de un proveedor **ya cubierto** (Zoho, Slackbot, OneSignal, MetaAds) | el `references/<proveedor>.md` correspondiente |
| Operar un toolkit **nuevo** (sin referencia) | este `SKILL.md`, y al terminar añade su `references/<proveedor>.md` |
| Descubrir qué toolkits o conexiones hay | `RUBE_SEARCH_TOOLS` / `RUBE_MANAGE_CONNECTIONS` |

## Prerequisites

- Rube MCP conectado (`RUBE_SEARCH_TOOLS` disponible)
- Conexión **ACTIVE** del toolkit del proveedor vía `RUBE_MANAGE_CONNECTIONS`
- **Siempre** llamar `RUBE_SEARCH_TOOLS` primero: los esquemas cambian

## Setup

**Obtener Rube MCP:** añadir `https://rube.app/mcp` como servidor MCP. Sin API keys.

1. Verificar que `RUBE_SEARCH_TOOLS` responde
2. `RUBE_MANAGE_CONNECTIONS` con el toolkit del proveedor
3. Si la conexión no está ACTIVE, seguir el enlace de auth que devuelve
4. Confirmar estado ACTIVE antes de ejecutar cualquier workflow

## Patrón de trabajo (idéntico en todos los proveedores)

### 1. Descubrir herramientas

```
RUBE_SEARCH_TOOLS
queries: [{use_case: "<tarea concreta>", known_fields: ""}]
session: {generate_id: true}
```

### 2. Verificar conexión

```
RUBE_MANAGE_CONNECTIONS
toolkits: ["<toolkit>"]
session_id: "your_session_id"
```

### 3. Ejecutar

```
RUBE_MULTI_EXECUTE_TOOL
tools: [{tool_slug: "TOOL_SLUG_FROM_SEARCH",
         arguments: {/* esquema devuelto por la búsqueda */}}]
memory: {}
session_id: "your_session_id"
```

## Pitfalls conocidos (valen para todos los proveedores)

- **Buscar primero**: los esquemas cambian; nunca fijar slugs ni argumentos sin `RUBE_SEARCH_TOOLS`
- **Comprobar la conexión**: `RUBE_MANAGE_CONNECTIONS` debe mostrar ACTIVE antes de ejecutar
- **Cumplir el esquema**: nombres y tipos exactos de los resultados de la búsqueda
- **Parámetro memory**: incluir siempre `memory` en `RUBE_MULTI_EXECUTE_TOOL`, aunque sea `{}`
- **Reuso de sesión**: reutilizar el `session_id` dentro de un workflow; generar uno nuevo por workflow
- **Paginación**: revisar tokens de paginación y seguir hasta completar

## Proveedores cubiertos

| Proveedor | Toolkit | Doc del toolkit | Referencia |
| --- | --- | --- | --- |
| Zoho | `zoho` | composio.dev/toolkits/zoho | `references/zoho.md` |
| Slackbot | `slackbot` | composio.dev/toolkits/slackbot | `references/slackbot.md` |
| OneSignal | `onesignal_rest_api` | composio.dev/toolkits/onesignal_rest_api | `references/onesignal_rest_api.md` |
| MetaAds | `metaads` | composio.dev/toolkits/metaads | `references/metaads.md` |

## Quick Reference

| Operación | Cómo |
| --- | --- |
| Encontrar herramientas | `RUBE_SEARCH_TOOLS` con el caso de uso del proveedor |
| Conectar | `RUBE_MANAGE_CONNECTIONS` con el toolkit |
| Ejecutar | `RUBE_MULTI_EXECUTE_TOOL` con los slugs descubiertos |
| Operaciones masivas | `RUBE_REMOTE_WORKBENCH` con `run_composio_tool()` |
| Esquema completo | `RUBE_GET_TOOL_SCHEMAS` para herramientas con `schemaRef` |

---
*Paraguas de clase creado por F6 lote 1 el %s a partir de 4 skills de una sola
técnica (R15: condensar sin borrar). Las originales, íntegras, en
`data/archive/F6_lote1_%s/absorbidas/`.*
'''


def sh(cmd, timeout=900):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True,
                          cwd=str(REPO), timeout=timeout)


def sha16(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]


def puerta(firma=None, ensayo=False):
    """Candado idéntico al del lote 0 (cada script es autónomo a propósito)."""
    revisiones = 0
    if ESTADO_CURADOR.is_file():
        try:
            revisiones = int(json.loads(ESTADO_CURADOR.read_text(encoding='utf-8'))
                             .get('revisiones_limpias', 0))
        except Exception:
            revisiones = 0
    if revisiones < 2:
        return False, 'el curador acumula %d/2 revisiones limpias' % revisiones, {}
    if not ensayo:
        if not firma:
            return False, 'falta --firma', {}
        try:
            esperado = FIRMA_SHA.read_text().strip()
        except Exception as e:
            return False, 'no se pudo leer el archivo de firma: %s' % e, {}
        if hashlib.sha256(firma.strip().encode()).hexdigest() != esperado:
            return False, 'la firma no coincide con /root/.sync-firma.sha256', {}
    return True, 'candado satisfecho', {'revisiones_limpias': revisiones}


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

    fecha = time.strftime('%Y-%m-%d')
    arch = DATA / 'archive' / ('F6_lote1_%s' % TS)
    res = {'ts': TS, 'lote': 1, 'paraguas': PARAGUAS, 'absorbidas': [],
           'diferido': {'skill': DIFERIDO[0], 'motivo': DIFERIDO[1]},
           'revisiones_limpias': det.get('revisiones_limpias')}
    print('\nPARAGUAS: %s' % PARAGUAS)
    for rel, tk, nombre in ABSORBER:
        print('  ABSORBE %-56s (toolkit %s)' % (rel, tk))
    print('  DIFIERE %s\n' % DIFERIDO[0])

    if a.ensayo:
        print('(ENSAYO: sin escrituras)')
        return 0

    arch.mkdir(parents=True, exist_ok=True)
    (arch / 'absorbidas').mkdir(exist_ok=True)
    p_sup = CANON / PARAGUAS
    (p_sup / 'references').mkdir(parents=True, exist_ok=True)
    (p_sup / 'SKILL.md').write_text(SKILL_MD % (fecha, TS), encoding='utf-8')

    ledger, cambios = [], ['skills/%s/SKILL.md' % PARAGUAS.split('/', 1)[1]]
    for rel, tk, nombre in ABSORBER:
        p = CANON / rel
        md = p / 'SKILL.md'
        if not md.is_file():
            res['absorbidas'].append({'skill': rel, 'estado': 'ABORTADO: no existe'})
            continue
        cuerpo = md.read_text(encoding='utf-8', errors='ignore')
        ref = p_sup / 'references' / ('%s.md' % tk)
        ref.write_text('<!-- Caso absorbido por F6 lote 1 el %s desde `%s`.\n'
                       '     Contenido íntegro; el original está en\n'
                       '     `data/archive/F6_lote1_%s/absorbidas/`. -->\n\n%s'
                       % (fecha, rel, TS, cuerpo), encoding='utf-8')
        destino = arch / 'absorbidas' / rel
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(p), str(destino))
        ext = [x.name for x in destino.iterdir() if x.name != 'SKILL.md']
        h = {'skill': rel, 'toolkit': tk, 'hash_antes': sha16(destino / 'SKILL.md'),
             'referencia': str(ref.relative_to(REPO)), 'archivada_en': str(destino.relative_to(REPO)),
             'archivos_extra': ext, 'estado': 'absorbida'}
        res['absorbidas'].append(h)
        ledger.append({'ts': time.strftime('%Y-%m-%dT%H:%M:%S%z'), 'lote': 1,
                       'absorbida': rel, 'superviviente': PARAGUAS,
                       'hash_absorbida_antes': h['hash_antes'],
                       'reversible_desde': h['archivada_en']})
        cambios += [str(ref.relative_to(REPO)), 'skills/%s' % rel]
        print('  absorbida %-56s -> references/%s.md %s' % (rel, tk, ('+ extras: %s' % ext) if ext else ''))

    with (DATA / 'state' / 'f6_lote1_ledger.jsonl').open('a', encoding='utf-8') as f:
        for e in ledger:
            f.write(json.dumps(e, ensure_ascii=False) + '\n')
    (DATA / 'state' / ('f6_lote1_%s.json' % TS)).write_text(
        json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')

    print('\n=== ADUANA ===')
    print((sh('python3 scripts/verify_skills.py', 600).stdout or '')[-350:])
    print('=== MÉTRICA OFICIAL (debe BAJAR) ===')
    print(sh('python3 scripts/f6_metrica_oficial.py', 600).stdout[:300])
    print('\ncambios:', len(cambios))
    return 0


if __name__ == '__main__':
    sys.exit(main())
