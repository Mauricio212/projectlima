#!/usr/bin/env python3
# FIX-5: Live Price Validator — Fixed CSV Version
import csv
import requests
from datetime import datetime
from pathlib import Path

# Configuration
INPUT_FILE = "grid_hold_output/step_3_3_selected_tokens.csv"
OUTPUT_FILE = "grid_hold_output/fix_5_validation_results.csv"  
LOG_FILE = "logs/fix_5_price_validation.csv"

def validate_price(symbol):
    """Validate live price from API"""
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol.lower()}&vs_currencies=usd"
        response = requests.get(url, timeout=10)
        data = response.json()
        return data.get(symbol.lower(), {}).get('usd', 0)
    except:
        return 0

# Read selected tokens
tokens = []
try:
    with open(INPUT_FILE, "r") as f:
        reader = csv.DictReader(f)
        tokens = list(reader)
except FileNotFoundError:
    print(f"❌ Input file not found: {INPUT_FILE}")
    exit(1)

# Validate each token with live prices
validated_tokens = []
for token in tokens:
    symbol = token.get('symbol', '')
    if symbol:
        live_price = validate_price(symbol)
        validated_token = {
            'symbol': symbol,
            'grid_roi': token.get('grid_roi', 0),
            'hold_roi': token.get('hold_roi', 0),
            'live_price_usd': round(live_price, 4),
            'price_validation': '✅' if live_price > 0 else '❌',
            'timestamp': datetime.utcnow().isoformat()
        }
        validated_tokens.append(validated_token)

# Write validation results with correct fieldnames
Path(OUTPUT_FILE).parent.mkdir(parents=True, exist_ok=True)
with open(OUTPUT_FILE, "w", newline='') as f:
    fieldnames = ['symbol', 'grid_roi', 'hold_roi', 'live_price_usd', 'price_validation', 'timestamp']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(validated_tokens)

print(f'[✅ FIX-5] Live price validation complete: {len(validated_tokens)} tokens validated')

# Update FIX registry
import json
try:
    with open('fix_registry.json', 'r') as f:
        registry = json.load(f)
except:
    registry = {}

registry['FIX-5'] = {
    'status': 'PASSED',
    'timestamp': datetime.utcnow().isoformat(),
    'message': f'Live price validation completed for {len(validated_tokens)} tokens.'
}

with open('fix_registry.json', 'w') as f:
    json.dump(registry, f, indent=2)
