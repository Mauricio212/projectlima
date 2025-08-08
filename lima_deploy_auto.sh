#!/bin/bash
# Project Lima — Auto-pick AWS-allowed & locally-free port, validate, log, and launch application

set -euo pipefail

if [[ "$1" != "--" ]]; then
  echo "[USAGE] $0 -- <command> [args...]"
  exit 2
fi
shift

# 1) Refresh AWS master file
"$HOME/project_lima/lima_update_aws_ports_master.sh" >/dev/null

# 2) Pick first AWS-allowed & locally-free port
PORT="$("$HOME/project_lima/lima_pick_open_port.sh")"
if [[ -z "${PORT:-}" ]]; then
  echo "[ERROR] No AWS-allowed port is currently free locally."
  exit 5
fi
echo "[LIMA] Selected port: $PORT"

# 3) Run validation and capture result
if "$HOME/project_lima/lima_require_port.sh" "$PORT"; then
  echo "[PASS] Port $PORT validated successfully."
else
  echo "[FAIL] Port $PORT did not pass validation."
  "$HOME/project_lima/lima_run_with_port_check.sh" "$PORT" -- true >/dev/null 2>&1 || true
  exit 1
fi

# 4) Launch application through logging wrapper
"$HOME/project_lima/lima_run_with_port_check.sh" "$PORT" -- "$@"
