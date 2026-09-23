#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F4 · documenta el modelo del curador (dueño, alcance y ciclo) y actualiza la
lista de protegidas con el resultado del pin."""
import json
import time
from pathlib import Path

R = Path('/root/hermes-agent')
POL = R / 'docs' / 'skills' / 'POLITICA-ARBOL-CANONICO.md'
PROT = R / 'docs' / 'skills' / 'protected-skills.json'

NOTA = '''
## F4 · Curador con dueño, alcance y ciclo (23-sep-2026)

### El problema que tenía el curador

Antes de F3 el canon vivía en `skills.external_dirs`, y el curador excluye por
regla dura esos árboles: su universo estaba VACÍO. Con el canon ya montado como
raíz del runtime, apareció un segundo bloqueo, más silencioso:

`get_bundled_skills_dir()` devuelve **el mismo directorio que** `get_skills_dir()`
(`/opt/data/skills`). El sync de bundled, al comparar el árbol consigo mismo,
escribía `.bundled_manifest` con las **718** entradas del catálogo → el curador
clasificaba todo como `bundled`, y por diseño no toca, ni poda, ni deja pinear
lo bundled. El catálogo estaba visible pero intocable.

### Lo que se hizo

1. **Opt-out del sync de bundled** (`hermes skills opt-out`) en los 12 perfiles:
   siembra solo las esenciales y no borra nada de lo que ya está en disco.
2. **Manifiesto auto-referencial archivado** (`data/archive/F4_manifiesto_*`).
   Efecto: `curator usage` pasa de `bundled=594` a **`bundled=0`**.
3. **Adopción del catálogo**: `hermes curator adopt --all-unmanaged --yes` —
   la procedencia del canon es una **declaración del dueño**, no una heurística.
4. **Pin de las protegidas**: 22 de las 23 de `protected-skills.json`
   (`meta-ads-discord-reporter` aún no vive en el canon: entra en F5). El pin
   era imposible mientras el árbol fuera `external_dirs`; ya es ejecutable.
5. **Driver automático neutralizado**: `curator.enabled: true` (necesario para
   el run manual) **+ `curator pause`**. El automático exige
   `enabled && !paused && intervalo vencido`, así que no puede mutar nada.
   `consolidate: false` (prune-only) por defecto.
6. **Un solo curador para un solo árbol**: el driver vive en el perfil raíz;
   los 11 perfiles quedan con `curator.enabled: false` para que nadie más
   opere sobre el árbol compartido.
7. **Ciclo semanal en seco**: `scripts/f4_curador_semanal.py` (cron lunes
   07:00) corre una revisión REAL con `--dry-run`, **no confía en la bandera**:
   compara un retrato del árbol antes/después (SKILL.md, archivo, ledger) y
   falla si algo cambió. Publica el informe en `#sistema-servers`.

### La regla de las dos revisiones

La consolidación (fusión de contenido, F6) **no se enciende** hasta acumular
**dos revisiones limpias consecutivas** (0 mutaciones, rc=0) y contar con
respaldo y firma del CTO. El job lleva el contador en
`data/state/f4_curador_last.json` (`revisiones_limpias`) y escribe
`consolidacion_autorizada: false` en cada corrida: la autorización no depende
de que nadie se acuerde.

Primera revisión: **1/2**, con 594 candidatas y 0 transiciones propuestas.
'''

t = POL.read_text(encoding='utf-8')
if 'F4 · Curador con dueño' not in t:
    POL.write_text(t.rstrip('\n') + '\n' + NOTA, encoding='utf-8')
    print('política: sección F4 añadida')

d = json.loads(PROT.read_text(encoding='utf-8'))
d['transicion_A2'] = (
    'EJECUTADA 23-sep-2026 (F4): `hermes curator pin` aplicado sobre 22 de las 23 '
    'skills de esta lista — el canon dejó de ser `external_dirs` y el comando ya '
    'las acepta. `meta-ads-discord-reporter` no vive aún en el canon (F5): pinearla '
    'cuando se incorpore.')
d['estado_pin_20260923'] = {
    'pineadas': 22,
    'pendientes': ['meta-ads-discord-reporter (no está en el canon; entra en F5)'],
    'comando': 'hermes curator pin <skill>  (perfil raíz, HERMES_HOME=/opt/data)',
    'nota': 'El pin sobre skills no gestionadas se registra igual y las excluye de '
            'toda transición automática del curador.',
}
d['verificado_en'] = time.strftime('%Y-%m-%dT%H:%M:%S%z')
PROT.write_text(json.dumps(d, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
print('protected-skills.json: estado del pin registrado')
