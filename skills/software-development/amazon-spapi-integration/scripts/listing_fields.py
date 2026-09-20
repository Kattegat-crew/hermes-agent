#!/usr/bin/env python3
"""
listing_fields.py - Descarga el esquema real de campos para crear listings perfectos.
Amazon SP-API · Product Type Definitions API v2020-09-01 · Digital Expressions 2026-08-18

Uso:
    python3 listing_fields.py --product-type PET_PRODUCTS          # lista campos requeridos
    python3 listing_fields.py --product-type PET_PRODUCTS --full   # todos los campos (requeridos+opcionales)
    python3 listing_fields.py --search "pet"                       # buscar product types disponibles
    python3 listing_fields.py --product-type PET_PRODUCTS --payload # genera plantilla de payload PUT lista para llenar

Requisito: credenciales de PRODUCCIÓN en /opt/data/.env (AMAZON_SPAPI_CLIENT_ID, _SECRET, _REFRESH_TOKEN).
El sandbox estático rechaza este endpoint.
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
TOKEN_URL = "https://api.amazon.com/auth/o2/token"
USER_AGENT = "NeuralCrew-DigitalExpressions/1.0 (J&N Digital Expressions LLC)"
API_ROOT = "/definitions/2020-09-01"
MARKETPLACE_DEFAULT = "A39IBJ37TRP1C6"  # Amazon AU


def load_env():
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


def call_api(endpoint, access_token, region="eu"):
    url = f"{REGIONS[region]}{endpoint}"
    req = urllib.request.Request(url, headers={
        "x-amz-access-token": access_token,
        "Content-Type": "application/json",
        "User-Agent": USER_AGENT,
    })
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode())


def search_product_types(access_token, keyword, region, marketplace_ids):
    ep = f"{API_ROOT}/productTypes?marketplaceIds={marketplace_ids}&keywords={urllib.parse.quote(keyword)}"
    return call_api(ep, access_token, region)


def get_definition(access_token, product_type, region, marketplace_ids, requirements="LISTING"):
    ep = (f"{API_ROOT}/productTypes/{urllib.parse.quote(product_type)}"
          f"?marketplaceIds={marketplace_ids}&requirements={requirements}&locale=en_US")
    return call_api(ep, access_token, region)


def extract_fields(schema, full=False):
    fields = []
    props = schema.get("properties", {})
    required = set(schema.get("required", []))
    for name, p in props.items():
        if isinstance(p, dict):
            is_required = name in required
            if not full and not is_required:
                continue
            ref = p.get("$ref", "")
            ptype = p.get("type", ref.split("/")[-1] if ref else "object")
            constraints = []
            for c in ["maxLength", "minLength", "maximum", "minimum", "maxItems", "pattern"]:
                if c in p:
                    constraints.append(f"{c}={p[c]}")
            fields.append({
                "name": name,
                "required": is_required,
                "type": ptype,
                "constraints": ", ".join(constraints),
                "description": (p.get("description") or "")[:150],
            })
    return fields


def build_payload_template(fields):
    attributes = {}
    for f in fields:
        if f["required"]:
            attributes[f["name"]] = f"__{f['name'].upper()}__"
    return {
        "productType": "PET_PRODUCTS",
        "requirements": "LISTING",
        "attributes": attributes,
    }


def main():
    parser = argparse.ArgumentParser(description="Product Type Definitions helper (listings perfectos)")
    parser.add_argument("--product-type", help="Tipo de producto (ej. PET_PRODUCTS)")
    parser.add_argument("--search", help="Buscar product types por keyword")
    parser.add_argument("--full", action="store_true", help="Incluir campos opcionales")
    parser.add_argument("--payload", action="store_true", help="Generar plantilla de payload")
    parser.add_argument("--marketplace-ids", default=MARKETPLACE_DEFAULT)
    parser.add_argument("--region", default="eu")
    parser.add_argument("--client-id")
    parser.add_argument("--client-secret")
    parser.add_argument("--refresh-token")
    args = parser.parse_args()

    load_env()
    client_id = args.client_id or os.environ.get("AMAZON_SPAPI_CLIENT_ID")
    client_secret = args.client_secret or os.environ.get("AMAZON_SPAPI_CLIENT_SECRET")
    refresh_token = args.refresh_token or os.environ.get("AMAZON_SPAPI_REFRESH_TOKEN")

    if not (client_id and client_secret and refresh_token):
        print("ERROR: faltan credenciales de PRODUCCIÓN. Configura AMAZON_SPAPI_* en /opt/data/.env")
        sys.exit(1)

    try:
        token = get_access_token(client_id, client_secret, refresh_token)
        at = token.get("access_token")

        if args.search:
            data = search_product_types(at, args.search, args.region, args.marketplace_ids)
            types = data.get("productTypes", [])
            print(f"=== Product types que contienen '{args.search}' ===")
            for t in types:
                print(f"- {t.get('displayName', '?')}  (productType: {t.get('name', '?')})")
            sys.exit(0)

        if not args.product_type:
            parser.print_help()
            sys.exit(1)

        schema = get_definition(at, args.product_type, args.region, args.marketplace_ids)
        schema_body = schema.get("schema", schema)
        fields = extract_fields(schema_body, full=args.full)
        req_count = len([f for f in fields if f["required"]])
        print(f"=== {args.product_type} — {len(fields)} campos "
              f"({'REQUERIDOS' if not args.full else 'requeridos+opcionales'}; requeridos: {req_count}) ===")
        for f in fields:
            flag = "[REQ]" if f["required"] else "[opt]"
            extra = f" | {f['constraints']}" if f["constraints"] else ""
            print(f"{flag} {f['name']} ({f['type']}){extra}")
            if f["description"]:
                print(f"      {f['description']}")

        if args.payload:
            print("\n=== PLANTILLA PAYLOAD PUT /listings/2021-08-01/items/{sellerId}/{sku} ===")
            print(json.dumps(build_payload_template(fields), indent=2, ensure_ascii=False))

    except urllib.error.HTTPError as e:
        print(f"✗ HTTP {e.code}: {e.read().decode()[:1500]}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
