import requests

def check_usd_pairs():
    try:
        url = "https://api.exchange.coinbase.com/products"
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            products = response.json()
            
            # Check USD pairs instead of USDC
            usd_pairs = []
            for product in products:
                if (product.get('quote_currency') == 'USD' and 
                    product.get('status') == 'online' and
                    product.get('trading_disabled') == False):
                    usd_pairs.append(product['id'])
            
            print(f"Active USD pairs found: {len(usd_pairs)}")
            print("\nFirst 20 active USD pairs:")
            for i, pair in enumerate(usd_pairs[:20]):
                print(f"  {i+1}. {pair}")
                
            # Check specifically for major cryptos
            major_cryptos = ['BTC', 'ETH', 'ADA', 'SOL', 'DOGE', 'MATIC', 'LTC']
            print(f"\nMajor crypto USD pairs available:")
            for crypto in major_cryptos:
                pair_name = f"{crypto}-USD"
                if pair_name in usd_pairs:
                    print(f"  ✅ {pair_name}")
                else:
                    print(f"  ❌ {pair_name}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    check_usd_pairs()
