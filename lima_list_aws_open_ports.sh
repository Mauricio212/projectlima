#!/bin/bash
# Project Lima - AWS Open Ports Listing Script (Rule #6 Compliant)

INSTANCE_ID="i-03df00c07b9d1ce3e"   # Lima-Rebuild instance ID
REGION="us-east-1"

echo "[LIMA] Listing AWS-open ports for instance $INSTANCE_ID in $REGION..."
echo "----------------------------------------------------"

# Get security groups attached to the instance
SG_IDS=$(aws ec2 describe-instances \
    --instance-ids "$INSTANCE_ID" \
    --region "$REGION" \
    --query 'Reservations[].Instances[].SecurityGroups[].GroupId' \
    --output text)

if [ -z "$SG_IDS" ]; then
    echo "[ERROR] No security groups found for instance."
    exit 1
fi

# List inbound rules for each SG
for SG in $SG_IDS; do
    echo "[INFO] Security Group: $SG"
    aws ec2 describe-security-groups \
        --group-ids "$SG" \
        --region "$REGION" \
        --query 'SecurityGroups[].IpPermissions[].{Protocol:IpProtocol,FromPort:FromPort,ToPort:ToPort,SourceRanges:IpRanges}' \
        --output table
done

echo "----------------------------------------------------"
