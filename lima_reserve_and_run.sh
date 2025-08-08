#!/bin/bash
# Reserve an AWS-allowed, locally-free port and launch a command on that port. (LOCKED)

set -euo pipefail
PORT="${1:-}"
shift || true
if [[ -z "$PORT" || ! "$PORT" =~ ^[0-9]+$ ]]; then
  echo "[USAGE] $0 <port> -- <command> [args...]"
  exit 2
fi
if [[ "${1:-}" != "--" ]]; then
  echo "[USAGE] $0 <port> -- <command> [args...]"
  exit 2
fi
shift

. "$HOME/project_lima/ports_lib.sh"

# 1) Enforce AWS-only source exists
require_master_file

# 2) Verify AWS allows it
if ! is_port_allowed "$PORT"; then
  echo "[DENY] Port $PORT is NOT in AWS-allowed list."
  exit 3
fi

# 3) Verify locally free
if ! is_port_free_local "$PORT"; then
  echo "[BUSY] Port $PORT is already in use locally."
  exit 4
fi

# 4) Acquire an exclusive lock to prevent races
LOCKROOT="/var/lock"
[[ -w "$LOCKROOT" ]] || LOCKROOT="$HOME/.lima_locks"
mkdir -p "$LOCKROOT"
LOCKFILE="$LOCKROOT/port_${PORT}.lock"
exec 9>"$LOCKFILE"
if ! command -v flock >/dev/null 2>&1; then
  echo "[FATAL] 'flock' not available; cannot guarantee exclusive launch."
  exit 7
fi
if ! flock -n 9; then
  echo "[LOCKED] Another process holds the reservation for port $PORT."
  exit 5
fi

echo "[OK] Port $PORT reserved. Launching command..."

# 5) Final sanity check just before exec
if ! is_port_free_local "$PORT"; then
  echo "[RACE] Port $PORT became busy just before launch."
  exit 6
fi

# 6) Substitute __PORT__ tokens in the command with the reserved port
ARGS=("$@")
for i in "${!ARGS[@]}"; do
  if [[ "${ARGS[$i]}" == "__PORT__" ]]; then
    ARGS[$i]="$PORT"
  fi
done

# Also export env var for commands that read from environment
export LIMA_PORT="$PORT"

# 7) Exec the service; lock is held until this process exits
exec "${ARGS[@]}"
