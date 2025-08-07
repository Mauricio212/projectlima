#!/usr/bin/env python3
"""
Project Lima - 3Commas HMAC API ATR Calculator
USES HMAC AUTHENTICATION (WORKING METHOD) + COINBASE ADVANCED DATA
"""

import requests
import pandas as pd
import numpy as np
import json
import logging
import hmac
import hashlib
import time
from datetime import datetime, timedelta
import os
import urllib.parse

# Lima Project Configuration
LIMA_CONFIG = {
    'project_name': 'GRID_vs_HOLD',
    'version': '6.0_3COMMAS_HMAC_WORKING',
    'log_level': 'INFO',
    'output_dir': '/tmp/lima_outputs',
    'results_file': '3commas_atr_results.json'
}

# Create output directory
os.makedirs(LIMA_CONFIG['output_dir'], exist_ok=True)

# Configure logging
logging.basicConfig(
    level=getattr(logging, LIMA_CONFIG['log_level']),
    format='%(asctime)s - LIMA-3C-ATR - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"{LIMA_CONFIG['output_dir']}/3commas_atr.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Your trading pairs with CORRECT Coinbase Advanced formats (USD not USDC)
TRADING_PAIRS = [
    {"rank": 1, "symbol": "BTC", "pair": "BTC-USDC", "coinbase_product": "BTC-USD"},
    {"rank": 2, "symbol": "ETH", "pair": "ETH-USDC", "coinbase_product": "ETH-USD"},
    {"rank": 3, "symbol": "XRP", "pair": "XRP-USDC", "coinbase_product": "XRP-USD"},
    {"rank": 6, "symbol": "SOL", "pair": "SOL-USDC", "coinbase_product": "SOL-USD"},
    {"rank": 8, "symbol": "DOGE", "pair": "DOGE-USDC", "coinbase_product": "DOGE-USD"},
    {"rank": 10, "symbol": "ADA", "pair": "ADA-USDC", "coinbase_product": "ADA-USD"},
    {"rank": 11, "symbol": "XLM", "pair": "XLM-USDC", "coinbase_product": "XLM-USD"},
    {"rank": 13, "symbol": "SUI", "pair": "SUI-USDC", "coinbase_product": "SUI-USD"},
    {"rank": 14, "symbol": "LINK", "pair": "LINK-USDC", "coinbase_product": "LINK-USD"},
    {"rank": 15, "symbol": "HBAR", "pair": "HBAR-USDC", "coinbase_product": "HBAR-USD"},
    {"rank": 16, "symbol": "AVAX", "pair": "AVAX-USDC", "coinbase_product": "AVAX-USD"},
    {"rank": 17, "symbol": "BCH", "pair": "BCH-USDC", "coinbase_product": "BCH-USD"},
    {"rank": 18, "symbol": "SHIB", "pair": "SHIB-USDC", "coinbase_product": "SHIB-USD"},
    {"rank": 21, "symbol": "LTC", "pair": "LTC-USDC", "coinbase_product": "LTC-USD"},
    {"rank": 22, "symbol": "DOT", "pair": "DOT-USDC", "coinbase_product": "DOT-USD"},
    {"rank": 24, "symbol": "PEPE", "pair": "PEPE-USDC", "coinbase_product": "PEPE-USD"},
    {"rank": 25, "symbol": "UNI", "pair": "UNI-USDC", "coinbase_product": "UNI-USD"},
    {"rank": 29, "symbol": "AAVE", "pair": "AAVE-USDC", "coinbase_product": "AAVE-USD"},
    {"rank": 30, "symbol": "TAO", "pair": "TAO-USDC", "coinbase_product": "TAO-USD"},
    {"rank": 32, "symbol": "NEAR", "pair": "NEAR-USDC", "coinbase_product": "NEAR-USD"},
    {"rank": 33, "symbol": "APT", "pair": "APT-USDC", "coinbase_product": "APT-USD"}
]

def load_3commas_credentials():
    """Load 3Commas HMAC credentials from Lima infrastructure"""
    creds_path = "/home/ec2-user/project_lima/secrets/3commas_api.json"
    
    try:
        with open(creds_path, 'r') as f:
            creds = json.load(f)
            
        config = {
            'api_key': creds.get('api_key'),
            'api_secret': creds.get('api_secret'),
            'base_url': 'https://api.3commas.io',
            'coinbase_account_id': creds.get('coinbase_advanced_account_id')
        }
        
        if not config['api_key'] or not config['api_secret']:
            raise ValueError("Missing API key or secret")
            
        logger.info(f"✅ 3Commas HMAC credentials loaded")
        return config
        
    except Exception as e:
        logger.error(f"❌ Failed to load 3Commas credentials: {e}")
        raise

class ThreeCommasHMACAPI:
    """3Commas API client using HMAC authentication (working method)"""
    
    def __init__(self, api_key, api_secret, base_url):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        
    def _generate_signature(self, query_string):
        """Generate HMAC-SHA256 signature for 3Commas API"""
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    def _make_request(self, endpoint, params=None):
        """Make authenticated HMAC request to 3Commas API"""
        if params is None:
            params = {}
            
        # Create query string
        query_string = urllib.parse.urlencode(sorted(params.items()))
        
        # Generate HMAC signature
        signature = self._generate_signature(query_string)
        
        # Headers for 3Commas HMAC
        headers = {
            'APIKEY': self.api_key,
            'Signature': signature
        }
        
        url = f"{self.base_url}/{endpoint}"
        if query_string:
            url += f"?{query_string}"
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ 3Commas HMAC API request failed for {endpoint}: {e}")
            return None
    
    def get_accounts(self):
        """Get trading accounts - working endpoint"""
        endpoint = "public/api/ver1/accounts"
        return self._make_request(endpoint)
    
    def validate_api(self):
        """Validate API credentials using working endpoint"""
        endpoint = "public/api/ver1/validate"
        return self._make_request(endpoint)

def get_coinbase_advanced_data(pair, days=30):
    """Get data directly from Coinbase Advanced API using correct pair format"""
    try:
        # Use the correct Coinbase product ID from pair definition
        coinbase_product = pair['coinbase_product']
        symbol = pair['symbol']
        
        # Coinbase Advanced public API endpoint for candles
        url = f"https://api.exchange.coinbase.com/products/{coinbase_product}/candles"
        
        # Calculate date range
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)
        
        params = {
            'start': start_time.isoformat(),
            'end': end_time.isoformat(),
            'granularity': 86400  # 1 day candles
        }
        
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        if not data:
            return None
            
        # Convert Coinbase data to DataFrame
        # Coinbase returns: [timestamp, low, high, open, close, volume]
        df = pd.DataFrame(data, columns=['timestamp', 'low', 'high', 'open', 'close', 'volume'])
        
        # Convert timestamp from unix to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        
        # Convert price columns to float
        price_columns = ['low', 'high', 'open', 'close', 'volume']
        for col in price_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Sort by timestamp (oldest first)
        df = df.sort_values('timestamp')
        df = df.dropna()
        
        logger.info(f"✅ Coinbase Advanced data fetched for {symbol} ({coinbase_product}): {len(df)} points")
        return df
        
    except Exception as e:
        logger.warning(f"⚠️ Coinbase Advanced failed for {symbol} ({coinbase_product}): {e}")
        return None

