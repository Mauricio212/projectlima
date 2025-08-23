#!/usr/bin/env python3
"""
Grid Bot Trading Framework - Phase 1.5 Automation Script
Implements the proven 3-condition filter system with technical analysis
"""

import requests
import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
import time
import logging
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('grid_bot_automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class GridBotFramework:
    """
    Implements the proven 3-condition filter framework for grid bot trading
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'GridBotFramework/1.0',
            'Accept': 'application/json'
        })
        
        # Framework constants
        self.ATR_MIN = 6.0   # Minimum ATR percentage
        self.ATR_MAX = 18.0  # Maximum ATR percentage
        self.MIN_PROFIT_PER_GRID = 1.0  # Minimum 1% profit per grid
        self.TOP_N_PAIRS = 30  # Top 30 ranking target
        
        # Trading cost analysis (Coinbase Advanced Tier 3)
        self.MAKER_FEE = 0.075   # 0.075% maker fee
        self.TAKER_FEE = 0.150   # 0.150% taker fee
        self.ROUND_TRIP_COST = 0.225  # 0.225% total round-trip cost
        
        logger.info("🚀 Grid Bot Framework initialized")
        logger.info(f"📊 ATR Filter: {self.ATR_MIN}% - {self.ATR_MAX}%")
        logger.info(f"💰 Target: {self.MIN_PROFIT_PER_GRID}% profit per grid minimum")

    def fetch_coinbase_pairs(self) -> List[str]:
        """
        Fetch all USDC trading pairs from Coinbase Advanced
        Implements Condition 2: USDC Base Pairs
        """
        logger.info("🔍 Fetching Coinbase Advanced USDC pairs...")
        
        try:
            url = "https://api.exchange.coinbase.com/products"
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            products = response.json()
            
            # Filter for USDC pairs that are trading
            usdc_pairs = []
            for product in products:
                if (product.get('quote_currency') == 'USDC' and 
                    product.get('status') == 'online' and
                    product.get('trading_disabled') == False):
                    
                    pair_symbol = product['id']  # e.g., "ADA-USDC"
                    base_currency = product['base_currency']  # e.g., "ADA"
                    
                    usdc_pairs.append({
                        'pair': pair_symbol,
                        'base': base_currency,
                        'coinbase_supported': True
                    })
            
            logger.info(f"✅ Found {len(usdc_pairs)} USDC pairs on Coinbase Advanced")
            return usdc_pairs
            
        except Exception as e:
            logger.error(f"❌ Failed to fetch Coinbase pairs: {str(e)}")
            return []

    def calculate_atr(self, symbol: str, days: int = 7) -> Optional[float]:
        """
        Calculate 7-day Average True Range (ATR) percentage for a cryptocurrency
        Implements Condition 1: ATR Filter (6-18%)
        """
        try:
            # Convert symbol format (ADA-USDC -> ada)
            base_symbol = symbol.split('-')[0].lower()
            
            # Get historical data from CoinGecko
            url = f"https://api.coingecko.com/api/v3/coins/{base_symbol}/market_chart"
            params = {
                'vs_currency': 'usd',
                'days': str(days + 2),  # Get extra days for calculation
                'interval': 'daily'
            }
            
            response = self.session.get(url, params=params, timeout=30)
            if response.status_code != 200:
                return None
                
            data = response.json()
            
            if 'prices' not in data or len(data['prices']) < days:
                return None
            
            # Extract price data
            prices = [price[1] for price in data['prices'][-days-1:]]  # Get last N+1 days
            
            if len(prices) < days + 1:
                return None
            
            # Calculate True Range for each day
            true_ranges = []
            for i in range(1, len(prices)):
                high = max(prices[i], prices[i-1])  # Simplified: max of current and previous
                low = min(prices[i], prices[i-1])   # Simplified: min of current and previous
                close_prev = prices[i-1]
                
                tr = max(
                    high - low,
                    abs(high - close_prev),
                    abs(low - close_prev)
                )
                
                if close_prev > 0:
                    tr_percentage = (tr / close_prev) * 100
                    true_ranges.append(tr_percentage)
            
            if not true_ranges:
                return None
            
            # Calculate Average True Range
            atr_percentage = np.mean(true_ranges)
            return round(atr_percentage, 2)
            
        except Exception as e:
            logger.debug(f"ATR calculation failed for {symbol}: {str(e)}")
            return None

    def get_market_data(self, symbol: str) -> Optional[Dict]:
        """
        Get current market data for technical analysis
        """
        try:
            base_symbol = symbol.split('-')[0].lower()
            
            url = f"https://api.coingecko.com/api/v3/simple/price"
            params = {
                'ids': base_symbol,
                'vs_currencies': 'usd',
                'include_market_cap': 'true',
                'include_24hr_vol': 'true',
                'include_24hr_change': 'true'
            }
            
            response = self.session.get(url, params=params, timeout=30)
            if response.status_code != 200:
                return None
                
            data = response.json()
            
            if base_symbol not in data:
                return None
            
            coin_data = data[base_symbol]
            
            return {
                'price': coin_data.get('usd', 0),
                'market_cap': coin_data.get('usd_market_cap', 0),
                'volume_24h': coin_data.get('usd_24h_vol', 0),
                'change_24h': coin_data.get('usd_24h_change', 0)
            }
            
        except Exception as e:
            logger.debug(f"Market data fetch failed for {symbol}: {str(e)}")
            return None

    def analyze_technical_range(self, symbol: str, current_price: float) -> Optional[Dict]:
        """
        Analyze technical trading range using simplified support/resistance
        """
        try:
            # Simplified technical analysis using recent price action
            base_symbol = symbol.split('-')[0].lower()
            
            # Get 30-day historical data for range analysis
            url = f"https://api.coingecko.com/api/v3/coins/{base_symbol}/market_chart"
            params = {
                'vs_currency': 'usd',
                'days': '30',
                'interval': 'daily'
            }
            
            response = self.session.get(url, params=params, timeout=30)
            if response.status_code != 200:
                return None
                
            data = response.json()
            prices = [price[1] for price in data['prices']]
            
            if len(prices) < 20:
                return None
            
            # Simple support/resistance calculation
            recent_prices = prices[-20:]  # Last 20 days
            
            # Support: Lower boundary (20th percentile of recent prices)
            support = np.percentile(recent_prices, 20)
            
            # Resistance: Upper boundary (80th percentile of recent prices)
            resistance = np.percentile(recent_prices, 80)
            
            # Ensure current price is within reasonable range
            if not (support <= current_price <= resistance * 1.1):
                # Adjust range if current price is outside
                price_buffer = current_price * 0.15  # 15% buffer
                support = min(support, current_price - price_buffer)
                resistance = max(resistance, current_price + price_buffer)
            
            # Calculate technical range percentage
            technical_range_pct = ((resistance - support) / support) * 100
            
            return {
                'support': round(support, 4),
                'resistance': round(resistance, 4),
                'current_price': current_price,
                'technical_range_pct': round(technical_range_pct, 2),
                'range_valid': support < current_price < resistance
            }
            
        except Exception as e:
            logger.debug(f"Technical analysis failed for {symbol}: {str(e)}")
            return None

    def calculate_grid_configuration(self, technical_range_pct: float, current_price: float, 
                                   support: float, resistance: float) -> Dict:
        """
        Calculate optimal grid configuration based on technical range
        """
        # Maximum possible grids based on technical range
        max_grids = int(technical_range_pct / self.MIN_PROFIT_PER_GRID)
        
        # Conservative deployment (65% of maximum)
        recommended_grids = int(max_grids * 0.65)
        
        # Ensure minimum viable grid count
        if recommended_grids < 5:
            recommended_grids = min(5, max_grids)
        
        # Calculate grid spacing
        total_range = resistance - support
        if recommended_grids > 1:
            grid_spacing = total_range / (recommended_grids - 1)
            grid_spacing_pct = (grid_spacing / current_price) * 100
        else:
            grid_spacing = total_range
            grid_spacing_pct = technical_range_pct
        
        # Estimate profit per grid
        profit_per_grid = max(grid_spacing_pct, self.MIN_PROFIT_PER_GRID)
        
        # Net profit after fees
        net_profit_per_grid = profit_per_grid - self.ROUND_TRIP_COST
        
        return {
            'max_grids': max_grids,
            'recommended_grids': recommended_grids,
            'grid_spacing': round(grid_spacing, 4),
            'grid_spacing_pct': round(grid_spacing_pct, 2),
            'profit_per_grid': round(profit_per_grid, 2),
            'net_profit_per_grid': round(net_profit_per_grid, 2),
            'viable': net_profit_per_grid > 0.5,  # Minimum 0.5% net profit
            'range_lower': support,
            'range_upper': resistance
        }

    def run_three_condition_filter(self) -> pd.DataFrame:
        """
        Execute the complete 3-condition filter system
        """
        logger.info("🔄 Starting 3-Condition Filter Analysis...")
        
        # Condition 2 & 3: Get Coinbase USDC pairs
        coinbase_pairs = self.fetch_coinbase_pairs()
        
        if not coinbase_pairs:
            logger.error("❌ No Coinbase pairs found. Cannot proceed.")
            return pd.DataFrame()
        
        results = []
        total_pairs = len(coinbase_pairs)
        
        logger.info(f"📊 Analyzing {total_pairs} USDC pairs...")
        
        for i, pair_info in enumerate(coinbase_pairs):
            pair = pair_info['pair']
            base = pair_info['base']
            
            # Progress indicator
            if (i + 1) % 10 == 0 or (i + 1) == total_pairs:
                logger.info(f"⏳ Progress: {i + 1}/{total_pairs} pairs analyzed...")
            
            try:
                # Condition 1: ATR Filter
                atr = self.calculate_atr(pair)
                
                if atr is None:
                    logger.debug(f"⚠️ {pair}: ATR calculation failed")
                    continue
                
                # Check ATR filter
                if not (self.ATR_MIN <= atr <= self.ATR_MAX):
                    logger.debug(f"⚠️ {pair}: ATR {atr}% outside {self.ATR_MIN}-{self.ATR_MAX}% range")
                    continue
                
                # Get market data
                market_data = self.get_market_data(pair)
                if not market_data or market_data['price'] <= 0:
                    logger.debug(f"⚠️ {pair}: Invalid market data")
                    continue
                
                # Technical analysis
                tech_analysis = self.analyze_technical_range(pair, market_data['price'])
                if not tech_analysis:
                    logger.debug(f"⚠️ {pair}: Technical analysis failed")
                    continue
                
                # Grid configuration
                grid_config = self.calculate_grid_configuration(
                    tech_analysis['technical_range_pct'],
                    market_data['price'],
                    tech_analysis['support'],
                    tech_analysis['resistance']
                )
                
                # Only include viable configurations
                if not grid_config['viable']:
                    logger.debug(f"⚠️ {pair}: Grid configuration not viable")
                    continue
                
                # Compile results
                result = {
                    'pair': pair,
                    'base_currency': base,
                    'atr_7d': atr,
                    'current_price': market_data['price'],
                    'market_cap': market_data['market_cap'],
                    'volume_24h': market_data['volume_24h'],
                    'change_24h': market_data['change_24h'],
                    'support_level': tech_analysis['support'],
                    'resistance_level': tech_analysis['resistance'],
                    'technical_range_pct': tech_analysis['technical_range_pct'],
                    'max_grids': grid_config['max_grids'],
                    'recommended_grids': grid_config['recommended_grids'],
                    'grid_spacing_pct': grid_config['grid_spacing_pct'],
                    'profit_per_grid': grid_config['profit_per_grid'],
                    'net_profit_per_grid': grid_config['net_profit_per_grid'],
                    'coinbase_supported': True,
                    'filter_passed': True
                }
                
                results.append(result)
                logger.info(f"✅ {pair}: ATR {atr}%, Range {tech_analysis['technical_range_pct']:.1f}%, "
                          f"Grids {grid_config['recommended_grids']}, Profit {grid_config['net_profit_per_grid']:.2f}%")
                
                # Rate limiting
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"❌ Error analyzing {pair}: {str(e)}")
                continue
        
        if not results:
            logger.warning("⚠️ No pairs passed all three conditions")
            return pd.DataFrame()
        
        # Convert to DataFrame and rank by ATR (highest first)
        df = pd.DataFrame(results)
        df = df.sort_values('atr_7d', ascending=False)
        
        # Limit to Top 30
        top_30 = df.head(self.TOP_N_PAIRS)
        
        logger.info(f"🎯 Analysis Complete: {len(top_30)} pairs passed all conditions")
        logger.info(f"📊 Top 5 pairs by ATR: {', '.join(top_30.head()['pair'].tolist())}")
        
        return top_30

    def generate_summary_report(self, results_df: pd.DataFrame) -> str:
        """
        Generate comprehensive summary report
        """
        if results_df.empty:
            return "❌ No viable pairs found in analysis"
        
        avg_atr = results_df['atr_7d'].mean()
        avg_profit = results_df['net_profit_per_grid'].mean()
        total_grids = results_df['recommended_grids'].sum()
        
        # Find ADA/USDC validation case if present
        ada_case = results_df[results_df['pair'] == 'ADA-USDC']
        ada_validation = ""
        if not ada_case.empty:
            ada_row = ada_case.iloc[0]
            ada_validation = f"""
🔍 ADA/USDC Validation Case:
   ATR: {ada_row['atr_7d']}% ✅ (Framework: 8%)
   Technical Range: {ada_row['technical_range_pct']:.1f}% (Framework: 29.1%)
   Recommended Grids: {ada_row['recommended_grids']} (Framework: 17 deployed)
   Net Profit/Grid: {ada_row['net_profit_per_grid']:.2f}% (Framework: 1.61% actual)
"""
        
        report = f"""
═══════════════════════════════════════════════════════════════
🎯 GRID BOT FRAMEWORK - PHASE 1.5 AUTOMATION RESULTS
═══════════════════════════════════════════════════════════════

📊 EXECUTIVE SUMMARY:
   ✅ Pairs Analyzed: {len(results_df)} passed all 3 conditions
   📈 Average ATR: {avg_atr:.2f}% (Target: 6-18%)
   💰 Average Net Profit/Grid: {avg_profit:.2f}%
   🎛️ Total Recommended Grids: {total_grids}
   �� All pairs Coinbase Advanced supported ✅

📋 3-CONDITION FILTER RESULTS:
   ✅ Condition 1 (ATR 6-18%): {len(results_df)} pairs qualified
   ✅ Condition 2 (USDC Base): All pairs USDC-based ✅  
   ✅ Condition 3 (Coinbase): All pairs supported ✅

🥇 TOP 5 OPPORTUNITIES:
"""
        
        for i, (_, row) in enumerate(results_df.head().iterrows()):
            report += f"""   {i+1}. {row['pair']}: ATR {row['atr_7d']}%, {row['recommended_grids']} grids, {row['net_profit_per_grid']:.2f}% profit/grid\n"""
        
        report += ada_validation
        
        report += f"""
🔧 FRAMEWORK VALIDATION:
   ✅ Mathematical Approach: Technical Range ÷ 1% = Grid Count
   ✅ Conservative Deployment: 65% of maximum grids
   ✅ Cost Analysis: 0.225% fees factored in
   ✅ Profitability Filter: Minimum 0.5% net profit/grid

📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
═══════════════════════════════════════════════════════════════
"""
        
        return report

    def export_results(self, results_df: pd.DataFrame, summary_report: str):
        """
        Export results to CSV and generate summary files
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Export main results
        csv_filename = f"grid_bot_top30_{timestamp}.csv"
        results_df.to_csv(csv_filename, index=False)
        logger.info(f"📄 Results exported: {csv_filename}")
        
        # Export summary report
        report_filename = f"grid_bot_summary_{timestamp}.txt"
        with open(report_filename, 'w') as f:
            f.write(summary_report)
        logger.info(f"📋 Summary report: {report_filename}")
        
        # Export grid configuration for TreeCommAS deployment
        if not results_df.empty:
            deployment_df = results_df[['pair', 'current_price', 'support_level', 
                                     'resistance_level', 'recommended_grids', 
                                     'grid_spacing_pct', 'net_profit_per_grid']].copy()
            
            deployment_filename = f"grid_deployment_config_{timestamp}.csv"
            deployment_df.to_csv(deployment_filename, index=False)
            logger.info(f"🎛️ Deployment config: {deployment_filename}")

def main():
    """
    Main execution function - implements complete Phase 1.5 automation
    """
    print("🚀 Grid Bot Framework - Phase 1.5 Automation")
    print("🎯 Implementing proven 3-condition filter system\n")
    
    # Initialize framework
    framework = GridBotFramework()
    
    # Run complete analysis
    logger.info("🔄 Starting complete framework analysis...")
    start_time = time.time()
    
    # Execute 3-condition filter
    results = framework.run_three_condition_filter()
    
    # Generate summary
    summary = framework.generate_summary_report(results)
    
    # Export results
    framework.export_results(results, summary)
    
    # Display results
    print(summary)
    
    execution_time = time.time() - start_time
    logger.info(f"⏱️ Total execution time: {execution_time:.2f} seconds")
    logger.info("✅ Phase 1.5 automation complete!")

if __name__ == "__main__":
    main()
