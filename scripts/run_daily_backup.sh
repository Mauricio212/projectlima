#!/bin/bash
# run_daily_backup.sh - Project Lima Phase 1 Backup Script

CONFIG_ENFORCER="$HOME/project_lima/scripts/enforce_config_integrity.sh"
SOURCE_PATH="$HOME/project_lima"
DEST_PATH="gdrive:/Project_Lima_Backup"
LOG="$HOME/project_lima/logs/deployment_results.log"
HISTORY="$HOME/project_lima/logs/backup_history.txt"
NOW=$(date "+%Y-%m-%d %H:%M:%S")

# Enforce config integrity
bash "$CONFIG_ENFORCER" || exit 1

# Begin backup
echo "$NOW ⏳ Starting Project Lima backup to Google Drive..." | tee -a "$LOG"

rclone sync "$SOURCE_PATH" "$DEST_PATH" \
  --create-empty-src-dirs \
  --copy-links \
  --fast-list \
  --transfers=8 \
  --checkers=8 \
  --tpslimit=10 \
  --log-level INFO \
  --log-file="$HOME/project_lima/logs/last_backup_rclone.log"

if [ $? -eq 0 ]; then
    echo "$NOW ✅ BACKUP SUCCESS: Synced $SOURCE_PATH → $DEST_PATH" | tee -a "$LOG"
    echo "$NOW ✅ $SOURCE_PATH → $DEST_PATH" >> "$HISTORY"
else
    echo "$NOW ❌ BACKUP FAILED: Error syncing $SOURCE_PATH → $DEST_PATH" | tee -a "$LOG"
    echo "$NOW ❌ $SOURCE_PATH → $DEST_PATH" >> "$HISTORY"
    exit 1
fi
