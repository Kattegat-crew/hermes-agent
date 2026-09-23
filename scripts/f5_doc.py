#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F5 · publica el inventario del archivo de skills y la nota de política.

Cierra el punto D2 ("publicar inventario por grupo con rutas antes de firmar
nada") con datos LEÍDOS DEL DISCO, no recordados: lo que se purgó, cuándo y con
qué respaldo.
"""
import hashlib
import json
import subprocess
import time
from pathlib import Path

R = Path('/root/hermes-agent')
ARCH = R / 'data' / 'archive'
DOC = R / 'docs' / 'skills' / 'INVENTARIO-ARCHIVO.md'
POL = R / 'docs' / 'skills' / 'POLITICA-ARBOL-CANONICO.md'


def sh(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout.strip()


def tamano(p):
    return subprocess.run(['du', '-sh', str(p)], capture_output=True, text=True).stdout.split()[0]


def entradas_tar(p):
    return len(subprocess.run(['tar', 'tzf', str(p)], capture_output=True, text=True).stdout.splitlines())


def sha(p, limite=True):
    if limite and p.stat().st_size > 200 * 1024 * 1024:
        return '(no calculado: >200MB)'
    h = hashlib.sha256()
    with p.open('rb') as fh:
        for b in iter(lambda: fh.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()[:16]


grupos, tars = [], []
for p in sorted(ARCH.iterdir()):
    if p.is_dir():
        n = len(list(p.rglob('*')))
        sk = len(list(p.rglob('SKILL.md')))
        grupos.append((p.name, tamano(p), n, sk))
    elif p.suffix == '.gz':
        tars.append((p.name, tamano(p), entradas_tar(p), sha(p)))

encabezado = (
    'Generado el ' + time.strftime('%Y-%m-%d %H:%M %z') + ' desde el disco (no de memoria). '
    'Regla R3 de la política: **nada se\nborra; todo se archiva con respaldo**. Este documento '
    'es la respuesta al punto D2\ndel informe NC-2026-09-21-SK-01: publicar el inventario por '
    'grupo, con rutas, antes\nde firmar cualquier limpieza.')

L = ['# Inventario del archivo de skills',
     '',
     encabezado,
     '',
     'Directorio raíz del archivo: `data/archive/`',
     '',
     '## Grupos (directorios)',
     '',
     '| Grupo | Tamaño | Entradas | SKILL.md |',
     '|---|---|---|---|']
for n, t, f, sk in grupos:
    L.append('| `%s` | %s | %d | %d |' % (n, t, f, sk))
L += ['',
      '## Paquetes (tarballs)',
      '',
      '| Paquete | Tamaño | Entradas | sha256 (16) |',
      '|---|---|---|---|']
for n, t, e, s in tars:
    L.append('| `%s` | %s | %d | `%s` |' % (n, t, e, s))
L += ['',
      '## Lectura de D2',
      '',
      '- La cifra «849 cascarones listos para papelera» del informe del 21-sep **no se',
      '  reproduce**: el residuo verificable son los grupos `pre_purge_*` de la purga del',
      '  20-sep, ya empaquetados y con inventario. Dimensionar una limpieza sobre aquella',
      '  cifra habría borrado contenido en uso.',
      '- Los grupos `sync_*` son instantáneas de cada corrida del motor de sincronización',
      '  (el que F3 retiró): se conservan como bitácora, no como catálogo.',
      '- `F5_*` recoge los tres árboles retirados el 23-sep (raíces locales, `/root/.agents/',
      '  skills` y el `/opt/data/skills` del host) más sus tarballs verificados entrada por',
      '  entrada (SKILL.md en disco == SKILL.md en el paquete).',
      '',
      '## Restauración',
      '',
      '```bash',
      'tar xzf data/archive/<paquete>.tar.gz -C <destino>',
      '# o, para los grupos retirados en F5:',
      'mv data/archive/F5_<fecha>/<grupo>.original <ruta-original>',
      '```',
      '',
      '⚠️ **Aviso del 23-sep-2026:** `data/skills` NO era residuo: era el **punto de montaje**',
      'de `/opt/data/skills` (el namespace del contenedor). Moverlo en el host desancló el',
      'montaje y el perfil default se quedó sin raíz de skills hasta restaurarlo. Para',
      'retirarlo de verdad hay que recrear el contenedor (Docker vuelve a crear el punto de',
      'montaje) — nunca `mv` en caliente. El job de higiene lo detectó en la misma corrida',
      '(V1 pasó de 12 rutas a 11 y V4 bajó a 0 alcanzables) y ahora informa la ruta ausente.',
      '']

DOC.write_text('\n'.join(L), encoding='utf-8')
print('escrito %s (%d lineas)' % (DOC, len(L)))

NOTA = '''
## F5 · Cerrar todo lo que vivía fuera del repositorio (23-sep-2026)

### Árboles retirados

| Origen | Qué era | Destino |
|---|---|---|
| `/root/.agents/skills` | 189 SKILL.md, el mayor árbol externo; alimentaba los 2 crons de Meta Ads | `data/archive/F5_*/agents_skills.original` + tar 473 MB |
| `/opt/data/skills` (host) | 5 SKILL.md: las 4 huérfanas + `web-performance-core-vitals` + un `graphify-out` del 26-ago | `data/archive/F5_*/host_opt_data_skills.original` + tar |
| `data/skills` | residuo **y punto de montaje** de `/opt/data/skills` | restaurado (ver aviso abajo) |

Las **4 skills huérfanas** se incorporaron al canon antes de archivar:
`meta-ads-discord-reporter` → `specialists/marketing-ads/`,
`mobile-landing-optimization` → `specialists/marketing/`,
`google-sheets-crm-sync` y `twenty-crm-lead-ops` → `productivity/`.
(`web-performance-core-vitals` ya vivía en `specialists/devops-infra/`.)

### Los 2 crons de Meta Ads

Repuntados de `/root/.agents/skills/...` al canon
(`skills/specialists/marketing-ads/meta-ads-discord-reporter/scripts/report.py`),
con respaldo previo de la crontab y **prueba de entrega real ANTES de archivar**:
corrida desde la ruta nueva, como root en el host, contra un webhook **temporal** en
`#sistema-servers` — `Successfully sent report to Discord!`, rc=0 — para no publicar
nada en el canal del cliente. El webhook temporal se borró después (verificado: ya no
acepta mensajes).

### El aviso del punto de montaje (incidente del 23-sep-2026)

`data/skills` parecía residuo de la purga; en realidad es el **punto de montaje** de
`/opt/data/skills` en el namespace del contenedor. Al moverlo en el host, el montaje
quedó huérfano, `/opt/data/skills` dejó de existir y el perfil default perdió su raíz
de skills. Se restauró moviendo el directorio de vuelta (el montaje sigue pegado al
inodo). Regla que queda: **los puntos de montaje no se mueven en caliente**; su retiro
exige recrear el contenedor. El job de higiene lo detectó en la misma corrida y ahora
V1 informa la **ruta ausente**, no solo un conteo.

### Catálogos ajenos

`/neuralcrew_agent` (182 SKILL.md, PRD/TRD y `core/`) es el **catálogo del producto
nca-api**: contenedores `nca-*`. Queda FUERA del inventario de Hermes por definición
(R10): no se mezcla, no se consolida y no entra en el censo del canon.

### Cierre de D2

El inventario por grupo, con rutas, tamaños, entradas y sha256, queda publicado en
`docs/skills/INVENTARIO-ARCHIVO.md`, generado desde el disco.
'''

t = POL.read_text(encoding='utf-8')
if 'F5 · Cerrar todo lo que vivía' not in t:
    POL.write_text(t.rstrip('\n') + '\n' + NOTA, encoding='utf-8')
    print('política: sección F5 añadida')
