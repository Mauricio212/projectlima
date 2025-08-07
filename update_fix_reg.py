# update_fix_reg.py

import json
import argparse
from datetime import datetime
from pathlib import Path

# Paths to FIX registry and log file
FIX_REG_PATH = Path("/home/ec2-user/project_lima/system_state/fix_reg.json")
LOG_PATH = Path("/home/ec2-user/project_lima/logs/fix_reg_update_log.csv")

def update_fix_status(fix_id, status):
    # Load existing FIX_REG or create new
    if FIX_REG_PATH.exists():
        with FIX_REG_PATH.open("r") as f:
            fix_reg = json.load(f)
    else:
        fix_reg = {}

    # Update the FIX module's status and timestamp
    timestamp = datetime.utcnow().isoformat()
    fix_reg[fix_id] = {
        "status": status.upper(),
        "timestamp": timestamp
    }

    # Save updated FIX_REG back to file
    FIX_REG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with FIX_REG_PATH.open("w") as f:
        json.dump(fix_reg, f, indent=2)

    # Append update to CSV log file
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    log_line = f"{timestamp},{fix_id},{status.upper()}\n"
    with LOG_PATH.open("a") as log_file:
        log_file.write(log_line)

    # Confirmation message
    print(f"✅ {fix_id} updated to {status.upper()} at {timestamp}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update FIX_REG status")
    parser.add_argument("fix_id", help="Fix module ID, e.g. FIX-1")
    parser.add_argument("status", help="Status: PASSED, FAILED, PENDING")
    args = parser.parse_args()

    update_fix_status(args.fix_id, args.status)
