# rotate_lima_logs.py

import shutil
from datetime import datetime
from pathlib import Path

log_dir = Path("/home/ec2-user/project_lima/logs")
log_file = log_dir / "daily_pipeline.log"
archive_name = f"daily_pipeline_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.log"
archive_path = log_dir / "archive" / archive_name

# Ensure archive directory exists
archive_path.parent.mkdir(parents=True, exist_ok=True)

if log_file.exists():
    shutil.copy(log_file, archive_path)
    log_file.unlink()
    print(f"[✅] Rotated and archived: {archive_path}")
else:
    print("[⚠️] No daily_pipeline.log found to rotate.")
