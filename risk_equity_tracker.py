import pandas as pd
import sqlite3
import datetime

# Load existing logs
conn = sqlite3.connect("project_lima.db")
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS equity_logs (
        timestamp TEXT,
        equity REAL
    )
''')

# Simulate current equity value (replace with live equity fetch later)
equity_now = 10000  # Example only
timestamp = datetime.datetime.utcnow().isoformat()
cursor.execute("INSERT INTO equity_logs (timestamp, equity) VALUES (?, ?)", (timestamp, equity_now))
conn.commit()

# Analyze drawdown
equity_df = pd.read_sql("SELECT * FROM equity_logs", conn)
equity_df["equity"] = equity_df["equity"].astype(float)
max_equity = equity_df["equity"].cummax()
drawdown = (equity_df["equity"] - max_equity) / max_equity
current_dd = round(drawdown.iloc[-1] * 100, 2)

print(f"Current drawdown: {current_dd}%")

if current_dd < -15:
    print("🚨 Drawdown breach. Recommending PAUSE on all bots.")
else:
    print("✅ Risk profile acceptable. Continue operation.")

conn.close()
