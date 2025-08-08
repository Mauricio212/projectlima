#!/bin/bash
# Project Lima — Pick the first AWS-allowed & locally-free port (LOCKED)

set -euo pipefail
. "$HOME/project_lima/ports_lib.sh"

# Ensure master exists
require_master_file

# Choose
CHOSEN="$(choose_allowed_free_port || true)"

if [[ -z "${CHOSEN:-}" ]]; then
  echo "[ERROR] No AWS-allowed port is currently free locally."
  exit 5
fi

echo "$CHOSEN"
