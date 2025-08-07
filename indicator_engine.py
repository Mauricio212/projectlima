import pandas as pd
import sqlite3
import pandas_ta as ta
import os

path = "./data/ETHUSDC.csv"

# Fallback: auto-generate sample OHLCV if file is missing
if not os.path.exists(path):
    print("⚠️ ETHUSDC.csv not found. Using fallback sample data.")
    dates = pd.date_range(end=pd.Timestamp.today(), periods=30, freq='D')
    price = 2900 + pd.Series(range(30)).apply(lambda x: x * 3 + 10)
    df = pd.DataFrame({
        'Date': dates.strftime('%Y-%m-%d'),
        'Open': price * 0.98,
        'High': price * 1.01,
        'Low': price * 0.97,
        'Close': price,
        'Volume': 1000
    })
else:
    df = pd.read_csv(path)

# Indicators using pandas-ta
df['ATR'] = ta.atr(high=df['High'], low=df['Low'], close=df['Close'], length=14)
df['ADX'] = ta.adx(high=df['High'], low=df['Low'], close=df['Close'], length=14)['ADX_14']
df['RSI'] = ta.rsi(close=df['Close'], length=14)
df['DONCHIAN_HIGH'] = df['High'].rolling(window=20).max()
df['DONCHIAN_LOW'] = df['Low'].rolling(window=20).min()

# Calculate Alpha and Confidence
df['Alpha'] = df['Close'].pct_change(7) - df['Close'].pct_change(7).shift(7)
df['Confidence'] = 1 - (df['ATR'] / df['Close'])

# Save to SQLite
conn = sqlite3.connect("project_lima.db")
df.to_sql("indicator_logs", conn, if_exists="replace", index=False)
conn.close()
