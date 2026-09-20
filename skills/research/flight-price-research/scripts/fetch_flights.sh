#!/usr/bin/env bash
# fetch_flights.sh — descarga páginas de Google Flights (1 por fecha) para parsear con parse_gf.py
# Uso: ./fetch_flights.sh BOG HNL 2026-10-26 2026-10-31 IDA
#   (ej. para ida; para comparar país usar --co que cambia hl/gl/curr)

set -euo pipefail

ORIG="${1:-BOG}"
DEST="${2:-HNL}"
DATE_START="${3:-2026-10-26}"
DATE_END="${4:-2026-10-31}"
MODE="${5:-USD}"   # USD o COP

UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
CK="CONSENT=YES+cb.20260601-13-p0.en+FX+111"

if [ "$MODE" = "COP" ]; then
  HL="es"; GL="CO"; CURR="COP"; SUF="co"
else
  HL="en"; GL="US"; CURR="USD"; SUF="us"
fi

d="$DATE_START"
while [ "$(date -d "$d" +%s)" -le "$(date -d "$DATE_END" +%s)" ]; do
  q="Flights%20from%20${ORIG}%20to%20${DEST}%20on%20${d}%20one-way"
  out="gf_${ORIG,,}_${DEST,,}_${d}_${SUF}.html"
  curl -sL --max-time 60 \
    "https://www.google.com/travel/flights?q=${q}&hl=${HL}&gl=${GL}&curr=${CURR}" \
    -H "User-Agent: $UA" -H "Accept-Language: ${HL}-${GL},${HL};q=0.9" -H "Cookie: $CK" \
    -o "$out"
  echo "$d -> $(wc -c < "$out") bytes ($out)"
  d=$(date -d "$d + 1 day" +%Y-%m-%d)
done