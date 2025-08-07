import csv
import json
from datetime import datetime

TOKENS_CSV = "grid_hold_output/step_3_3_selected_tokens.csv"
OUTPUT_FILE = "grid_hold_output/strategy_recommendation.json"

def load_tokens():
    with open(TOKENS_CSV, "r") as f:
        reader = csv.DictReader(f)
        return list(reader)

def select_best_token(tokens):
    # Sort by step_pct descending
    sorted_tokens = sorted(tokens, key=lambda x: float(x["step_pct"]), reverse=True)
    return sorted_tokens[0] if sorted_tokens else None

def save_recommendation(token):
    result = {
        "timestamp": datetime.utcnow().isoformat(),
        "symbol": token["symbol"],
        "grid_roi": token["grid_roi"],
        "hold_roi": token["hold_roi"],
        "step_pct": token["step_pct"]
    }
    with open(OUTPUT_FILE, "w") as f:
        json.dump(result, f, indent=2)

def main():
    tokens = load_tokens()
    best_token = select_best_token(tokens)
    if best_token:
        save_recommendation(best_token)
        print(f"✅ Best token selected: {best_token['symbol']} with Step % = {best_token['step_pct']}")
        print(f"📄 Saved to: {OUTPUT_FILE}")
    else:
        print("❌ No tokens available to select.")

if __name__ == "__main__":
    main()
