#!/usr/bin/env python3
import os
import json
from datetime import datetime

# ✅ Define required files
REQUIRED_FILES = [
    "project_lima_config.json",
    "fix_1_token_validator.py",
    "fix_2_roi_calculator.py",
    "fix_3_roi_filter.py",
    "fix_4_decision_generator.py",
    "fix_5_live_price_validator.py",
    "run_project_lima_pipeline.py",
    "grid_hold_output/grid_config.csv",
    "grid_hold_output/step_3_1_tokens.csv",
    "grid_hold_output/step_3_2_token_roi.csv",
    "logs/lima_file_index_report.txt"
]

# ✅ Paths
BASE_DIR = "/home/ec2-user/project_lima"
REPORT_PATH = os.path.join(BASE_DIR, "logs/fix_gr_008_watchdog_report.json")
os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)

# ✅ Check for files
missing = []
existing = []

for f in REQUIRED_FILES:
    full_path = os.path.join(BASE_DIR, f)
    if os.path.isfile(full_path):
        existing.append(f)
    else:
        missing.append(f)

# ✅ Generate report
report = {
    "timestamp": datetime.utcnow().isoformat(),
    "total_required": len(REQUIRED_FILES),
    "found": len(existing),
    "missing": len(missing),
    "missing_files": missing,
    "existing_files": existing,
    "status": "✅ OK" if not missing else "❌ MISSING FILES"
}

with open(REPORT_PATH, "w") as f:
    json.dump(report, f, indent=2)

# ✅ Output result
print("✅ FIX-GR-008 Watchdog Complete")
print(f"📝 Report saved to: {REPORT_PATH}")
print(f"📦 Found {len(existing)} / {len(REQUIRED_FILES)} required files")
if missing:
    print("❌ Missing files:")
    for m in missing:
        print(f"   - {m}")
else:
    print("🎉 All required files are present.")
