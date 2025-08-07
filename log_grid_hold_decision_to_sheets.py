# log_grid_hold_decision_to_sheets.py

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pandas as pd

# === CONFIGURATION ===
SHEET_NAME = "Project Lima Decision Log"
CSV_FILE = "/home/ec2-user/project_lima/grid_hold_output/step_3_2_token_roi.csv"

# Google Sheets auth
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("/home/ec2-user/project_lima/secrets/google_sheets_credentials.json", scope)
client = gspread.authorize(creds)

# Load ROI data
df = pd.read_csv(CSV_FILE)

# Compute average ROI
grid_df = df[df["symbol"].str.upper() != "HOLD"]
hold_df = df[df["symbol"].str.upper() == "HOLD"]
grid_roi = grid_df["grid_roi"].mean()
hold_roi = hold_df["hold_roi"].mean()

# Determine recommendation
if grid_roi > hold_roi:
    decision = "INVEST IN GRID"
else:
    decision = "INVEST IN HOLD"

# Prepare log row
timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
row = [timestamp, round(grid_roi, 2), round(hold_roi, 2), decision]

# Write to sheet
sheet = client.open(SHEET_NAME).sheet1
sheet.append_row(row)

print(f"[✅] Logged decision to Google Sheet: {SHEET_NAME}")
