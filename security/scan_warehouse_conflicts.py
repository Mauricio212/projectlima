#!/usr/bin/env python3

import os
import fnmatch
from pathlib import Path

WAREHOUSE_ROOT = Path("~/project_lima/doc_warehouse/").expanduser()
FIX_ROOT = Path("~/project_lima/").expanduser()
LOG_ROOT = Path("~/project_lima/logs/").expanduser()
CONFLICTS = []

def scan_paths(base, target):
    for root, _, files in os.walk(base):
        for f in files:
            if fnmatch.fnmatch(f, "*.csv") or fnmatch.fnmatch(f, "*.log"):
                full_path = Path(root) / f
                if f in target:
                    CONFLICTS.append((str(full_path), target[f]))

def index_fix_files():
    known = {}
    for root, _, files in os.walk(FIX_ROOT):
        for f in files:
            if fnmatch.fnmatch(f, "*.csv") or fnmatch.fnmatch(f, "*.log"):
                path = Path(root) / f
                known[f] = str(path)
    return known

def check_crontab():
    print("🔍 Checking crontab for potential job overlap...")
    os.system("crontab -l")

def main():
    print("🔎 Scanning for warehouse and FIX file collisions...")
    fix_index = index_fix_files()
    scan_paths(WAREHOUSE_ROOT, fix_index)
    scan_paths(LOG_ROOT, fix_index)

    if CONFLICTS:
        print("\n🚨 FILE CONFLICTS FOUND:")
        for warehouse_file, fix_file in CONFLICTS:
            print(f"⚠️ {warehouse_file} conflicts with FIX file: {fix_file}")
    else:
        print("\n✅ No file collisions found between warehouse and FIX modules.")

    check_crontab()
    print("\n🧪 Interference scan complete.")

if __name__ == "__main__":
    main()
