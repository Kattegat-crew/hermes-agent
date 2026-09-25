---
name: amazon-fba-profitability
description: "Use when sizing Amazon FBA product profitability."
tags: [amazon, fba, rentabilidad, ecommerce, pricing, fees, research]
  Complete workflow for evaluating Amazon FBA product profitability:
  cost analysis, fee calculation, competitor research, and pricing strategy.
  Supports multiple marketplaces (AU, US, UK, etc.).
version: 1.0.0
author: Ragnar
license: MIT
metadata:
  hermes:
    tags: [amazon, fba, profitability, e-commerce, pricing, competitor-analysis]
    category: research
    related_skills: [document-reader, brainstorming, executing-plans]
---

# Amazon FBA Profitability Calculator

Flujo completo para evaluar rentabilidad de productos en Amazon FBA.
Incluye: cálculo de fees, investigación de precios de competencia,
y estrategia de pricing óptima.

## Cuándo Usar

- **ALWAYS** al evaluar un nuevo producto para venta en Amazon
- **ALWAYS** al recibir una cotización de proveedor y necesites calcular ROI
- **ALWAYS** al definir precio de venta para un producto nuevo
- **NUNCA** usar como único criterio — validar con investigación de mercado

## Pasos del Workflow

### 1. Recopilar Datos del Producto

Necesitás:
- **Peso estimado** (kg) — SIEMPRE verificar con proveedor
- **Dimensiones** (cm) — para determinar size tier
- **Costo unitario EXW** (USD o moneda local)
- **Cantidad del pedido**
- **Costo de envío total** (DDP/FCL/FCA)
- **Marketplace objetivo** (AU, US, UK, DE, etc.)

```python
# Ejemplo de estructura de datos
product_data = {
    "sku": "PS-3052",
    "name": "Pet Snuffle Mat - Polar Fleece",
    "size": "50x80cm",
    "weight_kg": 0.65,  # VERIFICAR CON PROVEEDOR
    "cost_usd": 5.95,   # EXW unit cost
    "qty": 200,
    "shipping_usd": 750,  # Total shipping (DDP)
    "marketplace": "AU"  # Amazon Australia
}
```

### 2. Calcular Fees del Marketplace

Cada marketplace tiene estructura de fees distinta:

#### Amazon Australia (AU) — Pet Supplies

```python
# Fee structure (AUD, aproximados 2024-2025)
FEE_CONFIG_AU = {
    "category": "Pet Supplies",
    "referral_fee_pct": 0.15,  # 15% del precio de venta
    "referral_fee_min": 4.00,  # Mínimo $4.00 AUD
    
    # FBA Fulfillment Fees (por peso y dimensiones)
    "fba_tiers": {
        0.45: {"name": "Small Parcel", "fee": 8.10},
        0.90: {"name": "Medium Parcel Small", "fee": 11.70},
        1.50: {"name": "Medium Parcel", "fee": 13.50},
        2.00: {"name": "Large Parcel", "fee": 18.90},
        3.00: {"name": "XL Large", "fee": 24.30},
    },
    
    # Storage fee: $44.75 AUD/m³/month
    "storage_per_m3_month": 44.75,
    
    # Exchange rate USD → AUD
    "usd_to_local": 1.55,
}
```

#### Amazon US (ejemplo)

```python
FEE_CONFIG_US = {
    "category": "Pet Supplies",
    "referral_fee_pct": 0.15,
    "referral_fee_min": 0.75,  # $0.75 USD mínimo
    
    "fba_tiers": {
        0.25: {"name": "Small Parcel", "fee": 3.86},
        0.50: {"name": "Medium Small", "fee": 4.75},
        0.90: {"name": "Medium Large", "fee": 5.05},
        1.50: {"name": "Large", "fee": 9.73},
    },
    
    "storage_per_cuft_month": 0.87,  # por foot cúbico
    "usd_to_local": 1.0,
}
```

### 3. Scraping de Competencia

Usar urllib para buscar productos similares en el marketplace:

```python
import urllib.request
import re
from collections import defaultdict

def scrape_competitor_prices(product_keyword, marketplace="AU"):
    """
    Scrapa precios de productos similares en Amazon.
    Retorna diccionario con precio, ratings y título.
    """
    url = f"https://www.amazon.{marketplace.lower()}/s?k={product_keyword}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept-Language': 'en-US,en;q=0.5'
    }
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
        
        # Extraer precios (pattern variable según HTML de Amazon)
        prices = re.findall(r'[\$](\d+\.\d{2})', html)
        
        # Extraer ratings
        ratings = re.findall(r'(\d[\d,]*)\s*ratings?', html)
        
        # Extraer títulos (más difícil con regex puro)
        titles = re.findall(r'<span.*?class="[^"]*title[^"]*"[^>]*>(.*?)</span>', html)
        
        return {
            "prices": [float(p) for p in prices[:20]],  # Top 20 precios
            "ratings": [int(r.replace(',', '')) for r in ratings[:20]],
            "titles": [t.strip() for t in titles[:20]],
        }
    except Exception as e:
        print(f"[!] Error scraping: {e}")
        return None
```

