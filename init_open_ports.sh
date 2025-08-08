#!/bin/bash

# Project Lima – Initialize open_ports.json
# ✅ Golden Rule #6 Compliant

mkdir -p ~/project_lima/config

cat > ~/project_lima/config/open_ports.json << 'EOF'
{
  "80": "HTTP",
  "443": "HTTPS",
  "3000": "Modal Site Feature Audit",
  "8001": "Project Lima Web Access",
  "8085": "Grid vs Hold"
}
EOF
