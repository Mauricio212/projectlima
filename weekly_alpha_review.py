import pandas as pd
import sqlite3
import datetime

# Connect to DB and get last 30 days
conn = sqlite3.connect("project_lima.db")
df = pd.read_sql("SELECT * FROM indicator_logs", conn)
df["Alpha"] = df["Alpha"].astype(float)
df["Confidence"] = df["Confidence"].astype(float)
df["timestamp"] = pd.date_range(end=datetime.datetime.utcnow(), periods=len(df), freq='D')

# Weekly score logic
rolling_alpha = df["Alpha"].rolling(window=7).mean()
decay_flag = rolling_alpha.pct_change().iloc[-1] < -0.25

print("📊 Alpha Weekly Review")
print(f"7-day average Alpha: {round(rolling_alpha.iloc[-1], 5)}")
print(f"Decay flag triggered: {decay_flag}")

# Optional: flag for retrain or scoring downgrade
if decay_flag:
    print("⚠️ Recommend review or downgrade of token scoring.")
else:
    print("✅ Signal stable. No adjustment required.")

conn.close()
