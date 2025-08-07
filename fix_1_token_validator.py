#!/usr/bin/env python3
# ✅ FIX-1: Token Validator — Project Lima Golden Rule Certified

import csv
import requests
from datetime import datetime
from pathlib import Path

import glob; INPUT_FILE = max(glob.glob("grid_hold_output/step_3_1_tokens_*.csv"))
OUTPUT_FILE = "grid_hold_output/step_3_1_tokens.csv"
VALID_TOKENS = []
MIN_ATR_PCT = 7
MAX_ATR_PCT = 15
MAX_MARKET_CAP_RANK = 30

def read_top_30():
    with open(INPUT_FILE, "r") as f:
        return list(csv.DictReader(f))

def validate_token(token):
    try:
        atr = float(token.get("ATR_14d_Pct", 0))
        rank = int(token.get("MarketCapRank", 999))
        return (
            MIN_ATR_PCT <= atr <= MAX_ATR_PCT
            and rank <= MAX_MARKET_CAP_RANK
        )
    except:
        return False

def write_output(valid_tokens):
    Path("grid_hold_output").mkdir(exist_ok=True)
    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Token", "ATR_14d_Pct", "MarketCapRank"])
        writer.writeheader()
        writer.writerows(valid_tokens)

if __name__ == "__main__":
    tokens = read_top_30()
    VALID_TOKENS = [t for t in tokens if validate_token(t)]
    write_output(VALID_TOKENS)
    print(f"✅ FIX-1 complete. {len(VALID_TOKENS)} valid tokens written to: {OUTPUT_FILE}")

