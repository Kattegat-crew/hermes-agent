#!/usr/bin/env python3
"""
spapi_token.py - Helper para Amazon SP-API (Selling Partner API).
Digital Expressions / NeuralCrew Labs · 2026-08-18

Uso:
    python3 spapi_token.py --test                          # smoke test (sellers/v1)
    python3 spapi_token.py --test --sandbox                # smoke test contra sandbox (lee AMAZON_SPAPI_SANDBOX_*)
    python3 spapi_token.py --endpoint "/reports/v1/reportTypes"
    python3 spapi_token.py --endpoint "/orders/v0/orders?MarketplaceIds=A39IBJ37TRP1C6&CreatedAfter=TIMESTAMP"

Credenciales: lee AMAZON_SPAPI_* (producción) o AMAZON_SPAPI_SANDBOX_* (con --sandbox) de /opt/data/.env.
También acepta flags: --client-id --client-secret --refresh-token --region
"""
import os
import sys
import json
import argparse
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path

REGIONS = {
    "na": "https://sellingpartnerapi-na.amazon.com",
    "eu": "https://sellingpartnerapi-eu.amazon.com",
    "fe": "https://sellingpartnerapi-fe.amazon.com",
}
SANDBOX_REGIONS = {
    "na": "https://sandbox.sellingpartnerapi-na.amazon.com",
    "eu": "https://sandbox.sellingpartnerapi-eu.amazon.com",
    "fe": "https://sandbox.sellingpartnerapi-fe.amazon.com",
}
TOKEN_URL = "https://api.amazon.com/auth/o2/token"
USER_AGENT = "NeuralCrew-DigitalExpressions/1.0 (J&N Digital Expressions LLC)"


def load_env():
    """Lee AMAZON_SPAPI_* de /opt/data/.env sin instalar python-dotenv."""
    env_path = Path("/opt/data/.env")
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


def get_access_token(client_id, client_secret, refresh_token):
    data = urllib.parse.urlencode({
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }).encode()
    req = urllib.request.Request(
        TOKEN_URL, data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                 "User-Agent": USER_AGENT},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def call_spapi(endpoint, access_token, region="eu", sandbox=False):
    base = SANDBOX_REGIONS[region] if sandbox else REGIONS[region]
    url = f"{base}{endpoint}"
    req = urllib.request.Request(url, headers={
        "x-amz-access-token": access_token,
        "Content-Type": "application/json",
        "User-Agent": USER_AGENT,
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def main():
    parser = argparse.ArgumentParser(description="Amazon SP-API helper (Digital Expressions)")
    parser.add_argument("--test", action="store_true", help="Smoke test: sellers/v1/marketplaceParticipations")
    parser.add_argument("--endpoint", help="Endpoint SP-API a llamar (ej. /reports/v1/reportTypes)")
    parser.add_argument("--sandbox", action="store_true", help="Usar endpoint sandbox + credenciales AMAZON_SPAPI_SANDBOX_*")
    parser.add_argument("--client-id")
    parser.add_argument("--client-secret")
    parser.add_argument("--refresh-token")
    parser.add_argument("--region", default=None)
    args = parser.parse_args()

    load_env()
    if args.sandbox:
        client_id = args.client_id or os.environ.get("AMAZON_SPAPI_SANDBOX_CLIENT_ID")
        client_secret = args.client_secret or os.environ.get("AMAZON_SPAPI_SANDBOX_CLIENT_SECRET")
        refresh_token = args.refresh_token or os.environ.get("AMAZON_SPAPI_SANDBOX_REFRESH_TOKEN")
        region = args.region or os.environ.get("AMAZON_SPAPI_SANDBOX_REGION", "eu")
    else:
        client_id = args.client_id or os.environ.get("AMAZON_SPAPI_CLIENT_ID")
        client_secret = args.client_secret or os.environ.get("AMAZON_SPAPI_CLIENT_SECRET")
        refresh_token = args.refresh_token or os.environ.get("AMAZON_SPAPI_REFRESH_TOKEN")
        region = args.region or os.environ.get("AMAZON_SPAPI_REGION", "eu")

    if not (client_id and client_secret and refresh_token):
        print("ERROR: faltan credenciales. Configura AMAZON_SPAPI_* en /opt/data/.env o usa flags.")
        sys.exit(1)

    if not args.test and not args.endpoint:
        parser.print_help()
        sys.exit(1)

    try:
        token = get_access_token(client_id, client_secret, refresh_token)
        at = token.get("access_token")
        print(f"✓ Access token obtenido ({token.get('token_type')}, expira en {token.get('expires_in')}s)")

        endpoint = args.endpoint
        if args.test:
            endpoint = "/sellers/v1/marketplaceParticipations"
        result = call_spapi(endpoint, at, region, args.sandbox)
        print(json.dumps(result, indent=2, ensure_ascii=False)[:3000])
    except urllib.error.HTTPError as e:
        print(f"✗ HTTP {e.code}: {e.read().decode()[:1000]}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
