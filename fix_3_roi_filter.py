import pandas as pd
from datetime import datetime
import os
import json

# File paths
input_file = "grid_hold_output/step_3_2_token_roi.csv"
output_file = "grid_hold_output/step_3_3_selected_tokens.csv"
log_file = "logs/grid_vs_hold_filter_log.csv"
fix_reg_path = "fix_registry.json"

# Load ROI data
df = pd.read_csv(input_file)

# Filter: GRID ROI must be greater than HOLD ROI
filtered_df = df[df["grid_roi"] > df["hold_roi"]]

# Preserve step_pct in output
filtered_df.to_csv(output_file, index=False)

# Logging
timestamp = datetime.utcnow().isoformat()
log_data = {
    "timestamp": timestamp,
    "input_count": len(df),
    "filtered_count": len(filtered_df),
    "output_file": output_file,
    "log_file": log_file,
}

log_df = pd.DataFrame([log_data])
if os.path.exists(log_file):
    log_df.to_csv(log_file, mode="a", header=False, index=False)
else:
    log_df.to_csv(log_file, index=False)

# Update FIX registry
registry = {}
if os.path.exists(fix_reg_path):
    with open(fix_reg_path, "r") as f:
        registry = json.load(f)

registry["FIX-3"] = {
    "status": "PASSED",
    "timestamp": timestamp,
    "message": f"{len(filtered_df)} tokens passed ROI superiority check.",
}

with open(fix_reg_path, "w") as f:
    json.dump(registry, f, indent=2)

print(f"[✅ FIX-3] Filtered {len(df)} tokens → {len(filtered_df)} passed ROI superiority check.")
print(f"[📄 OUTPUT] {output_file}")
print(f"[📝 LOGGED] {log_file}")
