from alpaca_trade_api.rest import REST

# Alpaca API credentials
ALPACA_API_KEY = "<AK9YWX7JNR46WFH4102E>"
ALPACA_SECRET_KEY = "<Vf7lQDQV8LWKCXaEcL9kaMBDrXQgHYHleyoOEDHJ>"
BASE_URL = "https://paper-api.alpaca.markets"  # Paper trading base URL

# Create an API object
api = REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, BASE_URL)

# Fetch real-time stock data
symbol = "AAPL"  # Example stock symbol
try:
    latest_trade = api.get_latest_trade(symbol)
    print(f"Latest trade for {symbol}: ${latest_trade.price}")
except Exception as e:
    print(f"Error fetching market data for {symbol}:", e)
