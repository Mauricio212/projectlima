# export_lima_cert_logs_to_sheets.py

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from pathlib import Path

# === CONFIG ===
SHEET_NAME = "Project Lima Certification Logs"
FILES_TO_EXPORT = [
    "logs/fix_2_token_roi_log.csv",
    "logs/grid_vs_hold_filter_log.csv",
    "logs/fix_4_decision_log.csv",
    "logs/system_certification.log",
    "logs/cron_heartbeat.log",
    "logs/pipeline_health_cron.log",
]

# === Google Sheets Auth ===
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("/home/ec2-user/project_lima/secrets/google_sheets_credentials.json", scope)
client = gspread.authorize(creds)
spreadsheet = client.open(SHEET_NAME)

# === Process and export each log file
for path_str in FILES_TO_EXPORT:
    path = Path(f"/home/ec2-user/project_lima/{path_str}")
    if not path.exists():
        print(f"[⚠️] Skipped missing log: {path.name}")
        continue

    with path.open("r") as f:
        lines = [line.strip().split(",") for line in f.readlines() if line.strip()]
    
    if not lines:
        print(f"[⚠️] Empty: {path.name}")
        continue

    # Create or clear sheet tab
    sheet_title = path.stem[:100]
    try:
        worksheet = spreadsheet.worksheet(sheet_title)
        spreadsheet.del_worksheet(worksheet)
        worksheet = spreadsheet.add_worksheet(title=sheet_title, rows="1000", cols="20")
    except gspread.exceptions.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(title=sheet_title, rows="1000", cols="20")

    worksheet.update("A1", lines)
    print(f"[✅] Exported: {sheet_title}")
