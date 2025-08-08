#!/bin/bash
# Run app only if chosen port is valid; log PASS/FAIL; rotate+compress logs; substitute __PORT__.

set -euo pipefail
LOGFILE="$HOME/project_lima/lima_port_validation.log"
MAXSIZE=1048576   # 1 MB
PORT="${1:-}"
shift || true

if [[ -z "$PORT" || ! "$PORT" =~ ^[0-9]+$ ]]; then
  echo "[USAGE] $0 <port> -- <application_command> [args...]"
  exit 2
fi
if [[ "${1:-}" != "--" ]]; then
  echo "[USAGE] $0 <port> -- <application_command> [args...]"
  exit 2
fi
shift

# Rotate + compress log if too big
if [ -f "$LOGFILE" ] && [ "$(stat -c%s "$LOGFILE")" -ge "$MAXSIZE" ]; then
  BACKUP="$LOGFILE.$(date -u +'%Y%m%dT%H%M%SZ').bak"
  mv "$LOGFILE" "$BACKUP"
  gzip "$BACKUP"
  touch "$LOGFILE"
fi

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Validate port via pre-flight
if ! "$HOME/project_lima/lima_require_port.sh" "$PORT"; then
  echo "$TIMESTAMP | FAIL | Port: $PORT | Command: $*" >> "$LOGFILE"
  echo "[FAIL] Port $PORT validation failed."
  exit 1
fi

echo "$TIMESTAMP | PASS | Port: $PORT | Command: $*" >> "$LOGFILE"
echo "[PASS] Port $PORT validated. Launching…"

# Substitute __PORT__ tokens and export LIMA_PORT
ARGS=("$@")
for i in "${!ARGS[@]}"; do
  if [[ "${ARGS[$i]}" == "__PORT__" ]]; then
    ARGS[$i]="$PORT"
  fi
done
export LIMA_PORT="$PORT"

exec "${ARGS[@]}"
