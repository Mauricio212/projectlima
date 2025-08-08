#!/bin/bash
# Project Lima — Validate a specific port against AWS master + local availability (LOCKED)

set -euo pipefail
PORT="${1:-}"

if [[ -z "$PORT" || ! "$PORT" =~ ^[0-9]+$ ]]; then
  echo "[USAGE] $0 <port>"
  exit 2
fi

. "$HOME/project_lima/ports_lib.sh"

# 1) Ensure master exists (AWS-only source)
require_master_file

# 2) Check if port is in AWS-allowed list
if ! is_port_allowed "$PORT"; then
  echo "[DENY] Port $PORT is NOT in AWS-allowed list (Security Groups)."
  exit 3
fi

# 3) Check if port is free locally
if ! is_port_free_local "$PORT"; then
  echo "[BUSY] Port $PORT is allowed by AWS but NOT free locally."
  exit 4
fi

echo "[OK] Port $PORT is allowed by AWS AND free locally."
