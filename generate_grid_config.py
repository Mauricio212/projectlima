# generate_grid_config.py — Project Lima GRID Bot Config Generator
import pandas as pd
import numpy as np

def calculate_indicators(df):
    df = df.copy()
    df['H-L'] = df['high'] - df['low']
    df['H-PC'] = abs(df['high'] - df['close'].shift(1))
    df['L-PC'] = abs(df['low'] - df['close'].shift(1))
    df['TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1)
    df['ATR'] = df['TR'].rolling(window=14).mean()

    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))

    df['+DM'] = np.where((df['high'] - df['high'].shift(1)) > (df['low'].shift(1) - df['low']),
                         df['high'] - df['high'].shift(1), 0)
    df['-DM'] = np.where((df['low'].shift(1) - df['low']) > (df['high'] - df['high'].shift(1)),
                         df['low'].shift(1) - df['low'], 0)
    df['+DI'] = 100 * (df['+DM'].rolling(window=14).sum() / df['ATR'])
    df['-DI'] = 100 * (df['-DM'].rolling(window=14).sum() / df['ATR'])
    df['DX'] = (abs(df['+DI'] - df['-DI']) / (df['+DI'] + df['-DI'])) * 100
    df['ADX'] = df['DX'].rolling(window=14).mean()

    df['donchian_high'] = df['high'].rolling(window=20).max()
    df['donchian_low'] = df['low'].rolling(window=20).min()

    return df

def generate_grid_config(symbol, df):
    df = calculate_indicators(df)
    latest = df.iloc[-1]

    price = latest['close']
    atr = latest['ATR']
    rsi = latest['RSI']
    adx = latest['ADX']
    high = latest['donchian_high']
    low = latest['donchian_low']

    config_valid = (atr > 0) and (7 <= (atr / price) * 100 <= 15) and (adx > 20) and (rsi > 50)

    grid_range_low = max(price - 1.5 * atr, low)
    grid_range_high = min(price + 1.5 * atr, high)
    range_width = grid_range_high - grid_range_low

    grid_step_pct = max(1.5, (atr / price) * 100)
    grid_count = max(5, int((range_width / price) / (grid_step_pct / 100)))

    return {
        'symbol': symbol,
        'price': price,
        'ATR': atr,
        'RSI': rsi,
        'ADX': adx,
        'Donchian_High': high,
        'Donchian_Low': low,
        'range_low': grid_range_low,
        'range_high': grid_range_high,
        'grid_step_pct': grid_step_pct,
        'grid_count': grid_count,
        'trailing_up': adx > 20 and rsi > 55,
        'stop_loss_pct': 12,
        'expansion_floor_pct': -20,
        'config_valid': config_valid
    }
