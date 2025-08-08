#!/bin/bash

# Project Lima – Fix Bash command accidentally injected into app.py
# ✅ Golden Rule #6 Compliant

sed -i "/^cat << 'EOF'/,/^EOF/d" ~/project_lima/app.py
