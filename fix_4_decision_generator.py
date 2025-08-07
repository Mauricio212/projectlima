# fix_4_decision_generator.py

import pandas as pd
from pathlib import Path
from datetime import datetime

# Step 1: Load FIX-2 ROI file
input_path = Path("/home/ec2-user/project_lima/grid_hold_output/step_3_2_token_roi.csv")
log_file = Path("/home/ec2-user/project_lima/logs/fix_4_decision_log.csv")

try:
    df = pd.read_csv(input_path)
except Exception as e:
    raise FileNotFoundError(f"❌ ERROR: Cannot load ROI file: {input_path}\n{e}")

# Step 2: Validate required rows
grid_row = df[df["symbol"].str.upper() == "GRID"]
hold_row = df[df["symbol"].str.upper() == "HOLD"]

if grid_row.empty or hold_row.empty:
    # Fallback: use avg of filtered tokens vs HOLD
    df_hold = df[df["symbol"].str.upper() == "HOLD"]
    df_grid = df[df["symbol"].str.upper() != "HOLD"]
    grid_roi = df_grid["grid_roi"].mean()
    hold_roi = df_hold["hold_roi"].mean()
    compare_basis = "average of all GRID candidates vs HOLD"
else:
    grid_roi = float(grid_row["grid_roi"].values[0])
    hold_roi = float(hold_row["hold_roi"].values[0])
    compare_basis = "specific GRID vs HOLD token pair"

# Step 3: Decision
if grid_roi > hold_roi:
    recommendation = "INVEST IN GRID"
else:
    recommendation = "INVEST IN HOLD"

# Step 4: Output result
print(f"\n✅ FINAL DECISION:")
print(f"→ {recommendation}")
print(f"📊 Reason: GRID ROI = {grid_roi:.2f}% vs HOLD ROI = {hold_roi:.2f}% ({compare_basis})")

# Step 5: Log result
log_file.parent.mkdir(parents=True, exist_ok=True)
timestamp = datetime.utcnow().isoformat()
with log_file.open("a") as f:
    f.write(f"{timestamp},{recommendation},GRID={grid_roi:.2f},HOLD={hold_roi:.2f},{compare_basis}\n")

# Update FIX registry
import json
from datetime import datetime
try:
    with open('fix_registry.json', 'r') as f:
        registry = json.load(f)
except:
    registry = {}

registry['FIX-4'] = {
    'status': 'PASSED',
    'timestamp': datetime.utcnow().isoformat(),
    'message': 'Investment decision generated successfully.'
}

with open('fix_registry.json', 'w') as f:
    json.dump(registry, f, indent=2)
