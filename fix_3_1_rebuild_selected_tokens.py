import csv

INPUT_ROI_FILE = "grid_hold_output/step_3_2_token_roi.csv"
GRID_CONFIG_FILE = "grid_hold_output/grid_config.csv"
OUTPUT_FILE = "grid_hold_output/step_3_3_selected_tokens.csv"

# Load step_pct from grid_config.csv
step_pct_map = {}
with open(GRID_CONFIG_FILE, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        step_pct_map[row["symbol"]] = row["step_pct"]

# Rebuild output with step_pct
with open(INPUT_ROI_FILE, "r") as infile, open(OUTPUT_FILE, "w", newline="") as outfile:
    reader = csv.DictReader(infile)
    fieldnames = ["symbol", "grid_roi", "hold_roi", "step_pct"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in reader:
        symbol = row["symbol"]
        if float(row["grid_roi"]) > float(row["hold_roi"]) and symbol in step_pct_map:
            row["step_pct"] = step_pct_map[symbol]
            writer.writerow(row)

print(f"✅ Rebuilt: {OUTPUT_FILE} with step_pct included.")
