# reset_pipeline_state.py

from pathlib import Path
import shutil

base = Path("/home/ec2-user/project_lima")
folders = ["grid_hold_output", "logs", "system"]

# Confirm reset directory exists
for folder in folders:
    target = base / folder
    if target.exists():
        for item in target.iterdir():
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
        print(f"[🧹] Cleared: {target}")
    else:
        print(f"[⚠️] Skipped (missing): {target}")

print("✅ Project Lima pipeline state has been reset.")
