#!/bin/bash
# enforce_config_integrity.sh - Project Lima Policy Firewall

CONFIG_PATH="$HOME/project_lima/config/project_lima_config.json"
LOG_FILE="$HOME/project_lima/logs/deployment_results.log"
NOW=$(date +"%Y-%m-%d %H:%M:%S")

# Fail if config file is missing
if [ ! -f "$CONFIG_PATH" ]; then
    echo "$NOW ❌ CONFIG ENFORCEMENT FAILED: Missing $CONFIG_PATH" | tee -a "$LOG_FILE"
    exit 1
fi

# Load and enforce Google Drive protection policy
read_drive_path=$(jq -r '.drive_protection_policy.destination_path' "$CONFIG_PATH")
read_prohibited=$(jq -r '.drive_protection_policy.read_access_outside_path' "$CONFIG_PATH")
write_prohibited=$(jq -r '.drive_protection_policy.write_access_outside_path' "$CONFIG_PATH")
delete_blocked=$(jq -r '.drive_protection_policy.delete_operations_allowed' "$CONFIG_PATH")

if [[ "$read_drive_path" != "gdrive:/Project_Lima_Backup/" ]]; then
    echo "$NOW ❌ ENFORCEMENT BLOCKED: Invalid Google Drive destination path ($read_drive_path)" | tee -a "$LOG_FILE"
    exit 1
fi

if [[ "$read_prohibited" != "false" || "$write_prohibited" != "false" || "$delete_blocked" != "false" ]]; then
    echo "$NOW ❌ ENFORCEMENT BLOCKED: Drive access restrictions not enforced" | tee -a "$LOG_FILE"
    exit 1
fi

# Enforce physical validation policy
require_live=$(jq -r '.physical_validation_policy.live_data_required' "$CONFIG_PATH")
block_logic=$(jq -r '.physical_validation_policy.simulate_logic_allowed' "$CONFIG_PATH")
block_mock=$(jq -r '.physical_validation_policy.mock_output_allowed' "$CONFIG_PATH")

if [[ "$require_live" != "true" || "$block_logic" != "false" || "$block_mock" != "false" ]]; then
    echo "$NOW ❌ ENFORCEMENT BLOCKED: Physical validation policy not respected (live=$require_live, logic=$block_logic, mock=$block_mock)" | tee -a "$LOG_FILE"
    exit 1
fi

# Enforce live financial data policy
live_required=$(jq -r '.live_financial_data_policy.live_required' "$CONFIG_PATH")
no_simulate=$(jq -r '.live_financial_data_policy.simulate_allowed' "$CONFIG_PATH")
no_hardcode=$(jq -r '.live_financial_data_policy.use_hardcoded_values' "$CONFIG_PATH")
verify_source=$(jq -r '.live_financial_data_policy.source_verification_required' "$CONFIG_PATH")
no_memory=$(jq -r '.live_financial_data_policy.fallback_to_memory' "$CONFIG_PATH")

if [[ "$live_required" != "true" || "$no_simulate" != "false" || "$no_hardcode" != "false" || "$verify_source" != "true" || "$no_memory" != "false" ]]; then
    echo "$NOW ❌ ENFORCEMENT BLOCKED: Live financial data policy violation" | tee -a "$LOG_FILE"
    exit 1
fi

# Pass
echo "$NOW ✅ CONFIG ENFORCEMENT PASSED: All Project Lima rules validated successfully." >> "$LOG_FILE"
exit 0
