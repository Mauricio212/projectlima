# selfaware_structure_check.py

from pathlib import Path
from datetime import datetime

required_paths = [
    "/home/ec2-user/project_lima",
    "/home/ec2-user/project_lima/grid_hold_output",
    "/home/ec2-user/project_lima/logs",
    "/home/ec2-user/project_lima/scripts",
    "/home/ec2-user/project_lima/run_project_lima_pipeline.py",
    "/home/ec2-user/project_lima/grid_hold_output/step_3_1_tokens_*.csv",
    "/home/ec2-user/project_lima/grid_hold_output/step_3_2_token_roi.csv",
    "/home/ec2-user/project_lima/grid_hold_output/step_3_3_selected_tokens.csv",
    "/home/ec2-user/project_lima/logs/fix_4_decision_log.csv"
]

log_file = Path("/home/ec2-user/project_lima/system/selfaware.log")
log_file.parent.mkdir(parents=True, exist_ok=True)
timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

log_lines = [f"🔎 SELF-AWARE STRUCTURE CHECK — {timestamp}"]

for path in required_paths:
    if "*" in path:
        matches = list(Path().glob(path.replace("/home/ec2-user/", "")))
        exists = len(matches) > 0
    else:
        exists = Path(path).exists()
    status = "✅" if exists else "❌"
    log_lines.append(f"{status} {path}")

# Save log
with log_file.open("a") as f:
    for line in log_lines:
        f.write(line + "\n")

print("\n".join(log_lines))