**⚠️ Pitfall CRÍTICO:** Amazon usa protección anti-bots. El scraping por urllib/regex:
- Funciona para precios visibles en la página de búsqueda
- NO extrae títulos detallados de forma confiable
- Puede devolver CAPTCHA o HTML vacío si se detecta automatización
- **Siempre verificar datos manualmente en el navegador**

### 4. Análisis de Rentabilidad

Cálculo completo por unidad:

```python
def calculate_profitability(product_data, fee_config, retail_price):
    """
    Calcula toda la estructura de costos y rentabilidad.
    """
    local_currency_rate = fee_config['usd_to_local']
    
    # Costos base
    cost_local = product_data['cost_usd'] * local_currency_rate
    shipping_per_unit = (product_data['shipping_total'] / product_data['qty']) * local_currency_rate
    landed_cost = cost_local + shipping_per_unit
    
    # Determinar FBA fee por peso
    weight = product_data['weight_kg']
    fba_fee = _get_fba_fee(weight, fee_config['fba_tiers'])
    
    # Referral fee
    referral_fee = max(retail_price * fee_config['referral_fee_pct'], 
                       fee_config['referral_fee_min'])
    
    # Storage (estimado 2 meses promedio)
    volume_m3 = 0.02  # Estimación conservadora
    storage_fee_2months = volume_m3 * fee_config.get('storage_per_m3_month', 44.75) * 2
    
    # Totales
    total_fees = fba_fee + referral_fee + storage_fee_2months
    profit = retail_price - landed_cost - total_fees
    margin = (profit / retail_price) * 100
    
    # Break-even
    break_even = landed_cost + fba_fee + referral_fee + storage_fee_2months
    
    # Ajustar por PPC y devoluciones
    ppc_pct = 0.15  # 15% del precio (publicidad)
    return_rate = 0.04  # 4% devoluciones (estimado)
    
    adjusted_profit = profit - (retail_price * ppc_pct) - (retail_price * return_rate)
    adjusted_margin = (adjusted_profit / retail_price) * 100
    
    return {
        "landed_cost": landed_cost,
        "fba_fee": fba_fee,
        "referral_fee": referral_fee,
        "storage_fee": storage_fee_2months,
        "total_fees": total_fees,
        "retail_price": retail_price,
        "profit_before_ad": profit,
        "margin_before_ad": margin,
        "profit_after_ad": adjusted_profit,
        "margin_after_ad": adjusted_margin,
        "break_even": break_even,
        "fba_tier": _get_fba_tier_name(weight, fee_config['fba_tiers']),
    }

def _get_fba_fee(weight, tiers):
    for max_weight, tier_data in tiers.items():
        if weight <= max_weight:
            return tier_data['fee']
    return list(tiers.values())[-1]['fee']  # Última tier como fallback

def _get_fba_tier_name(weight, tiers):
    for max_weight, tier_data in tiers.items():
        if weight <= max_weight:
            return tier_data['name']
    return list(tiers.values())[-1]['name']
```

### 5. Análisis de Mercado y Recomendación

```python
def analyze_market_data(scraped_data, fee_config, product_weight):
    """
    Analiza datos de mercado y sugiere precio óptimo.
    """
    if not scraped_data or not scraped_data['prices']:
        return "Sin datos de mercado suficientes para recomendar precio"
    
    prices = sorted(scraped_data['prices'])
    ratings = scraped_data.get('ratings', [])
    
    # Estadísticas de precios
    min_price = min(prices)
    max_price = max(prices)
    median_price = prices[len(prices) // 2]
    
    # Analizar demanda por bracket de precio
    bracket_demand = defaultdict(list)
    for price in prices:
        bracket = (int(price // 10) * 10)
        bracket_demand[bracket].append(1)
    
    # Determinar posición de tu producto
    # Si tu producto es premium (mejor material), apunta al top 30% de precios
    is_premium_material = product_weight > 0.5  # Ejemplo: más peso = mejor material
    
    if is_premium_material:
        target_price = max_price * 0.85  # 15% debajo del más caro
    else:
        target_price = median_price  # Precio mediano para producto estándar
    
    return {
        "min_price": min_price,
        "max_price": max_price,
        "median_price": median_price,
        "recommended_price": round(target_price, 2),
        "market_insight": f"El mercado oscila entre {min_price} y {max_price}. "
                          f"Tu producto {'premium' if is_premium_material else 'estándar'} "
                          f"debería posicionarse en ~${target_price}",
    }
```

### 6. Presentación de Resultados

Generar un reporte claro con:

