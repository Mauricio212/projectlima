# cron_heartbeat_logger.py

from datetime import datetime
from pathlib import Path

log_dir = Path("/home/ec2-user/project_lima/logs")
log_dir.mkdir(parents=True, exist_ok=True)
heartbeat_log = log_dir / "cron_heartbeat.log"

timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
entry = f"[✅] Cron heartbeat ping — {timestamp}\n"

with heartbeat_log.open("a") as f:
    f.write(entry)

print(entry.strip())
