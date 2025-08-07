#!/usr/bin/env python3
import os
from datetime import datetime

root = "/home/ec2-user/project_lima"
report_file = f"{root}/logs/lima_file_index_report.txt"
terms = {
    "credentials": ["api", "key", "secret", "cred"],
    "config": ["config", "json", "env"],
    "runtime": ["fix", "reg", "state"],
    "logs": ["log", "csv"],
    "scripts": [".py"]
}

index = {k: [] for k in terms}

for dirpath, _, filenames in os.walk(root):
    for fname in filenames:
        fpath = os.path.join(dirpath, fname)
        for category, keywords in terms.items():
            if any(kw in fname.lower() for kw in keywords):
                index[category].append(fpath)
                break

with open(report_file, "w") as out:
    out.write(f"🧠 Project Lima File Index Report — {datetime.utcnow().isoformat()}Z\n\n")
    for category, files in index.items():
        out.write(f"📂 {category.upper()} FILES:\n")
        for path in sorted(files):
            out.write(f"  - {path}\n")
        out.write("\n")

print(f"✅ Index complete. Report saved to: {report_file}")
