#!/bin/bash
# Project Lima - AWS Ports Master File (Clean JSON, no trailing comma)

INSTANCE_ID="i-03df00c07b9d1ce3e"   # Lima-Rebuild
REGION="us-east-1"
OUTPUT_FILE="$HOME/project_lima/aws_ports_master.json"

echo "[LIMA] Updating AWS Ports Master File from live AWS data..."
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Get all SGs
SG_IDS=$(aws ec2 describe-instances \
  --instance-ids "$INSTANCE_ID" \
  --region "$REGION" \
  --query 'Reservations[].Instances[].SecurityGroups[].GroupId' \
  --output text)

if [ -z "$SG_IDS" ]; then
  echo "[FATAL] No Security Groups found for instance. Master file not updated."
  exit 1
fi

# Collect all TCP from-ports (deduped, numeric)
PORTS=$(for SG in $SG_IDS; do
  aws ec2 describe-security-groups \
    --group-ids "$SG" \
    --region "$REGION" \
    --query 'SecurityGroups[].IpPermissions[?IpProtocol==`tcp`].FromPort' \
    --output text
done | tr '\t' '\n' | grep -E '^[0-9]+$' | sort -n | uniq)

# Build JSON array safely without trailing comma
TMP_ARRAY=""
for P in $PORTS; do
  if [ -z "$TMP_ARRAY" ]; then
    TMP_ARRAY="$P"
  else
    TMP_ARRAY="$TMP_ARRAY, $P"
  fi
done

cat > "$OUTPUT_FILE" <<EOF
{
  "last_update_utc": "$TIMESTAMP",
  "source": "aws_ec2_security_groups",
  "region": "$REGION",
  "instance": {
    "name": "Lima-Rebuild",
    "public_ip": "52.200.101.103"
  },
  "allowed": {
    "tcp": [ $TMP_ARRAY ],
    "udp": []
  }
}
EOF

echo "[SUCCESS] AWS Ports Master File updated at $OUTPUT_FILE"
cat "$OUTPUT_FILE"
