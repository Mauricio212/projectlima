#!/bin/bash
# Project Lima — Show AWS-allowed ports, which are in use, and which are free right now

set -euo pipefail
. "$HOME/project_lima/ports_lib.sh"

# Ensure AWS master file is fresh
"$HOME/project_lima/lima_update_aws_ports_master.sh" >/dev/null

require_master_file

echo "=== AWS-ALLOWED PORTS ==="
ALL_PORTS=($(read_allowed_tcp_ports))
echo "${ALL_PORTS[@]}"
echo

echo "=== PORTS IN USE ==="
IN_USE=()
FREE=()
for p in "${ALL_PORTS[@]}"; do
  if is_port_free_local "$p"; then
    FREE+=("$p")
  else
    IN_USE+=("$p")
  fi
done

if [ ${#IN_USE[@]} -eq 0 ]; then
  echo "(none)"
else
  echo "${IN_USE[@]}"
fi
echo

echo "=== PORTS FREE NOW ==="
if [ ${#FREE[@]} -eq 0 ]; then
  echo "(none)"
else
  echo "${FREE[@]}"
fi
