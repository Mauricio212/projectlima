import os
import json
import socket
import platform
from datetime import datetime

ec2_env_info = {
    "timestamp": datetime.utcnow().isoformat() + "Z",
    "hostname": socket.gethostname(),
    "local_ip": socket.gethostbyname(socket.gethostname()),
    "os_name": platform.system(),
    "os_version": platform.version(),
    "platform": platform.platform(),
    "architecture": platform.machine(),
    "python_version": platform.python_version()
}

output_path = "/home/ec2-user/project_lima/logs/ec2_env_snapshot_stage1.json"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, "w") as f:
    json.dump(ec2_env_info, f, indent=2)

print(f"✅ Stage 1 snapshot saved to: {output_path}")
