import requests
import json

def test_coinbase_api():
    try:
        url = "https://api.exchange.coinbase.com/products"
        response = requests.get(url, timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            products = response.json()
            print(f"Total products found: {len(products)}")
            
            # Filter for USDC pairs
            usdc_pairs = []
            for product in products:
                if product.get('quote_currency') == 'USDC':
                    usdc_pairs.append({
                        'pair': product['id'],
                        'base': product['base_currency'],
                        'status': product.get('status'),
                        'trading_disabled': product.get('trading_disabled')
                    })
            
            print(f"Total USDC pairs found: {len(usdc_pairs)}")
            
            # Show first 10 USDC pairs
            print("\nFirst 10 USDC pairs:")
            for i, pair in enumerate(usdc_pairs[:10]):
                print(f"  {i+1}. {pair}")
                
            # Show online trading pairs only
            active_pairs = [p for p in usdc_pairs if p['status'] == 'online' and not p['trading_disabled']]
            print(f"\nActive trading USDC pairs: {len(active_pairs)}")
            for pair in active_pairs:
                print(f"  {pair['pair']}")
                
        else:
            print(f"API Error: {response.text}")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_coinbase_api()
