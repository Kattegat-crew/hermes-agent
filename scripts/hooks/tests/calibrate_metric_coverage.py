#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Calibracion v2: cobertura IDF del vocabulario del borrador dentro de cada documento."""
import json
import math
import sys
from collections import Counter
sys.path.insert(0, '/root/hermes-agent/scripts/hooks')
import guard_autoskill_create as g  # noqa: E402

docs, _ = g.corpus_con_cache()
docs_tk = [g.tokens(d[3]) for d in docs]

df = Counter()
for tk in docs_tk:
    df.update(set(tk))
N = len(docs)
IDF = {w: math.log((N + 1) / (c + 1)) + 1.0 for w, c in df.items()}


def cobertura(query_tk, doc_tk):
    """Fraccion del peso IDF del borrador que YA existe en el documento."""
    q = set(query_tk)
    if not q:
        return 0.0
    peso_total = sum(IDF.get(w, 1.0) for w in q)
    peso_presente = sum(IDF.get(w, 1.0) for w in q if w in set(doc_tk))
    return peso_presente / peso_total if peso_total else 0.0


CASOS = {
    'CAPI tracking -> meta-ads-ops': (
        'capi-events-diagnostico',
        'Diagnostica pixels y datasets de Meta en Events Manager y arregla la deduplicacion pixel CAPI. '
        'Enumerar datasets y pixeles de la cuenta, revisar last_fired_time, enriquecer user_data con ln ct st '
        'country zp, fbp fbc, y auditar el eventID para deduplicar pixel y CAPI. Revisar EMQ y cerrar campos '
        'server-side de forma gratuita.'),
    'reel subtitulado -> video-reel-pipeline': (
        'reel-subtitulado-automatico',
        'Quemar subtitulos en un reel con ffmpeg. Extraer el audio del reel, transcribir con whisper, generar '
        'el vtt y quemar los subtitulos sobre el mp4 vertical 9:16 con ffmpeg, verificando el keyframe con vision.'),
    'gmail inbox audit -> google-workspace-ops': (
        'auditoria-inbox-gmail', 
        'Auditar una bandeja de Gmail en modo solo lectura para otro cliente: usar las herramientas MCP de '
        'ncl_google, listar hilos no leidos, clasificar por remitente y etiquetar sin mover ni borrar nada.'),
    'tema ajeno (debe permitir crear)': (
        'calibracion-telescopio-andino',
        'Ajustar la montura ecuatorial, medir el error de alineacion polar y compensar la refraccion '
        'atmosferica para la observacion nocturna de alta montana.'),
    'otro ajeno (debe permitir crear)': (
        'fisioterapia-canina-postoperatoria',
        'Protocolo de rehabilitacion postoperatoria en perros: crioterapia, movilizacion pasiva temprana, '
        'ejercicios de propiocepcion con fitball y control del dolor en las primeras dos semanas.'),
}

print('corpus: %d documentos' % N)
for titulo, (nombre, cuerpo) in CASOS.items():
    q = g.tokens('%s %s' % (nombre.replace('-', ' '), cuerpo))
    pares = []
    for (clase, u, destino, txt), tk in zip(docs, docs_tk):
        pares.append((cobertura(q, tk), clase, u, destino))
    pares.sort(reverse=True)
    print('')
    print('### %s' % titulo)
    for s, clase, u, destino in pares[:4]:
        print('      %.3f  %-9s %-32s %s' % (s, clase, u, destino))
