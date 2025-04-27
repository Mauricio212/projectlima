# SSTI Universe Builder – Real-Time Finnhub Sector + Keyword Discovery
# Requirements: pip install finnhub-python

import finnhub

# Insert your actual API key here
FINNHUB_API_KEY = "cvr8sepr01qp88cp32h0cvr8sepr01qp88cp32hg"

# Initialize client
finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)

# Define your SSTI themes
SSTI_THEMES = [
    "AI", "artificial intelligence", "machine learning", "deep learning",
    "quantum", "data center", "cloud infrastructure", "semiconductor",
    "battery storage", "smart grid", "drug discovery", "predictive diagnostics",
    "cybersecurity", "renewables"
]

# Optional fallback Tier 1 overrides (whitelist)
TIER_1_OVERRIDES = ["QUBT", "QBTS", "IONQ", "QSI", "RXRX"]

def get_ssti_universe_from_finnhub(sector_filter="Technology", keyword_filters=None, max_results=100):
    """
    Pulls tickers using Finnhub symbol lookup and filters based on sector + keywords in description.
    Adds fallback whitelist tickers as Tier 1 overrides.
    """
    if keyword_filters is None:
        keyword_filters = SSTI_THEMES

    universe = set()
    seen = set()

    for keyword in keyword_filters:
        try:
            search_results = finnhub_client.symbol_lookup(keyword).get("result", [])
            for item in search_results:
                symbol = item.get("symbol")
                if not symbol or symbol in seen or "." in symbol:
                    continue
                seen.add(symbol)
                profile = finnhub_client.company_profile2(symbol=symbol)
                if profile.get("finnhubIndustry") == sector_filter:
                    description = profile.get("description", "").lower()
                    if any(k in description for k in keyword_filters):
                        universe.add(symbol)
                        if len(universe) >= max_results:
                            break
        except Exception as e:
            print(f"⚠️ Error fetching data for keyword '{keyword}': {e}")

    # Add fallback overrides (e.g. QUBT, QBTS, IONQ)
    universe.update(TIER_1_OVERRIDES)
    print(f"✅ Final SSTI Universe: {len(universe)} tickers")
    return sorted(list(universe))

# Example usage
def example():
    tickers = get_ssti_universe_from_finnhub(sector_filter="Technology")
    print("\nFiltered SSTI Universe:", tickers)

if __name__ == "__main__":
    example()
