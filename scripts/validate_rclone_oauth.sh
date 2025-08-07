#!/bin/bash
# validate_rclone_oauth.sh - Phase 0.1
# ✅ Verifies rclone OAuth connection with Google Drive

echo "[Phase 0.1] Verifying rclone OAuth with Google Drive..."

rclone lsd gdrive: > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "[Phase 0.1] ✅ rclone OAuth SUCCESS: Connected to Google Drive."
    echo "$(date) [Phase 0.1] ✅ rclone OAuth verified" >> ~/project_lima/logs/deployment_results.log
else
    echo "[Phase 0.1] ❌ rclone OAuth FAILED: Check authentication."
    echo "$(date) [Phase 0.1] ❌ rclone OAuth FAILED" >> ~/project_lima/logs/deployment_results.log
    exit 1
fi
