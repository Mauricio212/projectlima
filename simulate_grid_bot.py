# simulate_grid_bot.py — Project Lima Phase 4
# ✅ Simulates GRID bot ROI using CDG10 configuration

import pandas as pd
from generate_grid_config import generate_grid_config

def simulate_grid_bot(symbol, df, config=None):
    if config is None:
        config = generate_grid_config(symbol, df)

    if not config['config_valid']:
        return {
            'symbol': symbol,
            'config_valid': False,
            'grid_roi': None,
            'hold_roi': None,
            'details': 'Invalid configuration — indicators out of bounds'
        }

    capital = 1000
    price = config['price']
    step_pct = config['grid_step_pct'] / 100
    grid_count = config['grid_count']

    grid_prices = [config['range_low'] * (1 + step_pct) ** i for i in range(grid_count + 1)]
    position = {'usdc': capital, 'token': 0.0, 'trades': []}
    prev_price = df.iloc[0]['close']

    for _, row in df.iterrows():
        current_price = row['close']
        for i in range(len(grid_prices) - 1):
            lower = grid_prices[i]
            upper = grid_prices[i + 1]
            order_size = capital / grid_count / current_price

            if prev_price > upper and current_price <= upper and position['usdc'] >= order_size * current_price:
                position['token'] += order_size
                position['usdc'] -= order_size * current_price
                position['trades'].append(('BUY', current_price))

            elif prev_price < lower and current_price >= lower and position['token'] >= order_size:
                position['token'] -= order_size
                position['usdc'] += order_size * current_price
                position['trades'].append(('SELL', current_price))

        prev_price = current_price

    final_price = df.iloc[-1]['close']
    final_value = position['usdc'] + position['token'] * final_price
    grid_roi = (final_value - capital) / capital * 100

    hold_entry = df.iloc[0]['close']
    hold_exit = df.iloc[-1]['close']
    hold_roi = (hold_exit - hold_entry) / hold_entry * 100

    return {
        'symbol': symbol,
        'config_valid': True,
        'grid_roi': round(grid_roi, 2),
        'hold_roi': round(hold_roi, 2),
        'trades': position['trades'],
        'config': config
    }
