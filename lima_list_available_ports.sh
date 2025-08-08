#!/bin/bash
# Project Lima — Show AWS-open ports and which are FREE locally right now (LOCKED)

set -euo pipefail
. "$HOME/project_lima/ports_lib.sh"

# Ensure master exists (AWS-only source)
require_master_file

echo "[LIMA] AWS-open TCP ports (from aws_ports_master.json):"
read_allowed_tcp_ports | tr '\n' ' '
echo
echo "-------------------------------------------"

echo "[LIMA] Ports AVAILABLE NOW (AWS-allowed AND locally free):"
AVAILABLE=0
while IFS= read -r p; do
  if is_port_free_local "$p"; then
    printf "%s " "$p"
    AVAILABLE=1
  fi
done < <(read_allowed_tcp_ports)

if [ "$AVAILABLE" -eq 0 ]; then
  echo "(none)"
else
  echo
fi
