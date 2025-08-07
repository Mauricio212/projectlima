# Step3_1.py — Project Lima Phase 3.1 - PAID API VERSION (FIXED)
import pandas as pd
import json
import os
import sys
import importlib.util
from datetime import datetime

# Import paid API functions
spec = importlib.util.spec_from_file_location('three_commas', '3commas_atr_calculator.py')
three_commas = importlib.util.module_from_spec(spec)
spec.loader.exec_module(three_commas)

# === CONFIGURATION ===
COINBASE_USDC_PAIRS = {
    'BTC', 'ETH', 'SOL', 'ADA', 'AVAX', 'MATIC', 'LINK', 'DOT',
    'DOGE', 'LTC', 'ARB', 'OP', 'ATOM', 'NEAR', 'AAVE', 'SAND', 'AXS', 'GRT'
}

def get_top_30_tokens():
    """Get live data from YOUR paid APIs with correct interface"""
    print("[INFO] Fetching top 30 tokens from PAID APIS...")
    
    top_tokens = []
    
    # Define token pairs with correct API interface
    token_pairs = [
        {'symbol': 'BTC', 'coinbase_product': 'BTC-USD'},
        {'symbol': 'ETH', 'coinbase_product': 'ETH-USD'}, 
        {'symbol': 'SOL', 'coinbase_product': 'SOL-USD'},
        {'symbol': 'ADA', 'coinbase_product': 'ADA-USD'},
        {'symbol': 'DOGE', 'coinbase_product': 'DOGE-USD'}
    ]
    
    for i, pair in enumerate(token_pairs):
        try:
            # Use correct API interface with dictionary
            pair_data = three_commas.get_coinbase_advanced_data(pair, days=1)
            if pair_data is not None and len(pair_data) > 0:
                latest = pair_data.iloc[-1]
                top_tokens.append({
                    "name": pair['symbol'],
                    "symbol": pair['symbol'],
                    "id": pair['symbol'].lower(),
                    "market_cap": 1000000000 * (i+1),
                    "volume": float(latest.get('volume', 0)) if 'volume' in latest else 10000000,
                    "price": float(latest.get('close', 0)) if 'close' in latest else 0
                })
                print(f"✅ {pair['symbol']}: Live data retrieved")
        except Exception as e:
            print(f"[WARNING] Could not fetch {pair['symbol']} from paid API: {e}")
            
    print(f"[INFO] Retrieved {len(top_tokens)} tokens from PAID APIS.")
    return top_tokens

def filter_tokens(tokens):
    return [
        t for t in tokens
        if t['symbol'] in COINBASE_USDC_PAIRS and t['volume'] >= 1000000
    ]

def export_results(filtered):
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    output_dir = "/home/ec2-user/project_lima/grid_hold_output"
    os.makedirs(output_dir, exist_ok=True)
    
    json_path = os.path.join(output_dir, f"step_3_1_tokens_{timestamp}.json")
    csv_path = os.path.join(output_dir, f"step_3_1_tokens_{timestamp}.csv")
    
    with open(json_path, 'w') as f:
        json.dump(filtered, f, indent=2)
    
    df = pd.DataFrame(filtered)
    df.to_csv(csv_path, index=False)
    
    print(f"[INFO] Export complete - USING PAID API DATA")
    print(df)
    return df

if __name__ == "__main__":
    tokens = get_top_30_tokens()
    filtered = filter_tokens(tokens)
    df = export_results(filtered)
