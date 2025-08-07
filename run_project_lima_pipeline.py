# run_project_lima_pipeline.py

import subprocess
import pandas as pd
from pathlib import Path
from datetime import datetime

# Paths
roi_path = Path("/home/ec2-user/project_lima/grid_hold_output/step_3_2_token_roi.csv")
log_path = Path("/home/ec2-user/project_lima/logs/run_pipeline_log.csv")
diagnostic_path = Path("/home/ec2-user/project_lima/fix_grid_failure_debugger.py")

def run_step(label, command):
    print(f"\n🔧 Running: {label}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f"❌ {label} FAILED\n{result.stderr}")
        exit(1)

def check_and_diagnose():
    try:
        df = pd.read_csv(roi_path)
        grid_roi = df[df["symbol"].str.upper() != "HOLD"]["grid_roi"].mean()
        hold_roi = df[df["symbol"].str.upper() == "HOLD"]["hold_roi"].mean()
        if hold_roi >= grid_roi:
            print("⚠️ HOLD ROI is greater than or equal to GRID ROI. Triggering diagnostic...")
            subprocess.run(f"python3 {diagnostic_path}", shell=True)
        else:
            print(f"✅ GRID ROI ({grid_roi:.2f}%) > HOLD ROI ({hold_roi:.2f}%) — No diagnostic needed.")
    except Exception as e:
        print(f"❌ Error during ROI comparison or diagnostic trigger: {e}")
        exit(1)

def main():
    timestamp = datetime.utcnow().isoformat()

    run_step("Data Refresh", "python3 ~/project_lima/Step3_1.py")
    # Step-by-step execution
    run_step("FIX-1: Token Selector", "python3 ~/project_lima/fix_1_token_selector.py")
    run_step("Build GRID Config", "python3 ~/project_lima/build_grid_config.py")
    run_step("FIX-2: ROI Table Generator", "python3 ~/project_lima/fix_2_token_roi_generator.py")
    run_step("FIX-3: ROI Superiority Filter", "python3 ~/project_lima/fix_3_roi_filter.py")
    run_step("FIX-4: Decision Generator", "python3 ~/project_lima/fix_4_decision_generator.py")

    # Auto-trigger diagnostic if needed
    check_and_diagnose()

    # Log full pipeline run
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a") as f:
        f.write(f"{timestamp},FULL_PIPELINE_COMPLETED\n")

    print("\n✅ Project Lima Full Pipeline: COMPLETE")

if __name__ == "__main__":
    main()
