# SSTI Batch Screener v1.3 – Full Scoring Logic

import yfinance as yf

def fetch_signal_data(ticker):
    data = yf.Ticker(ticker)
    hist = data.history(period="5d")
    info = data.info

    try:
        current_price = round(hist['Close'][-1], 2)
        previous_close = hist['Close'][-2]
        price_change_pct = round((current_price - previous_close) / previous_close * 100, 2)
    except:
        current_price = "N/A"
        price_change_pct = "N/A"

    signal_data = {
        "Ticker": ticker.upper(),
        "Current Price": current_price,
        "Price Change 1D (%)": price_change_pct,
        "Sector": info.get("sector", "Unknown"),
        "Market Cap": info.get("marketCap", "N/A"),
        "Volume": info.get("volume", 0),
        "Avg Volume": info.get("averageVolume", 1),
        "EPS": info.get("trailingEps", "N/A"),
        "PE Ratio": info.get("trailingPE", "N/A"),
        "Beta": info.get("beta", "N/A"),
        "Float": info.get("floatShares", 0),
        "Recent Earnings": "Check Earnings Calendar"
    }
    return signal_data

def score_signal(data):
    weights = {
        "rumors": 0.20,
        "market_sentiment": 0.15,
        "financial_news": 0.15,
        "macro_sector_news": 0.10,
        "technical_indicators": 0.20,
        "fundamental_indicators": 0.20
    }

    scores = {}

    scores["rumors"] = 65  # Placeholder

    try:
        price_change = float(data['Price Change 1D (%)'])
        scores["market_sentiment"] = 80 if price_change > 1 else 60 if price_change > 0 else 40
    except:
        scores["market_sentiment"] = 50

    try:
        pe = float(data['PE Ratio'])
        eps = float(data['EPS'])
        scores["financial_news"] = 85 if eps > 0 and pe < 50 else 60
    except:
        scores["financial_news"] = 60

    scores["macro_sector_news"] = 65  # Placeholder

    try:
        volume = float(data['Volume'])
        avg_volume = float(data['Avg Volume'])
        technical_score = 70
        if volume > 1.5 * avg_volume:
            technical_score += 5
        scores["technical_indicators"] = technical_score
    except:
        scores["technical_indicators"] = 70

    try:
        pe = float(data['PE Ratio'])
        eps = float(data['EPS'])
        fundamental_score = 75
        if eps > 0 and pe > 0:
            fundamental_score += 5
        scores["fundamental_indicators"] = fundamental_score
    except:
        scores["fundamental_indicators"] = 70

    total_score = sum(scores[key] * weights[key] for key in scores)
    return round(total_score, 2)

def generate_gpt_prompt(data):
    return f"""
Please analyze this real-time signal using the SSTI framework.

🔹 Ticker: {data['Ticker']}
🔸 Current Price: ${data['Current Price']}
🔸 Sector: {data['Sector']}
🔸 Pattern: [Insert pattern here, e.g., breakout, pullback]
🔸 Volume: {data['Volume']} vs Avg {data['Avg Volume']}
🔸 Float: {data['Float']}
🔸 Recent Earnings: {data['Recent Earnings']}
🔸 Entry Price: ${data['Current Price']}
🔸 Target Price: [Insert]
🔸 Stop-Loss: [Insert]
🔸 Projected Profit: [Insert %]
🔸 Risk/Reward: [Insert ratio]

Please provide:
- SSTI Score with component breakdown
- Final classification (Wait / Review / Consider Entry)
- Trade validation summary (profit %, pattern, R/R, entry hover)
- Journal-ready output block
- Disqualification (if applicable)
- Suggestions for scoring or validation improvements (if any)
"""

def run_batch_screener(tickers):
    prompts = []
    for ticker in tickers:
        print(f"\n📡 Analyzing {ticker}...")
        data = fetch_signal_data(ticker)
        score = score_signal(data)

        if score >= 70:
            prompt = generate_gpt_prompt(data)
            prompts.append({"Ticker": ticker, "SSTI Score": score, "Prompt": prompt})
            print(prompt)
        else:
            print(f"⛔ {ticker} disqualified — SSTI score: {score}")
    return prompts

if __name__ == "__main__":
    tickers = ["MSFT", "PLTR", "NVDA", "IONQ", "CRWD", "NEE", "FLNC", "AMPS", "FSLR", "RXRX"]
    run_batch_screener(tickers)