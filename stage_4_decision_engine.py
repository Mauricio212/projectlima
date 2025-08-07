import json
import os
from datetime import datetime

STRATEGY_FILE = "grid_hold_output/strategy_recommendation.json"
DECISION_FILE = "grid_hold_output/decision_summary.json"

def load_strategy():
    with open(STRATEGY_FILE, "r") as f:
        return json.load(f)

def decide(strategy):
    symbol = strategy["symbol"]
    grid_roi = float(strategy["grid_roi"])
    hold_roi = float(strategy["hold_roi"])
    step_pct = float(strategy["step_pct"])

    if grid_roi > hold_roi:
        decision = "INVEST IN GRID"
        reason = f"GRID ROI = {grid_roi}% vs HOLD ROI = {hold_roi}%, with Step % = {step_pct}"
    else:
        decision = "HOLD"
        reason = f"HOLD ROI = {hold_roi}% vs GRID ROI = {grid_roi}%, Step % = {step_pct}"

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "symbol": symbol,
        "decision": decision,
        "reason": reason,
        "grid_roi": grid_roi,
        "hold_roi": hold_roi,
        "step_pct": step_pct
    }

def safe_write_json(data, filepath):
    try:
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
            f.flush()
            os.fsync(f.fileno())
    except Exception as e:
        print(f"❌ ERROR saving decision file: {e}")
        raise

def main():
    strategy = load_strategy()
    decision = decide(strategy)
    safe_write_json(decision, DECISION_FILE)
    print(f"✅ DECISION: {decision['decision']}")
    print(f"📊 {decision['reason']}")
    print(f"📝 Saved to: {DECISION_FILE}")

if __name__ == "__main__":
    main()
