# build_grid_config.py

import pandas as pd
from pathlib import Path

# Paths
token_file = max(Path("/home/ec2-user/project_lima/grid_hold_output").glob("step_3_1_tokens_*.csv"))
price_file = Path("/home/ec2-user/project_lima/price_data.csv")
output_path = Path("/home/ec2-user/project_lima/grid_hold_output/grid_config.csv")

# Defaults
STEP_PCT = 2.0
GRID_COUNT = 30
CAPITAL_PER_GRID = 15.0

# Load token list and price data
df_tokens = pd.read_csv(token_file)
df_price = pd.read_csv(price_file)

configs = []

for _, row in df_tokens.iterrows():
    symbol = row["symbol"]
    price_row = df_price[df_price["symbol"].str.upper() == symbol.upper()]
    if price_row.empty:
        print(f"⚠️ Missing price data for {symbol}, skipping.")
        continue

    high = float(price_row["high"].max())
    low = float(price_row["low"].min())
    median = (high + low) / 2
    price_min = round(median * 0.90, 4)
    price_max = round(median * 1.10, 4)

    configs.append({
        "symbol": symbol,
        "price_min": price_min,
        "price_max": price_max,
        "step_pct": STEP_PCT,
        "grid_count": GRID_COUNT,
        "capital_per_grid": CAPITAL_PER_GRID
    })

# Save output
df_config = pd.DataFrame(configs)
df_config.to_csv(output_path, index=False)

print(f"[✅ GRID CONFIG GENERATED] {output_path} with {len(df_config)} tokens.")