def calculate_atr(df, period=14):
    """Calculate Average True Range (ATR)"""
    if df is None or len(df) < period + 1:
        return None, None
    
    df = df.copy()
    
    # Calculate True Range
    df['prev_close'] = df['close'].shift(1)
    df['tr1'] = df['high'] - df['low']
    df['tr2'] = abs(df['high'] - df['prev_close'])
    df['tr3'] = abs(df['low'] - df['prev_close'])
    df['true_range'] = df[['tr1', 'tr2', 'tr3']].max(axis=1)
    
    # Calculate ATR
    df['atr'] = df['true_range'].rolling(window=period).mean()
    
    # Get current values
    current_price = df['close'].iloc[-1]
    current_atr = df['atr'].iloc[-1]
    
    if pd.isna(current_atr) or pd.isna(current_price) or current_price == 0:
        return None, None
    
    # Calculate ATR percentage
    atr_percentage = (current_atr / current_price) * 100
    
    return float(current_atr), float(atr_percentage)

def analyze_pairs_atr(pairs, atr_threshold=7.0):
    """Analyze pairs using 3Commas HMAC + Coinbase Advanced data"""
    
    # Load 3Commas credentials and test connection
    creds_config = load_3commas_credentials()
    
    api_client = ThreeCommasHMACAPI(
        creds_config['api_key'],
        creds_config['api_secret'],
        creds_config['base_url']
    )
    
    # Test 3Commas connection
    logger.info("🔑 Testing 3Commas HMAC authentication...")
    validation = api_client.validate_api()
    if validation:
        logger.info("✅ 3Commas HMAC API authenticated successfully")
    else:
        logger.warning("⚠️ 3Commas API validation failed, proceeding with Coinbase data only")
    
    results = []
    
    logger.info(f"🚀 Starting ATR analysis for {len(pairs)} pairs")
    logger.info(f"📡 Data source: Coinbase Advanced API (public endpoints)")
    logger.info(f"🎯 ATR threshold: {atr_threshold}%")
    
    for i, pair in enumerate(pairs):
        logger.info(f"[{i+1}/{len(pairs)}] Analyzing {pair['symbol']} via Coinbase Advanced ({pair['coinbase_product']})")
        
        # Get OHLC data from Coinbase Advanced using correct pair format
        df = get_coinbase_advanced_data(pair)
        
        if df is not None:
            # Calculate ATR
            atr_value, atr_percentage = calculate_atr(df)
            
            if atr_value is not None and atr_percentage is not None:
                result = {
                    'timestamp': datetime.now().isoformat(),
                    'rank': pair['rank'],
                    'symbol': pair['symbol'],
                    'pair': pair['pair'],
                    'current_price': float(df['close'].iloc[-1]),
                    'atr_value': atr_value,
                    'atr_percentage': atr_percentage,
                    'meets_threshold': int(atr_percentage >= atr_threshold),
                    'data_points': len(df),
                    'data_source': 'coinbase_advanced_public'
                }
                results.append(result)
                
                status = "✅ PASS" if atr_percentage >= atr_threshold else "❌ FAIL"
                logger.info(f"  💹 {pair['symbol']}: ATR {atr_percentage:.2f}% {status}")
            else:
                logger.warning(f"  ⚠️ {pair['symbol']}: Could not calculate ATR")
        else:
            logger.error(f"  ❌ {pair['symbol']}: No data available")
        
        # Small delay between requests
        time.sleep(0.2)
    
    logger.info(f"🏁 Analysis complete: {len(results)} pairs processed")
    return results

