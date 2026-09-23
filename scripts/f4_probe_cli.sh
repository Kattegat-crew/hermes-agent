#!/usr/bin/env bash
# Reconocimiento: ¿puede la flota publicar en Discord desde un cron? ¿Qué canales ve Vigía?
set -uo pipefail
echo "=== subcomandos del CLI hermes (busco envio/notify/send) ==="
docker exec hermes-agent bash -lc '/opt/hermes/.venv/bin/hermes --help 2>&1 | sed -n "/positional/,/options/p" | head -40'
echo
echo "=== help de gateway ==="
docker exec hermes-agent bash -lc '/opt/hermes/.venv/bin/hermes gateway --help 2>&1 | head -25'
