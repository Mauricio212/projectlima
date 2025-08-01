# system_snapshot_and_certify.py

import subprocess
from datetime import datetime
from pathlib import Path

log_dir = Path("/home/ec2-user/project_lima/logs")
scripts = [
    "archive_lima_snapshot.py",
    "golden_rule_cert_report.py"
]

timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
print(f"\n🧩 Starting Project Lima System Snapshot & Certification — {timestamp}")

for script in scripts:
    path = Path(f"/home/ec2-user/project_lima/scripts/{script}")
    if path.exists():
        print(f"▶️ Running {script}...")
        subprocess.run(["python3", str(path)])
    else:
        print(f"⚠️ Script not found: {script}")

print("✅ System snapshot + certification complete.")
