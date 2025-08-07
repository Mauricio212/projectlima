import json
import gspread
import datetime
from oauth2client.service_account import ServiceAccountCredentials

# === CONFIG ===
CREDS_FILE = "/home/ec2-user/project_lima/secrets/sheets_service_account.json"
SPREADSHEET_NAME = "Project Lima Decision Log"
WORKSHEET_NAME = "Daily Decisions"
DECISION_FILE = "/home/ec2-user/project_lima/grid_hold_output/decision_summary.json"

def auth_sheets():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    try:
        with open(CREDS_FILE, "r") as f:
            creds_data = json.load(f)
            if creds_data.get("type") != "service_account":
                raise ValueError("❌ Invalid credential type. Expected 'service_account'.")
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        print(f"❌ ERROR during Sheets authentication: {e}")
        raise

def export_to_sheet():
    client = auth_sheets()
    try:
        sheet = client.open(SPREADSHEET_NAME)
    except Exception:
        print(f"�� Sheet '{SPREADSHEET_NAME}' not found. Creating new sheet.")
        sheet = client.create(SPREADSHEET_NAME)
    try:
        worksheet = sheet.worksheet(WORKSHEET_NAME)
    except gspread.exceptions.WorksheetNotFound:
        worksheet = sheet.add_worksheet(title=WORKSHEET_NAME, rows="100", cols="20")
        worksheet.append_row(["Date", "Symbol", "GRID ROI", "HOLD ROI", "Step %", "Decision"])

    with open(DECISION_FILE, "r") as f:
        data = json.load(f)

    now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    row = [
        now,
        data.get("symbol", "N/A"),
        data.get("grid_roi", "N/A"),
        data.get("hold_roi", "N/A"),
        data.get("step_pct", "N/A"),
        "GRID" if float(data.get("grid_roi", 0)) > float(data.get("hold_roi", 0)) else "HOLD"
    ]
    worksheet.append_row(row)
    print(f"✅ Export complete. Row added: {row}")

if __name__ == "__main__":
    export_to_sheet()

