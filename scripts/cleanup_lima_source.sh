#!/bin/bash
# cleanup_lima_source.sh - Deletes known bloat from ~/project_lima safely

ROOT="$HOME/project_lima"
LOG="$ROOT/logs/deployment_results.log"
NOW=$(date "+%Y-%m-%d %H:%M:%S")

echo "$NOW 🧹 STARTING CLEANUP: Removing known junk from source" | tee -a "$LOG"

# Delete list (safe for Lima systems)
declare -a DELETE_PATHS=(
  "$ROOT/venv"
  "$ROOT/lima_env"
  "$ROOT/__pycache__"
  "$ROOT/certified"
  "$ROOT/tmp"
  "$ROOT/nohup.out"
  "$ROOT/*.bak"
  "$ROOT/**/*.bak"
  "$ROOT/**/*.pyc"
  "$ROOT/**/__pycache__"
  "$ROOT/logs_backup"
)

for path in "${DELETE_PATHS[@]}"; do
  echo "$NOW 🔥 Removing $path" | tee -a "$LOG"
  rm -rf $path
done

echo "$NOW ✅ CLEANUP COMPLETE: Unneeded files removed from ~/project_lima" | tee -a "$LOG"
