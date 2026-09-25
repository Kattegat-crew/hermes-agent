#!/usr/bin/env python3
"""
test_region_tokens.py — Diagnóstico de tokens SP-API de producción.

Prueba token×región contra GET /sellers/v1/marketplaceParticipations (operación
GRANTLESS: funciona aunque la app no tenga roles operativos seleccionados).

Para qué sirve:
  - Token inválido/revocado        -> falla en TODAS las regiones
  - Región equivocada              -> falla en una región, funciona en la correcta
  - Roles faltantes en la app      -> la sonda grantless FUNCIONA, pero los endpoints
                                       normales (ej. /sellers/v1) devuelven 403

Lee de /opt/data/.env (o SPAPI_ENV): AMAZON_SPAPI_CLIENT_ID/SECRET (comunes a todas
las regiones) y un refresh token POR REGIÓN (cuenta merged = un token por región).
Añade pares (label, envkey, región) al arreglo TESTS según el caso.
"""
import os
import json
from pathlib import Path
import urllib.request
import urllib.parse
import urllib.error

ENV = Path(os.environ.get("SPAPI_ENV", "/opt/data/.env"))
for line in ENV.read_text().splitlines():
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())

REGIONS = {
    "na": "https://sellingpartnerapi-na.amazon.com",
    "eu": "https://sellingpartnerapi-eu.amazon.com",
    "fe": "https://sellingpartnerapi-fe.amazon.com",
}
TOKEN_URL = "https://api.amazon.com/auth/o2/token"
PROBE = "/sellers/v1/marketplaceParticipations"  # grantless
UA = "NeuralCrew-DigitalExpressions/1.0"


def get_token(client_id, client_secret, refresh_token):
    data = urllib.parse.urlencode({
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }).encode()
    req = urllib.request.Request(TOKEN_URL, data=data, headers={
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def probe(base, at):
    req = urllib.request.Request(base + PROBE, headers={
        "x-amz-access-token": at,
        "Content-Type": "application/json",
        "User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def main():
    cid = os.environ["AMAZON_SPAPI_CLIENT_ID"]
    cs = os.environ["AMAZON_SPAPI_CLIENT_SECRET"]

    TESTS = [
        ("AU token (eu)", "AMAZON_SPAPI_REFRESH_TOKEN", "eu"),
        ("NA token (na)", "AMAZON_SPAPI_NA_REFRESH_TOKEN", "na"),
    ]
    for label, envkey, region in TESTS:
        rt = os.environ.get(envkey)
        if not rt:
            print(f"- {label}: {envkey} no está en el .env, omitido")
            continue
        try:
            at = get_token(cid, cs, rt)["access_token"]
            result = probe(REGIONS[region], at)
            m = result["payload"]
            print(f"OK  {label} @ {region}: {len(m)} marketplaces")
            for p in m[:8]:
                mm = p["marketplace"]
                print(f"      {mm['countryCode']:<3} {mm['id']:<16} {mm['name']}")
            print(f"      store={result['payload'][0].get('storeName')}")
        except urllib.error.HTTPError as e:
            print(f"403 {label} @ {region}: {e.read().decode()[:160]}")
        except Exception as e:
            print(f"ERR {label} @ {region}: {e}")


if __name__ == "__main__":
    main()
