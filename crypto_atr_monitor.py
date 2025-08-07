#!/usr/bin/env python3
"""
Project Lima - ATR-Based Live Crypto Monitor
Monitors specified crypto pairs and identifies those with ATR > 7% using VERIFIED LIVE DATA ONLY

GOLDEN RULE COMPLIANCE:
- ALWAYS USE LIVE AND VERIFIED DATA
- NEVER DEVIATE FROM REAL MARKET DATA  
- 0% TOLERANCE FOR SIMULATED DATA

Filtering Criteria: ATR for last 10 days > 7%

Requirements: pip install requests pandas numpy
"""

import requests
import pandas as pd
import numpy as np
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - ATR-MONITOR - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ATRCryptoMonitor:
    """ATR-based crypto monitor using VERIFIED LIVE DATA ONLY"""
    
    def __init__(self):
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # SPECIFIED CRYPTO PAIRS TO MONITOR (exact list from user)
        self.crypto_pairs = [
            {'rank': 1, 'name': 'Bitcoin', 'symbol': 'BTC', 'pair': 'BTC-USDC'},
            {'rank': 2, 'name': 'Ethereum', 'symbol': 'ETH', 'pair': 'ETH-USDC'},
            {'rank': 3, 'name': 'XRP', 'symbol': 'XRP', 'pair': 'XRP-USDC'},
            {'rank': 6, 'name': 'Solana', 'symbol': 'SOL', 'pair': 'SOL-USDC'},
            {'rank': 8, 'name': 'Dogecoin', 'symbol': 'DOGE', 'pair': 'DOGE-USDC'},
            {'rank': 10, 'name': 'Cardano', 'symbol': 'ADA', 'pair': 'ADA-USDC'},
            {'rank': 11, 'name': 'Stellar', 'symbol': 'XLM', 'pair': 'XLM-USDC'},
            {'rank': 13, 'name': 'Sui', 'symbol': 'SUI', 'pair': 'SUI-USDC'},
            {'rank': 14, 'name': 'Chainlink', 'symbol': 'LINK', 'pair': 'LINK-USDC'},
            {'rank': 15, 'name': 'Hedera', 'symbol': 'HBAR', 'pair': 'HBAR-USDC'},
            {'rank': 16, 'name': 'Avalanche', 'symbol': 'AVAX', 'pair': 'AVAX-USDC'},
            {'rank': 17, 'name': 'Bitcoin Cash', 'symbol': 'BCH', 'pair': 'BCH-USDC'},
            {'rank': 18, 'name': 'Shiba Inu', 'symbol': 'SHIB', 'pair': 'SHIB-USDC'},
            {'rank': 21, 'name': 'Litecoin', 'symbol': 'LTC', 'pair': 'LTC-USDC'},
            {'rank': 22, 'name': 'Polkadot', 'symbol': 'DOT', 'pair': 'DOT-USDC'},
            {'rank': 24, 'name': 'Pepe', 'symbol': 'PEPE', 'pair': 'PEPE-USDC'},
            {'rank': 25, 'name': 'Uniswap', 'symbol': 'UNI', 'pair': 'UNI-USDC'},
            {'rank': 29, 'name': 'Aave', 'symbol': 'AAVE', 'pair': 'AAVE-USDC'},
            {'rank': 30, 'name': 'Bittensor', 'symbol': 'TAO', 'pair': 'TAO-USDC'},
            {'rank': 32, 'name': 'NEAR Protocol', 'symbol': 'NEAR', 'pair': 'NEAR-USDC'},
            {'rank': 33, 'name': 'Aptos', 'symbol': 'APT', 'pair': 'APT-USDC'}
        ]
        
        # CoinGecko token ID mapping for API calls
        self.token_ids = {
            'BTC': 'bitcoin', 'ETH': 'ethereum', 'XRP': 'ripple',
            'SOL': 'solana', 'DOGE': 'dogecoin', 'ADA': 'cardano',
            'XLM': 'stellar', 'SUI': 'sui', 'LINK': 'chainlink',
            'HBAR': 'hedera-hashgraph', 'AVAX': 'avalanche-2', 'BCH': 'bitcoin-cash',
            'SHIB': 'shiba-inu', 'LTC': 'litecoin', 'DOT': 'polkadot',
            'PEPE': 'pepe', 'UNI': 'uniswap', 'AAVE': 'aave',
            'TAO': 'bittensor', 'NEAR': 'near', 'APT': 'aptos'
        }
        
        # FILTERING CRITERIA
        self.atr_threshold = 7.0  # ATR > 7%
        self.atr_period = 10      # Last 10 days
        
        # Data storage
        self.live_data = {}
        self.qualifying_tokens = []
        
        logger.info(f"🔴 ATR MONITOR INITIALIZED - SESSION: {self.session_id}")
        logger.info(f"📊 MONITORING {len(self.crypto_pairs)} CRYPTO PAIRS")
        logger.info(f"🎯 CRITERIA: ATR (10-day) > {self.atr_threshold}%")
        logger.info("⚠️  USING VERIFIED LIVE DATA ONLY - NO SIMULATED DATA")
    
    def get_live_ohlc_data(self, symbol: str) -> Optional[pd.DataFrame]:
        """Fetch VERIFIED live OHLC data for ATR calculation"""
        
        coin_id = self.token_ids.get(symbol)
        if not coin_id:
            logger.error(f"❌ Unknown token ID for {symbol}")
            return None
        
        try:
            # Get OHLC data for last 10+ days to ensure we have enough data
            url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/ohlc"
            params = {
                'vs_currency': 'usd',
                'days': 15  # Get 15 days to ensure we have 10 complete days
            }
            
            response = requests.get(url, params=params, timeout=20)
            response.raise_for_status()
            
            data = response.json()
            
            if not data or len(data) < self.atr_period:
                logger.warning(f"⚠️ Insufficient OHLC data for {symbol}: {len(data) if data else 0} days")
                return None
            
            # Convert to DataFrame
            df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close'])
            df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
            
            # Sort by date and take last 10 days
            df = df.sort_values('date').tail(self.atr_period).reset_index(drop=True)
            
            logger.info(f"📡 {symbol}: Retrieved {len(df)} days of LIVE OHLC data")
            return df
            
        except Exception as e:
            logger.error(f"❌ Failed to fetch OHLC data for {symbol}: {e}")
            return None
    
    def calculate_atr(self, ohlc_data: pd.DataFrame, symbol: str) -> Optional[float]:
        """Calculate Average True Range (ATR) from LIVE OHLC data"""
        
        if ohlc_data is None or len(ohlc_data) < 2:
            logger.error(f"❌ Insufficient data for ATR calculation: {symbol}")
            return None
        
        try:
            # Calculate True Range for each day
            high = ohlc_data['high'].values
            low = ohlc_data['low'].values
            close = ohlc_data['close'].values
            
            # True Range = max(High-Low, abs(High-PrevClose), abs(Low-PrevClose))
            true_ranges = []
            
            for i in range(1, len(ohlc_data)):
                tr1 = high[i] - low[i]  # High - Low
                tr2 = abs(high[i] - close[i-1])  # abs(High - Previous Close)
                tr3 = abs(low[i] - close[i-1])   # abs(Low - Previous Close)
                
                true_range = max(tr1, tr2, tr3)
                true_ranges.append(true_range)
            
            if not true_ranges:
                logger.error(f"❌ No true ranges calculated for {symbol}")
                return None
            
            # Calculate ATR (Average True Range)
            atr_value = np.mean(true_ranges)
            
            # Convert ATR to percentage of current price
            current_price = close[-1]
            atr_percentage = (atr_value / current_price) * 100
            
            logger.info(f"📊 {symbol}: ATR = {atr_value:.6f}, ATR% = {atr_percentage:.2f}%")
            return atr_percentage
            
        except Exception as e:
            logger.error(f"❌ Error calculating ATR for {symbol}: {e}")
            return None
    
    def get_current_price(self, symbol: str) -> Optional[float]:
        """Get current live price for additional context"""
        
        coin_id = self.token_ids.get(symbol)
        if not coin_id:
            return None
        
        try:
            url = "https://api.coingecko.com/api/v3/simple/price"
            params = {
                'ids': coin_id,
                'vs_currencies': 'usd',
                'include_24hr_change': 'true'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            price = data[coin_id]['usd']
            change_24h = data[coin_id].get('usd_24h_change', 0)
            
            logger.info(f"💰 {symbol}: ${price} ({change_24h:+.2f}% 24h)")
            return float(price)
            
        except Exception as e:
            logger.error(f"❌ Failed to fetch current price for {symbol}: {e}")
            return None
    
    def analyze_token(self, crypto_info: Dict) -> Optional[Dict]:
        """Analyze a single crypto token using VERIFIED LIVE DATA"""
        
        symbol = crypto_info['symbol']
        pair = crypto_info['pair']
        rank = crypto_info['rank']
        name = crypto_info['name']
        
        logger.info(f"🔍 Analyzing {name} ({symbol}) - Rank #{rank}")
        
        # Get LIVE OHLC data
        ohlc_data = self.get_live_ohlc_data(symbol)
        if ohlc_data is None:
            logger.error(f"❌ Cannot analyze {symbol} - no OHLC data")
            return None
        
        # Calculate ATR from LIVE data
        atr_percentage = self.calculate_atr(ohlc_data, symbol)
        if atr_percentage is None:
            logger.error(f"❌ Cannot analyze {symbol} - ATR calculation failed")
            return None
        
        # Get current price for context
        current_price = self.get_current_price(symbol)
        
        # Rate limiting for API calls
        time.sleep(0.8)  # Slightly longer delay for OHLC + price calls
        
        # Create analysis result
        analysis = {
            'rank': rank,
            'name': name,
            'symbol': symbol,
            'pair': pair,
            'current_price': current_price,
            'atr_percentage': round(atr_percentage, 2),
            'atr_period_days': self.atr_period,
            'timestamp': datetime.now().isoformat(),
            'data_source': 'CoinGecko_OHLC_API_LIVE',
            'session_id': self.session_id
        }
        
        return analysis
    
    def apply_atr_criteria(self, analysis: Dict) -> Tuple[bool, str]:
        """Apply ATR filtering criteria"""
        
        symbol = analysis['symbol']
        atr_percentage = analysis['atr_percentage']
        
        # Criterion: ATR (10-day) > 7%
        qualified = atr_percentage > self.atr_threshold
        
        # Create audit message
        if qualified:
            audit_msg = f"✅ QUALIFIED: ATR {atr_percentage}% > {self.atr_threshold}%"
        else:
            audit_msg = f"❌ EXCLUDED: ATR {atr_percentage}% ≤ {self.atr_threshold}%"
        
        logger.info(f"🎯 {symbol}: {audit_msg}")
        return qualified, audit_msg
    
    def monitor_all_pairs(self) -> List[Dict]:
        """Monitor all specified crypto pairs and identify qualifying ones"""
        
        logger.info(f"🚀 STARTING ATR MONITORING OF {len(self.crypto_pairs)} CRYPTO PAIRS")
        logger.info("⚠️  USING VERIFIED LIVE DATA ONLY")
        
        all_analyses = []
        qualifying_tokens = []
        
        for i, crypto_info in enumerate(self.crypto_pairs, 1):
            symbol = crypto_info['symbol']
            logger.info(f"📊 Processing {i}/{len(self.crypto_pairs)}: {symbol}")
            
            try:
                # Analyze token with LIVE data
                analysis = self.analyze_token(crypto_info)
                if analysis is None:
                    logger.warning(f"⚠️ Skipping {symbol} - analysis failed")
                    continue
                
                # Apply ATR filtering criteria
                qualified, audit_msg = self.apply_atr_criteria(analysis)
                analysis['qualified'] = qualified
                analysis['audit_message'] = audit_msg
                
                all_analyses.append(analysis)
                
                if qualified:
                    qualifying_tokens.append(analysis)
                    logger.info(f"✅ {symbol} QUALIFIED for Project Lima (ATR: {analysis['atr_percentage']}%)")
                else:
                    logger.info(f"❌ {symbol} EXCLUDED from Project Lima (ATR: {analysis['atr_percentage']}%)")
                
            except Exception as e:
                logger.error(f"❌ Error processing {symbol}: {e}")
                continue
        
        # Store results
        self.live_data = all_analyses
        self.qualifying_tokens = qualifying_tokens
        
        logger.info(f"🎯 ATR MONITORING COMPLETE: {len(qualifying_tokens)}/{len(all_analyses)} tokens qualified")
        return qualifying_tokens
    
    def generate_report(self) -> str:
        """Generate comprehensive ATR monitoring report"""
        
        if not self.live_data:
            return "❌ No data available for report generation"
        
        total_analyzed = len(self.live_data)
        total_qualified = len(self.qualifying_tokens)
        qualification_rate = (total_qualified / total_analyzed * 100) if total_analyzed > 0 else 0
        
        # Calculate statistics
        atr_values = [token['atr_percentage'] for token in self.live_data]
        avg_atr = np.mean(atr_values) if atr_values else 0
        max_atr = max(atr_values) if atr_values else 0
        min_atr = min(atr_values) if atr_values else 0
        
        report = [
            "=" * 80,
            "📊 PROJECT LIMA - ATR-BASED CRYPTO MONITORING REPORT",
            "=" * 80,
            f"📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"🆔 Session: {self.session_id}",
            f"📡 Data Source: CoinGecko OHLC API (VERIFIED LIVE DATA)",
            "",
            "🎯 FILTERING CRITERIA:",
            f"  • ATR Period: {self.atr_period} days",
            f"  • ATR Threshold: > {self.atr_threshold}%",
            "",
            "📋 MONITORING SUMMARY:",
            f"  • Total Pairs Analyzed: {total_analyzed}/{len(self.crypto_pairs)}",
            f"  • Qualified Pairs: {total_qualified}",
            f"  • Qualification Rate: {qualification_rate:.1f}%",
            f"  • Average ATR: {avg_atr:.2f}%",
            f"  • Highest ATR: {max_atr:.2f}%",
            f"  • Lowest ATR: {min_atr:.2f}%",
            "",
            "✅ QUALIFYING CRYPTO PAIRS (ATR > 7%):",
            "-" * 80,
        ]
        
        if self.qualifying_tokens:
            report.append(f"{'Rank':<6} {'Symbol':<8} {'Pair':<12} {'Price':<12} {'ATR%':<8} {'Status':<12}")
            report.append("-" * 80)
            
            # Sort by ATR percentage (highest first)
            sorted_qualified = sorted(self.qualifying_tokens, 
                                    key=lambda x: x['atr_percentage'], 
                                    reverse=True)
            
            for token_data in sorted_qualified:
                rank = token_data['rank']
                symbol = token_data['symbol']
                pair = token_data['pair']
                price = f"${token_data['current_price']:.4f}" if token_data['current_price'] else "N/A"
                atr_pct = f"{token_data['atr_percentage']:.2f}%"
                status = "QUALIFIED"
                
                report.append(f"{rank:<6} {symbol:<8} {pair:<12} {price:<12} {atr_pct:<8} {status:<12}")
        else:
            report.append("No crypto pairs qualified under ATR > 7% criteria.")
        
        # Add excluded tokens section
        excluded_tokens = [token for token in self.live_data if not token['qualified']]
        if excluded_tokens:
            report.extend([
                "",
                "❌ EXCLUDED CRYPTO PAIRS (ATR ≤ 7%):",
                "-" * 80,
                f"{'Rank':<6} {'Symbol':<8} {'Pair':<12} {'Price':<12} {'ATR%':<8} {'Status':<12}",
                "-" * 80
            ])
            
            # Sort excluded by ATR (highest first)
            sorted_excluded = sorted(excluded_tokens, 
                                   key=lambda x: x['atr_percentage'], 
                                   reverse=True)
            
            for token_data in sorted_excluded[:10]:  # Show top 10 excluded
                rank = token_data['rank']
                symbol = token_data['symbol']
                pair = token_data['pair']
                price = f"${token_data['current_price']:.4f}" if token_data['current_price'] else "N/A"
                atr_pct = f"{token_data['atr_percentage']:.2f}%"
                status = "EXCLUDED"
                
                report.append(f"{rank:<6} {symbol:<8} {pair:<12} {price:<12} {atr_pct:<8} {status:<12}")
            
            if len(excluded_tokens) > 10:
                report.append(f"... and {len(excluded_tokens) - 10} more excluded pairs")
        
        report.extend([
            "",
            "📊 ATR DISTRIBUTION ANALYSIS:",
            f"  • Pairs with ATR > 10%: {len([t for t in self.live_data if t['atr_percentage'] > 10])}",
            f"  • Pairs with ATR 7-10%: {len([t for t in self.live_data if 7 < t['atr_percentage'] <= 10])}",
            f"  • Pairs with ATR 5-7%: {len([t for t in self.live_data if 5 < t['atr_percentage'] <= 7])}",
            f"  • Pairs with ATR < 5%: {len([t for t in self.live_data if t['atr_percentage'] <= 5])}",
            "",
            "🎯 NEXT STEPS:",
            "  • Use qualified pairs for Project Lima grid trading",
            "  • Monitor ATR changes over time",
            "  • Adjust ATR threshold based on market conditions",
            "  • Implement automated monitoring with alerts",
            "",
            "=" * 80
        ])
        
        return "\n".join(report)
    
    def save_results(self, filename: str = None) -> str:
        """Save monitoring results to JSON file"""
        
        if filename is None:
            filename = f"atr_monitoring_results_{self.session_id}.json"
        
        output_data = {
            'timestamp': datetime.now().isoformat(),
            'session_id': self.session_id,
            'criteria': {
                'atr_threshold': self.atr_threshold,
                'atr_period_days': self.atr_period
            },
            'summary': {
                'total_analyzed': len(self.live_data),
                'total_qualified': len(self.qualifying_tokens),
                'qualification_rate': (len(self.qualifying_tokens) / len(self.live_data) * 100) if self.live_data else 0
            },
            'all_analyses': self.live_data,
            'qualifying_tokens': self.qualifying_tokens
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(output_data, f, indent=2)
            
            logger.info(f"📁 Results saved to {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"❌ Error saving results: {e}")
            return ""

def main():
    """Main execution function"""
    
    print("📊 PROJECT LIMA - ATR-BASED CRYPTO MONITOR")
    print("=" * 60)
    print("🎯 Criteria: ATR (10-day) > 7%")
    print("📡 Data Source: CoinGecko OHLC API (VERIFIED LIVE DATA)")
    print("⚠️  GOLDEN RULE: NO SIMULATED DATA ALLOWED")
    print("=" * 60)
    
    # Check for required dependencies
    try:
        import requests
        import pandas as pd
        import numpy as np
    except ImportError as e:
        print(f"❌ Missing required dependency: {e}")
        print("Please install: pip install requests pandas numpy")
        return
    
    # Initialize monitor
    monitor = ATRCryptoMonitor()
    
    try:
        # Monitor all crypto pairs
        qualifying_tokens = monitor.monitor_all_pairs()
        
        # Generate and display report
        report = monitor.generate_report()
        print(report)
        
        # Save results
        filename = monitor.save_results()
        
        print(f"\n✅ ATR monitoring completed successfully!")
        print(f"📊 {len(qualifying_tokens)} crypto pairs qualified")
        if filename:
            print(f"📁 Results saved to: {filename}")
        
    except KeyboardInterrupt:
        print("\n🛑 Monitoring interrupted by user")
    except Exception as e:
        print(f"\n❌ Monitoring failed: {e}")
        logger.error(f"Fatal error: {e}")

if __name__ == "__main__":
    main()
