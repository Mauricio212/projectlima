import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import numpy as np
import sqlite3

# Authenticate
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

# Connect to sheet
sheet = client.open("LIMA_Grid_Alpha_Export").sheet1

# Load data
conn = sqlite3.connect("project_lima.db")
df = pd.read_sql("SELECT Date, Alpha, Confidence FROM indicator_logs", conn)
conn.close()

# Clean and format rows
rows = [["Date", "Alpha", "Confidence"]] + [
    [
        str(row["Date"]),
        "" if pd.isna(row["Alpha"]) or not np.isfinite(row["Alpha"]) else round(row["Alpha"], 5),
        "" if pd.isna(row["Confidence"]) or not np.isfinite(row["Confidence"]) else round(row["Confidence"], 5),
    ]
    for _, row in df.iterrows()
]

# Upload to sheet
sheet.update(rows)