```
=== ANÁLISIS DE RENTABILIDAD ===

Producto: PS-3052 (Pet Snuffle Mat 50x80cm)
Marketplace: Amazon Australia
Peso: 0.65kg (TIER: Medium Parcel Small)

COSTOS:
├─ Costo producto: $9.22 AUD
├─ Envío DDP: $2.91 AUD
└─ Costo Landed: $12.13 AUD

FEES AMAZON:
├─ FBA Fee: $11.70 AUD
├─ Referral (15%): $4.50 AUD
├─ Storage (2 meses): $1.79 AUD
└─ Total Fees: $17.99 AUD

PRECIOS Y MARGENES:
├─ Break-even: $30.12 AUD
├─ Precio target: $29.99 AUD
├─ Ganancia (bruta): -$0.13 AUD (-0.4%) ❌
├─ Ganancia (neto con PPC 15% + 4% devs): -$3.33 AUD
└─ Precio recomendado: $35+ AUD → +$4.13 AUD (11.8%)

DATOS DE MERCADO:
├─ Rango de competencia: $15 - $85 AUD
├─ Mayoría precios: $15 - $27 AUD
├─ Posición del producto: Top 5% (premium)
└─ Conclusión: ✅ Justificable a $80 AUD si calidad es superior
```

## Datos de Referencia por Marketplace

### Amazon Australia (AU) — Pet Supplies

| Tier | Peso Máx | FBA Fee | Ejemplo |
|------|----------|---------|---------|
| Small Parcel | ≤450g | $8.10 | PS-3095 (0.45kg) |
| Med Small | ≤900g | $11.70 | PS-3052 (0.65kg) |
| Medium | ≤1.5kg | $13.50 | — |
| Large | ≤2kg | $18.90 | — |

- **Referral Fee:** 15% (mín $4.00)
- **Storage:** $44.75 AUD/m³/month
- **Exchange:** 1 USD ≈ 1.55 AUD

### Amazon US — Pet Supplies

| Tier | Peso Máx | FBA Fee |
|------|----------|---------|
| Small | ≤250g | $3.86 |
| Med Small | ≤500g | $4.75 |
| Med Large | ≤900g | $5.05 |
| Large | ≤1.5kg | $9.73 |

- **Referral Fee:** 15% (mín $0.75)
- **Storage:** $0.87/cuft/month

### Amazon UK — Pet Supplies

| Tier | Peso Máx | FBA Fee |
|------|----------|---------|
| Small | ≤400g | £6.00 |
| Med Small | ≤900g | £8.50 |
| Medium | ≤1.5kg | £10.50 |
| Large | ≤2kg | £14.50 |

- **Referral Fee:** 15% (mín £2.00)
- **Storage:** £45/m³/month
- **Exchange:** 1 USD ≈ 0.79 GBP

## Pitfalls

- **❌ Nunca confiar en peso estimado sin verificar con proveedor** — Un kg extra cambia tu tier de FBA y puede eliminar la rentabilidad.
- **❌ No asumir que scraping = datos confiables** — Amazon cambia su HTML constantemente. Validar siempre manualmente.
- **❌ No incluir PPC en análisis inicial** — El costo de publicidad es variable (10-20% del precio). Separar análisis bruto vs neto.
- **❌ No subestimar devoluciones** — En pet supplies, 3-5% es conservador. Productos baratos tienen mayor tasa de devolución.
- **❌ No calcular ROI sin considerar tiempo** — Un producto con 15% de margen pero que tarda 6 meses en rotar puede no valer la pena.
- **✅ Siempre incluir storage fee en cálculo** — El 2-3 meses promedio es un buen estimador.
- **✅ Calcular break-even antes de fijar precio** — Sabé el mínimo antes de negociar con el proveedor.
- **✅ Usar datos de mercado para validar tu precio** — Si nadie vende a $80, tu justificación premium debe ser sólida.

## Integración con document-reader

Usar `document-reader` para extraer datos de cotizaciones de proveedores:

```bash
python3 /opt/data/skills/document-reader/scripts/parse_document.py \
  /path/to/quotation.pdf --format json
```

Extraer:
- Unit cost
- Quantity
- Carton dimensions (para calcular volumen)
- Material descriptions (para determinar si es premium)

## Integración con persistent-task-manager

Crear tarea en Notion + Brain Wiki para seguimiento:

```python
# Leer Notion DB properties para crear correctamente
resp = requests.get('https://api.notion.com/v1/databases/{db_id}', headers=notion_headers)
properties = resp.json()['properties']
# Extraer: Nombre (title), Estado (status), Prioridad (select), Módulo (select)

# Crear página con valores existentes
resp = requests.post('https://api.notion.com/v1/pages', json={
    'parent': {'database_id': '349853a7-3369-8139-a73e-d0e4213c215c'},
    'properties': {
        'Nombre': {'title': [{'text': {'content': 'Tarea'}}]},
        'Estado': {'status': {'name': 'Sin empezar'}},
        'Prioridad': {'select': {'name': 'Alta'}},
        'Módulo': {'select': {'name': 'Infraestructura'}}
    }
}, headers=notion_headers)
```

## Referencias

- **FEEDS API docs:** https://developer-docs.amazon.com/sp-api/
- **Amazon FBA Fee Calculator:** https://seller.amazon.com (login requerido)
- **Marketplace API:** https://github.com/amzn/selling-partner-api-docs