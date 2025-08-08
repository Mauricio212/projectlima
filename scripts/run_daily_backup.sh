#!/bin/bash
# run_daily_backup.sh - Final Lima Backup Script (Full Sync, Enforced, With Confirmation)

CONFIG_ENFORCER="$HOME/project_lima/scripts/enforce_config_integrity.sh"
SOURCE_PATH="$HOME/project_lima"
DEST_PATH="gdrive:/Project_Lima_Backup"
LOG="$HOME/project_lima/logs/deployment_results.log"
HISTORY="$HOME/project_lima/logs/backup_history.txt"
NOW=$(date "+%Y-%m-%d %H:%M:%S")
SECONDS=0

# Enforce Lima policy
bash "$CONFIG_ENFORCER" || exit 1

# Start log
echo "$NOW ⏳ Starting FULL Project Lima backup to Google Drive..." | tee -a "$LOG"

rclone sync "$SOURCE_PATH" "$DEST_PATH" \
  --create-empty-src-dirs \
  --copy-links \
  --fast-list \
  --transfers=8 \
  --checkers=8 \
  --tpslimit=10 \
  --progress \
  --log-level INFO \
  --log-file="$HOME/project_lima/logs/last_backup_rclone.log"

# Handle outcome
if [ $? -eq 0 ]; then
    echo "$NOW ✅ BACKUP SUCCESS (Full Sync): $SOURCE_PATH → $DEST_PATH" | tee -a "$LOG"
    echo "$NOW ✅ $SOURCE_PATH → $DEST_PATH (Full Sync)" >> "$HISTORY"
    END=$(date "+%Y-%m-%d %H:%M:%S")
    echo "$END ✅ DONE: Project Lima backup completed. Duration: $((SECONDS))s" | tee -a "$LOG"
else
    echo "$NOW ❌ BACKUP FAILED (Full Sync): Error syncing to $DEST_PATH" | tee -a "$LOG"
    echo "$NOW ❌ $SOURCE_PATH → $DEST_PATH (Full Sync)" >> "$HISTORY"
    END=$(date "+%Y-%m-%d %H:%M:%S")
    echo "$END ❌ DONE: Backup attempt failed. Duration: $((SECONDS))s" | tee -a "$LOG"
    exit 1
fi
