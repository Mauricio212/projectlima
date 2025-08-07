#!/bin/bash
# verify_backup.sh - Phase 1.5 Backup Verification Script

CONFIG_ENFORCER="$HOME/project_lima/scripts/enforce_config_integrity.sh"
DEST_PATH="gdrive:/Project_Lima_Backup"
LOG="$HOME/project_lima/logs/deployment_results.log"
NOW=$(date "+%Y-%m-%d %H:%M:%S")

# Enforce config integrity
bash "$CONFIG_ENFORCER" || exit 1

echo "$NOW 🔍 Verifying Lima backup contents in $DEST_PATH..." | tee -a "$LOG"

file_count=$(rclone lsf "$DEST_PATH" --files-only | wc -l)

if [ "$file_count" -gt 0 ]; then
    echo "$NOW ✅ BACKUP VERIFIED: $file_count file(s) found in $DEST_PATH" | tee -a "$LOG"
    exit 0
else
    echo "$NOW ❌ BACKUP VERIFICATION FAILED: No files found in $DEST_PATH" | tee -a "$LOG"
    exit 1
fi
bash ~/project_lima/scripts/enforce_config_integrity.sh || exit 1
