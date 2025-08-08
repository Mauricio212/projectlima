#!/bin/bash
# Project Lima - Read-Only AWS Ports Master File (Enforced Single Source)

MASTER_FILE="$HOME/project_lima/aws_ports_master.json"

if [ ! -f "$MASTER_FILE" ]; then
    echo "[FATAL] AWS Ports Master File not found. No other source is allowed."
    exit 1
fi

echo "[LIMA] Reading from AWS Ports Master File only..."
cat "$MASTER_FILE"
