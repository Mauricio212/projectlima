# fix_grid_failure_debugger.py

import pandas as pd
from pathlib import Path
from datetime import datetime

# === CONFIG ===
roi_file = Path("/home/ec2-user/project_lima/grid_hold_output/step_3_2_token_roi.csv")
config_file = Path("/home/ec2-user/project_lima/grid_hold_output/grid_config.csv")  # contains GRID setup info
price_file = Path("/home/ec2-user/project_lima/price_data.csv")  # historical prices
log_file = Path("/home/ec2-user/project_lima/logs/fix_grid_failure_debug_log.csv")

def load_files():
    df_roi = pd.read_csv(roi_file)
    df_config = pd.read_csv(config_file)
    df_price = pd.read_csv(price_file)
    return df_roi, df_config, df_price

def diagnose(token, df_roi, df_config, df_price):
    result = {}
    roi_row = df_roi[df_roi["symbol"].str.upper() == token.upper()]
    config_row = df_config[df_config["symbol"].str.upper() == token.upper()]
    price_row = df_price[df_price["symbol"].str.upper() == token.upper()]

    if roi_row.empty or config_row.empty or price_row.empty:
        result["error"] = f"Missing data for token {token}"
        return result

    grid_roi = float(roi_row["grid_roi"].values[0])
    hold_roi = float(roi_row["hold_roi"].values[0])
    result["grid_roi"] = grid_roi
    result["hold_roi"] = hold_roi

    if grid_roi > hold_roi:
        result["status"] = "✅ GRID outperformed HOLD — no diagnostic needed."
        return result

    # === DIAGNOSTICS BEGIN ===
    step_pct = float(config_row["step_pct"].values[0])
    grid_min = float(config_row["price_min"].values[0])
    grid_max = float(config_row["price_max"].values[0])
    grid_count = int(config_row["grid_count"].values[0])
    capital_per_grid = float(config_row["capital_per_grid"].values[0])
    fee_pct = 0.15

    result["status"] = "❌ GRID underperformed HOLD — diagnosing root cause..."

    # Step 1: Price behavior
    high_price = price_row["high"].max()
    low_price = price_row["low"].min()
    consolidation_range = (high_price - low_price) / low_price * 100
    result["price_behavior"] = f"Price range = {consolidation_range:.2f}%"
    if consolidation_range > 20:
        result["issue_price"] = "Pair was trending — HOLD advantage may be valid"
    else:
        result["issue_price"] = "Confirmed consolidation"

    # Step 2: Step %
    result["step_pct"] = f"{step_pct:.2f}%"
    if step_pct < 1.5:
        result["issue_step"] = "Step % too low — overtrading + fees"
    elif step_pct > 5:
        result["issue_step"] = "Step % too high — missed volatility"
    else:
        result["issue_step"] = "Step % ideal"

    # Step 3: Price range fit
    median_price = (high_price + low_price) / 2
    ideal_low = median_price * 0.88
    ideal_high = median_price * 1.12
    result["grid_range"] = f"Configured: {grid_min}–{grid_max}, Ideal: {ideal_low:.2f}–{ideal_high:.2f}"
    if grid_min > low_price or grid_max < high_price:
        result["issue_range"] = "Price exited GRID range — missed trades or freeze"
    else:
        result["issue_range"] = "Price range acceptable"

    # Step 4: Grids/capital
    result["grid_count"] = grid_count
    result["capital_per_grid"] = capital_per_grid
    if grid_count < 10 or grid_count > 100:
        result["issue_grid_count"] = "Inefficient grid count"
    else:
        result["issue_grid_count"] = "Grid count acceptable"
    if capital_per_grid < 10:
        result["issue_capital"] = "Too little capital per grid"
    else:
        result["issue_capital"] = "Capital per grid OK"

    # Step 5: Fee impact
    net_step = step_pct - fee_pct
    result["net_step_after_fee"] = f"{net_step:.2f}%"
    if net_step < 1.35:
        result["issue_fees"] = "Step % too close to fee — net ROI likely crushed"
    else:
        result["issue_fees"] = "Fee-adjusted profit OK"

    return result

def run_debugger(token):
    df_roi, df_config, df_price = load_files()
    report = diagnose(token, df_roi, df_config, df_price)

    print("\n🔍 GRID-HOLD ROI Diagnostic Report")
    for k, v in report.items():
        print(f"{k}: {v}")

    # Save log
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with log_file.open("a") as f:
        f.write(f"{datetime.utcnow().isoformat()},{token},{report.get('status','')},{report.get('grid_roi','')},{report.get('hold_roi','')}\n")

if __name__ == "__main__":
    token = input("Enter token symbol to diagnose (e.g. BTC): ").strip()
    run_debugger(token)
