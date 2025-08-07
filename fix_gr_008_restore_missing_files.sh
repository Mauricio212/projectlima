#!/bin/bash
# FIX-GR-008 Auto-Restore Script (No Manual Edits Required)
# ✅ Compliant with Golden Rule #6

echo "🔁 Restoring FIX-1 and FIX-2 scripts..."

curl -s https://raw.githubusercontent.com/project-lima-official/scripts/main/fix_1_token_validator.py -o ~/project_lima/fix_1_token_validator.py
curl -s https://raw.githubusercontent.com/project-lima-official/scripts/main/fix_2_roi_calculator.py -o ~/project_lima/fix_2_roi_calculator.py

chmod +x ~/project_lima/fix_1_token_validator.py
chmod +x ~/project_lima/fix_2_roi_calculator.py

echo "✅ FIX scripts restored."

echo "🔁 Rebuilding token input CSV (step_3_1_tokens.csv)..."
source ~/project_lima/lima_env/bin/activate
python3 ~/project_lima/fix_1_token_validator.py

echo "✅ Token input file regenerated."

echo "🔍 Re-running watchdog for verification..."
python3 ~/project_lima/fix_gr_008_watchdog.py

echo "✅ Full restoration complete. All required files should now be present."
