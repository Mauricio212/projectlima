#!/bin/bash
# Project Lima - Ports Library (LOCKED to aws_ports_master.json)

MASTER_FILE="$HOME/project_lima/aws_ports_master.json"

require_master_file() {
  if [ ! -f "$MASTER_FILE" ] || [ ! -s "$MASTER_FILE" ]; then
    echo "[FATAL] Master file missing or empty: $MASTER_FILE"
    echo "[FATAL] No other source is allowed. Exiting."
    exit 1
  fi
}

# Robust: extract only numbers from the "tcp" array regardless of commas/spaces/format
read_allowed_tcp_ports() {
  require_master_file
  # Read only the tcp array block, then print each integer on its own line
  sed -n '/"tcp"[[:space:]]*:/,/\]/{p}' "$MASTER_FILE" | grep -o '[0-9]\+' | sort -n | uniq
}

is_port_allowed() {
  local port="$1"
  read_allowed_tcp_ports | awk -v p="$port" '$0==p {found=1} END{exit found?0:1}'
}

# Check if a TCP port is free locally (no process listening)
is_port_free_local() {
  local port="$1"
  if command -v ss >/dev/null 2>&1; then
    ss -lnt | awk 'NR>1 {print $4}' | awk -F: '{print $NF}' | awk 'NF' | awk -v p="$port" '$0==p{f=1} END{exit f?1:0}'
    return $?
  fi
  if command -v lsof >/dev/null 2>&1; then
    lsof -iTCP -sTCP:LISTEN -P -n 2>/dev/null | awk '{print $9}' | awk -F: '{print $NF}' | awk -v p="$port" '$0==p{f=1} END{exit f?1:0}'
    return $?
  fi
  echo "[FATAL] Neither 'ss' nor 'lsof' is available to test local ports."
  exit 2
}

choose_allowed_free_port() {
  local p
  while IFS= read -r p; do
    if is_port_free_local "$p"; then
      echo "$p"
      return 0
    fi
  done < <(read_allowed_tcp_ports)
  return 1
}

