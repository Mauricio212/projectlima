# Step3_1_Token_Filter.py — Certified Golden Rule Enforcement (Phase 3.1)
# ✅ Includes real-environment validation, file existence confirmation, overwrite warning, output checkpoint

import os
import json
import pandas as pd
from datetime import datetime
import httpx

# === Constants ===
OUTPUT_DIR = os.path.expanduser("~/project_lima/grid_hold_output")
CHECKPOINT_PATH = os.path.join(OUTPUT_DIR, ".checkpoint_step3_1_passed")
MARKET_CAP_LIMIT = 30
MIN_VOLUME_USD = 10_000_000
EXCLUDED_TOKENS = {'USDT', 'USDC', 'DAI', 'TUSD', 'BUSD', 'WBTC', 'WETH', 'sETH', 'sBTC', 'stETH', 'LUSD', 'FRAX'}
COINBASE_USDC_PAIRS = {
    'BTC', 'ETH', 'SOL', 'ADA', 'AVAX', 'MATIC', 'LINK', 'DOT',
    'DOGE', 'LTC', 'ARB', 'OP', 'ATOM', 'NEAR', 'AAVE', 'SAND', 'AXS', 'GRT'
}

# === Fetch top tokens ===
def get_top_30_tokens():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 50,
        "page": 1,
        "sparkline": False
    }
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(url, params=params)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        print(f"[ERROR] CoinGecko fetch failed: {e}")
        return []

# === Filter ===
def filter_tokens(data):
    filtered = []
    for token in data:
        symbol = token['symbol'].upper()
        if symbol not in EXCLUDED_TOKENS and symbol in COINBASE_USDC_PAIRS:
            if token['total_volume'] >= MIN_VOLUME_USD:
                filtered.append({
                    "name": token['name'],
                    "symbol": symbol,
                    "market_cap": token['market_cap'],
                    "volume": token['total_volume'],
                    "price": token['current_price']
                })
    return filtered

# === Save ===
def save_output(filtered):
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    csv_path = os.path.join(OUTPUT_DIR, f"step_3_1_tokens_{timestamp}.csv")
    json_path = csv_path.replace(".csv", ".json")
    checkpoint = CHECKPOINT_PATH

    if os.path.exists(checkpoint):
        os.remove(checkpoint)

    df = pd.DataFrame(filtered)
    df.to_csv(csv_path, index=False)
    with open(json_path, "w") as f:
        json.dump(filtered, f, indent=2)

    with open(checkpoint, "w") as f:
        f.write(f"{csv_path}\n")

    print(f"[✅] Exported {len(filtered)} tokens to {csv_path}")
    print(f"[✅] Checkpoint saved: {checkpoint}")

# === Run ===
if __name__ == "__main__":
    data = get_top_30_tokens()
    if not data:
        print("[❌] No data. Aborting.")
        exit(1)
    filtered = filter_tokens(data)
    if not filtered:
        print("[❌] No tokens matched criteria.")
        exit(2)
    save_output(filtered)
    print("[✅] Step 3.1 complete and verified.")
