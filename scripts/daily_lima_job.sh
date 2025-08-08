#!/bin/bash
# daily_lima_job.sh - Runs daily backup and Git commit under full enforcement

NOW=$(date "+%Y-%m-%d %H:%M:%S")
LOG="$HOME/project_lima/logs/deployment_results.log"

echo "$NOW ▶️ DAILY JOB STARTED" >> "$LOG"

/bin/bash "$HOME/project_lima/scripts/run_daily_backup.sh"
/bin/bash "$HOME/project_lima/scripts/commit_to_github.sh"

NOW_END=$(date "+%Y-%m-%d %H:%M:%S")
echo "$NOW_END ✅ DAILY JOB COMPLETE" >> "$LOG"
