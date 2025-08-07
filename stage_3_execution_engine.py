#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import csv
import json
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

# === File Paths ===
SELECTED_TOKENS_CSV = "grid_hold_output/step_3_3_selected_tokens.csv"
STRATEGY_JSON = "grid_hold_output/strategy_recommendation.json"
OUTPUT_LOG_CSV = "grid_hold_output/grid_simulation_log.csv"
SUMMARY_JSON = "grid_hold_output/grid_execution_summary.json"

# === Constants ===
CAPITAL = Decimal("1000.00")
ROUNDING = Decimal("0.0001")

# === Helpers ===
def round_d(value):
    return float(Decimal(value).quantize(ROUNDING, rounding=ROUND_HALF_UP))

def load_strategy():
    with open(STRATEGY_JSON, "r") as f:
        return json.load(f)

def load_selected_tokens():
    with open(SELECTED_TOKENS_CSV, "r") as f:
        reader = csv.DictReader(f)
        return list(reader)

def simulate_grid_trades(token: dict, capital: Decimal):
    try:
        grid_roi = Decimal(token["grid_roi"])
        step_pct = Decimal(token["step_pct"])
        symbol = token["symbol"]

        # Simulate trade loop
        step_gain = (capital * step_pct).quantize(ROUNDING, rounding=ROUND_HALF_UP)
        estimated_trades = int(grid_roi / step_pct)
        total_profit = step_gain * estimated_trades
        final_value = capital + total_profit

        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "symbol": symbol,
            "initial_capital": float(capital),
            "step_pct": float(step_pct),
            "grid_roi": float(grid_roi),
            "estimated_trades": estimated_trades,
            "profit": float(total_profit),
            "final_value": float(final_value),
        }

        return log_entry

    except Exception as e:
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "symbol": token.get("symbol", "UNKNOWN"),
            "error": str(e)
        }

def write_log(log_rows):
    fieldnames = list(log_rows[0].keys())
    with open(OUTPUT_LOG_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in log_rows:
            writer.writerow(row)

def write_summary(log_rows):
    summary = {
        "timestamp": datetime.utcnow().isoformat(),
        "token_count": len(log_rows),
        "total_estimated_profit": float(sum(Decimal(str(r["profit"])) for r in log_rows if "profit" in r)),
        "log_file": OUTPUT_LOG_CSV
    }
    with open(SUMMARY_JSON, "w") as f:
        json.dump(summary, f, indent=2)

# === Main ===
def main():
    print("🔁 Loading strategy and tokens...")
    strategy = load_strategy()
    selected_symbol = strategy["symbol"]
    tokens = load_selected_tokens()

    log_entries = []
    for token in tokens:
        if token["symbol"] == selected_symbol:
            log_entry = simulate_grid_trades(token, CAPITAL)
            log_entries.append(log_entry)

    if not log_entries:
        print("❌ No matching token found for simulation.")
        return

    write_log(log_entries)
    write_summary(log_entries)
    print(f"✅ Execution complete. Results:")
    print(f"   → Log: {OUTPUT_LOG_CSV}")
    print(f"   → Summary: {SUMMARY_JSON}")

if __name__ == "__main__":
    main()