def save_results(results, filename=None):
    """Save results in Lima format"""
    if filename is None:
        filename = LIMA_CONFIG['results_file']
    
    filepath = os.path.join(LIMA_CONFIG['output_dir'], filename)
    
    lima_output = {
        'project': LIMA_CONFIG['project_name'],
        'version': LIMA_CONFIG['version'],
        'timestamp': datetime.now().isoformat(),
        'analysis_type': 'ATR_ANALYSIS_3COMMAS_HMAC_COINBASE',
        'data_source': 'coinbase_advanced_public_api',
        'threshold': 7.0,
        'total_pairs': len(results),
        'qualifying_pairs': len([r for r in results if r['meets_threshold']]),
        'results': results
    }
    
    with open(filepath, 'w') as f:
        json.dump(lima_output, f, indent=2)
    
    logger.info(f"💾 Results saved to {filepath}")
    
    # Save CSV
    csv_file = filepath.replace('.json', '.csv')
    if results:
        df = pd.DataFrame(results)
        df.to_csv(csv_file, index=False)
        logger.info(f"📊 CSV saved to {csv_file}")

def display_results(results, atr_threshold=7.0):
    """Display comprehensive results"""
    if not results:
        print("❌ No results to display")
        return
    
    results_sorted = sorted(results, key=lambda x: x['atr_percentage'], reverse=True)
    
    print("\n" + "="*80)
    print("🚀 PROJECT LIMA - 3COMMAS HMAC + COINBASE ADVANCED ATR ANALYSIS")
    print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"�� Data Source: Coinbase Advanced API (Public)")
    print(f"🔑 Authentication: 3Commas HMAC (Working Method)")
    print("="*80)
    print(f"🎯 Threshold: {atr_threshold}% ATR")
    print(f"📊 Total Pairs Analyzed: {len(results_sorted)}")
    print(f"✅ Pairs Meeting Threshold: {len([r for r in results_sorted if r['meets_threshold']])}")
    print("="*80)
    
    print(f"{'Rank':<4} {'Symbol':<6} {'Pair':<12} {'Price':<16} {'ATR %':<8} {'Status':<8}")
    print("-" * 85)
    
    for result in results_sorted:
        status = "✅ PASS" if result['meets_threshold'] else "❌ FAIL"
        print(f"{result['rank']:<4} {result['symbol']:<6} {result['pair']:<12} "
              f"${result['current_price']:<15.8f} {result['atr_percentage']:<7.2f}% {status}")
    
    # Show qualifying pairs
    qualifying_pairs = [r for r in results_sorted if r['meets_threshold']]
    if qualifying_pairs:
        print("\n" + "="*50)
        print("🎯 QUALIFYING PAIRS FOR GRID TRADING")
        print("="*50)
        for result in qualifying_pairs:
            print(f"💰 {result['symbol']:<6} {result['pair']:<12} ATR: {result['atr_percentage']:.2f}%")
            
        print("\n🚀 GRID BOT DEPLOYMENT RECOMMENDATIONS:")
        for result in qualifying_pairs[:5]:  # Top 5
            print(f"   {result['rank']:>2}. {result['symbol']} - ATR: {result['atr_percentage']:.2f}% - Price: ${result['current_price']:.8f}")
    else:
        print("\n" + "="*50)
        print("⚠️ NO PAIRS MEET THE 7% ATR THRESHOLD")
        print("💡 Consider lowering threshold to 5% or wait for market volatility")
        print("="*50)
        
        # Show top 3 closest to threshold
        top_3 = results_sorted[:3]
        print("\n🔍 TOP 3 CLOSEST TO THRESHOLD:")
        for result in top_3:
            gap = 7.0 - result['atr_percentage']
            print(f"   {result['symbol']} - ATR: {result['atr_percentage']:.2f}% (need {gap:.2f}% more)")

def main():
    """Main function - Working 3Commas HMAC + Coinbase Advanced ATR Analysis"""
    print("🚀 PROJECT LIMA - 3COMMAS HMAC + COINBASE ADVANCED ATR CALCULATOR")
    logger.info("🚀 Starting Lima 3Commas HMAC + Coinbase Advanced ATR Calculator")
    
    try:
        # Run analysis using working methods
        results = analyze_pairs_atr(TRADING_PAIRS)
        
        # Display and save results
        display_results(results)
        
        if results:
            save_results(results)
            logger.info("✅ ATR analysis completed successfully")
            print("\n✅ ANALYSIS COMPLETED SUCCESSFULLY!")
            print(f"📁 Results saved to: {LIMA_CONFIG['output_dir']}")
        else:
            logger.error("❌ No results generated")
            print("\n❌ ANALYSIS FAILED")
            
    except Exception as e:
        logger.error(f"❌ Script failed: {e}")
        print(f"\n❌ SCRIPT FAILED: {e}")

if __name__ == "__main__":
    main()
