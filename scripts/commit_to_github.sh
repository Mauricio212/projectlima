#!/bin/bash
# commit_to_github.sh - Phase 2 Git Version Control with Lima Enforcement

CONFIG_ENFORCER="$HOME/project_lima/scripts/enforce_config_integrity.sh"
REPO_PATH="$HOME/project_lima"
LOG="$HOME/project_lima/logs/deployment_results.log"
NOW=$(date "+%Y-%m-%d %H:%M:%S")

# Enforce Lima policies before proceeding
bash "$CONFIG_ENFORCER" || exit 1

# Go to repo
cd "$REPO_PATH" || {
  echo "$NOW ❌ GIT COMMIT FAILED: Repo path not found" | tee -a "$LOG"
  exit 1
}

# Add changes
git add .

# Commit with timestamp
git commit -m "Project Lima auto-commit: $NOW"

# Push
git push origin main

# Log success
if [ $? -eq 0 ]; then
    echo "$NOW ✅ GIT COMMIT SUCCESS: Changes pushed to origin/main" | tee -a "$LOG"
else
    echo "$NOW ❌ GIT COMMIT FAILED: Push error" | tee -a "$LOG"
    exit 1
fi
