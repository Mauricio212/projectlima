#!/bin/bash
# Project Lima - AWS Access Check Script

echo "[LIMA] Checking AWS CLI access using attached IAM role..."
echo "-----------------------------------------------"

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "[ERROR] AWS CLI is not installed on this system."
    exit 1
fi

# Try to list instances in the current account/region
aws ec2 describe-instances --query 'Reservations[].Instances[].InstanceId' --output text 2>&1

if [ $? -eq 0 ]; then
    echo "[SUCCESS] AWS CLI is working and IAM role permissions are valid."
else
    echo "[FAIL] AWS CLI could not retrieve instance details. Check IAM role and permissions."
fi

echo "-----------------------------------------------"
