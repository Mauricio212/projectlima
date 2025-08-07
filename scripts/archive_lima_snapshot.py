# archive_lima_snapshot.py

import shutil
from pathlib import Path
from datetime import datetime

base = Path("/home/ec2-user/project_lima")
snapshot_dir = base / "snapshots"
snapshot_dir.mkdir(parents=True, exist_ok=True)

timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
archive_name = snapshot_dir / f"lima_snapshot_{timestamp}.zip"

# What to include
to_archive = [
    base / "grid_hold_output",
    base / "logs",
    base / "system"
]

shutil.make_archive(str(archive_name).replace(".zip", ""), 'zip', base_dir=base, logger=None)

print(f"[📦] Snapshot archived: {archive_name}")
