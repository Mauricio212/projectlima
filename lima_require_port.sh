#!/bin/bash
# Project Lima — Require that a specific port is AWS-allowed & locally free

set -euo pipefail
PORT="${1:-}"

if [[ -z "$PORT" || ! "$PORT" =~ ^[0-9]+$ ]]; then
  echo "[USAGE] $0 <port>"
  exit 2
fi

. "$HOME/project_lima/ports_lib.sh"

# Ensure AWS master file exists (single source of truth)
require_master_file

# Check if AWS allows the port
if ! is_port_allowed "$PORT"; then
  echo "[DENY] Port $PORT is NOT in AWS-allowed list (Security Groups)."
  exit 3
fi

# Check if port is free locally
if ! is_port_free_local "$PORT"; then
  echo "[BUSY] Port $PORT is allowed by AWS but NOT free locally."
  exit 4
fi

echo "[OK] Port $PORT passed pre-flight (AWS-allowed & locally free)."
