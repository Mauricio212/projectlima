#!/usr/bin/env python3
"""
PROJECT LIMA - Trading Intelligence Platform
ROI-Focused GRID Bot and Swing Trading Intelligence
"""

import sys
import os
sys.path.insert(0, os.getcwd())

try:
    from flask import Flask, jsonify, request, render_template_string, session
    import json
    from datetime import datetime, timedelta
    import random
    print("✅ All imports successful")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

app = Flask(__name__)
app.secret_key = 'lima_trading_intelligence_2025'  # For session management

# Mock database for user sessions (replace with real database)
users_data = {}

# Trading Intelligence Dashboard
TRADING_DASHBOARD = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project Lima - Trading Intelligence</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
            color: #ffffff;
            min-height: 100vh;
        }
        
        .header {
            background: rgba(26, 26, 46, 0.95);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(0, 255, 157, 0.3);
            padding: 15px 0;
            position: sticky;
            top: 0;
            z-index: 1000;
        }
        
        .nav {
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .logo {
            display: flex;
            align-items: center;
            font-size: 24px;
            font-weight: bold;
            color: #00ff9d;
        }
        
        .nav-menu {
            display: flex;
            gap: 30px;
        }
        
        .nav-item {
            color: #fff;
            text-decoration: none;
            padding: 10px 15px;
            border-radius: 8px;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .nav-item:hover, .nav-item.active {
            background: rgba(0, 255, 157, 0.2);
            color: #00ff9d;
        }
        
        .user-section {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .capital-display {
            background: rgba(0, 255, 157, 0.2);
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 14px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .hero-section {
            text-align: center;
            padding: 40px 0;
            border-bottom: 1px solid rgba(0, 255, 157, 0.1);
            margin-bottom: 30px;
        }
        
        .hero-title {
            font-size: 36px;
            margin-bottom: 15px;
            background: linear-gradient(45deg, #00ff9d, #ffffff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .hero-subtitle {
            font-size: 18px;
            color: #b8b8b8;
            margin-bottom: 30px;
        }
        
        .strategy-tabs {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .strategy-tab {
            background: rgba(26, 26, 46, 0.8);
            border: 1px solid rgba(0, 255, 157, 0.3);
            padding: 15px 30px;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .strategy-tab.active {
            background: linear-gradient(45deg, #00ff9d, #00d4aa);
            color: #000;
            border-color: #00ff9d;
        }
        
        .grid-section {
            display: block;
        }
        
        .stocks-section {
            display: none;
        }
        
        .main-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 30px;
        }
        
        .card {
            background: rgba(26, 26, 46, 0.8);
            border: 1px solid rgba(0, 255, 157, 0.2);
            border-radius: 15px;
            padding: 25px;
            backdrop-filter: blur(10px);
        }
        
        .card-title {
            font-size: 20px;
            color: #00ff9d;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .recommendations-list {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        
        .recommendation-item {
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(0, 255, 157, 0.2);
            border-radius: 10px;
            padding: 20px;
            transition: all 0.3s ease;
        }
        
        .recommendation-item:hover {
            border-color: #00ff9d;
            transform: translateY(-2px);
        }
        
        .crypto-pair {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        
        .pair-name {
            font-size: 18px;
            font-weight: bold;
            color: #00ff9d;
        }
        
        .roi-badge {
            background: linear-gradient(45deg, #00ff9d, #00d4aa);
            color: #000;
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 12px;
            font-weight: bold;
        }
        
        .recommendation-details {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin: 15px 0;
        }
        
        .detail-item {
            font-size: 14px;
            color: #b8b8b8;
        }
        
        .detail-label {
            color: #00ff9d;
            font-weight: bold;
        }
        
        .reasoning {
            background: rgba(0, 255, 157, 0.1);
            padding: 10px;
            border-radius: 8px;
            font-size: 14px;
            line-height: 1.4;
            margin-top: 10px;
        }
        
        .action-button {
            background: linear-gradient(45deg, #00ff9d, #00d4aa);
            color: #000;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            margin-top: 15px;
            transition: all 0.3s ease;
            width: 100%;
        }
        
        .action-button:hover {
            transform: scale(1.02);
            box-shadow: 0 5px 15px rgba(0, 255, 157, 0.3);
        }
        
        .performance-chart {
            height: 300px;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #b8b8b8;
            margin: 20px 0;
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        
        .metric-card {
            background: rgba(26, 26, 46, 0.8);
            border: 1px solid rgba(0, 255, 157, 0.2);
            border-radius: 10px;
            padding: 20px;
            text-align: center;
        }
        
        .metric-value {
            font-size: 28px;
            font-weight: bold;
            color: #00ff9d;
            margin-bottom: 5px;
        }
        
        .metric-label {
            font-size: 12px;
            color: #b8b8b8;
            text-transform: uppercase;
        }
        
        .capital-input {
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(0, 255, 157, 0.3);
            border-radius: 8px;
            padding: 12px;
            color: #fff;
            width: 100%;
            margin: 10px 0;
        }
        
        .capital-input:focus {
            outline: none;
            border-color: #00ff9d;
        }
        
        .allocation-display {
            margin-top: 20px;
            padding: 15px;
            background: rgba(0, 255, 157, 0.1);
            border-radius: 10px;
        }
        
        .coming-soon {
            opacity: 0.6;
            text-align: center;
            padding: 40px;
            color: #b8b8b8;
        }
    </style>
</head>
<body>
    <header class="header">
        <nav class="nav">
            <div class="logo">🚀 Project Lima Trading Intelligence</div>
            <div class="nav-menu">
                <a href="#" class="nav-item active" onclick="showSection('grid')">GRID Bots</a>
                <a href="#" class="nav-item" onclick="showSection('stocks')">Stock Swing</a>
                <a href="#" class="nav-item" onclick="showSection('portfolio')">Portfolio</a>
                <a href="#" class="nav-item" onclick="showSection('analytics')">Analytics</a>
            </div>
            <div class="user-section">
                <div class="capital-display" id="capitalDisplay">Capital: $25,000</div>
                <div class="nav-item" onclick="showCapitalModal()">⚙️ Settings</div>
            </div>
        </nav>
    </header>

    <div class="container">
        <section class="hero-section">
            <h1 class="hero-title">Capital ROI Maximization Platform</h1>
            <p class="hero-subtitle">Actionable GRID Bot & Swing Trading Intelligence</p>
        </section>

        <!-- GRID BOT SECTION -->
        <section id="gridSection" class="grid-section">
            <div class="main-grid">
                <!-- TOP GRID BOT RECOMMENDATIONS -->
                <div class="card">
                    <h2 class="card-title">🤖 Top GRID Bot Opportunities</h2>
                    <div class="recommendations-list" id="gridRecommendations">
                        <!-- Dynamic content loaded here -->
                    </div>
                </div>

                <!-- GRID vs HOLD PERFORMANCE -->
                <div class="card">
                    <h2 class="card-title">📊 GRID vs HOLD Performance (30 Days)</h2>
                    <div class="performance-chart">
                        📈 Interactive Chart Coming Soon
                        <br>GRID: +12.4% | HOLD: +8.7%
                    </div>
                    <div class="metrics-grid">
                        <div class="metric-card">
                            <div class="metric-value">+12.4%</div>
                            <div class="metric-label">GRID ROI</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-value">+8.7%</div>
                            <div class="metric-label">HOLD ROI</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-value">+3.7%</div>
                            <div class="metric-label">GRID Advantage</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- CAPITAL ALLOCATION -->
            <div class="card">
                <h2 class="card-title">💰 Recommended Capital Allocation</h2>
                <div class="main-grid">
                    <div>
                        <label for="workingCapital">Working Capital:</label>
                        <input type="number" id="workingCapital" class="capital-input" value="25000" 
                               onchange="updateAllocation()" placeholder="Enter your trading capital">
                    </div>
                    <div class="allocation-display" id="allocationDisplay">
                        <!-- Dynamic allocation display -->
                    </div>
                </div>
            </div>
        </section>

        <!-- STOCK SWING SECTION -->
        <section id="stocksSection" class="stocks-section">
            <div class="coming-soon">
                <h2>📈 Stock Swing Trading Intelligence</h2>
                <p>Coming Soon - Advanced stock swing trading recommendations and analysis</p>
            </div>
        </section>
    </div>

    <script>
        // Initialize the dashboard
        document.addEventListener('DOMContentLoaded', function() {
            loadGridRecommendations();
            updateAllocation();
            console.log('🚀 Trading Intelligence Dashboard Loaded');
        });

        function showSection(section) {
            // Hide all sections
            document.getElementById('gridSection').style.display = 'none';
            document.getElementById('stocksSection').style.display = 'none';
            
            // Remove active class from all nav items
            document.querySelectorAll('.nav-item').forEach(item => {
                item.classList.remove('active');
            });
            
            // Show selected section
            if (section === 'grid') {
                document.getElementById('gridSection').style.display = 'block';
                loadGridRecommendations();
            } else if (section === 'stocks') {
                document.getElementById('stocksSection').style.display = 'block';
            }
            
            // Add active class to clicked nav item
            event.target.classList.add('active');
        }

        async function loadGridRecommendations() {
            try {
                const response = await fetch('/api/v2/grid-recommendations');
                const data = await response.json();
                
                const container = document.getElementById('gridRecommendations');
                container.innerHTML = '';
                
                data.recommendations.forEach(rec => {
                    const item = createRecommendationItem(rec);
                    container.appendChild(item);
                });
            } catch (error) {
                console.error('Error loading recommendations:', error);
            }
        }

        function createRecommendationItem(rec) {
            const item = document.createElement('div');
            item.className = 'recommendation-item';
            
            item.innerHTML = `
                <div class="crypto-pair">
                    <span class="pair-name">${rec.pair}</span>
                    <span class="roi-badge">${rec.expected_roi}</span>
                </div>
                <div class="recommendation-details">
                    <div class="detail-item">
                        <span class="detail-label">Entry Price:</span> $${rec.entry_price}
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Confidence:</span> ${(rec.confidence * 100).toFixed(0)}%
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Time Frame:</span> ${rec.time_frame}
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Risk Level:</span> ${rec.risk_level}
                    </div>
                </div>
                <div class="reasoning">
                    <strong>Why Trade This:</strong> ${rec.reasoning}
                </div>
                <button class="action-button" onclick="executeGridBot('${rec.pair}')">
                    🤖 Start GRID Bot
                </button>
            `;
            
            return item;
        }

        function updateAllocation() {
            const capital = parseFloat(document.getElementById('workingCapital').value) || 25000;
            
            // Update capital display
            document.getElementById('capitalDisplay').textContent = `Capital: $${capital.toLocaleString()}`;
            
            // Calculate allocations (this would use real recommendations)
            const allocations = calculateOptimalAllocation(capital);
            
            const display = document.getElementById('allocationDisplay');
            display.innerHTML = `
                <h3>Optimal 10-Day Allocation:</h3>
                ${allocations.map(alloc => `
                    <div style="display: flex; justify-content: space-between; margin: 5px 0;">
                        <span>${alloc.pair}</span>
                        <span>$${alloc.amount.toLocaleString()} (${alloc.percentage}%)</span>
                    </div>
                `).join('')}
                <hr style="margin: 10px 0; border-color: rgba(0,255,157,0.3);">
                <div style="display: flex; justify-content: space-between; font-weight: bold;">
                    <span>Expected 10-Day ROI:</span>
                    <span style="color: #00ff9d;">+${allocations.reduce((sum, alloc) => sum + alloc.expectedReturn, 0).toFixed(1)}%</span>
                </div>
            `;
        }

        function calculateOptimalAllocation(capital) {
            // Mock allocation logic (replace with real algorithm)
            return [
                { pair: 'BTC/USDT', amount: capital * 0.4, percentage: 40, expectedReturn: 2.8 },
                { pair: 'ETH/USDT', amount: capital * 0.3, percentage: 30, expectedReturn: 3.2 },
                { pair: 'XRP/USDT', amount: capital * 0.2, percentage: 20, expectedReturn: 4.1 },
                { pair: 'SOL/USDT', amount: capital * 0.1, percentage: 10, expectedReturn: 3.9 }
            ];
        }

        function executeGridBot(pair) {
            alert(`🤖 Starting GRID Bot for ${pair}\\n\\nThis would integrate with your trading platform to automatically deploy the GRID bot with optimized parameters.`);
        }

        function showCapitalModal() {
            const newCapital = prompt('Enter your working capital for trading:', '25000');
            if (newCapital && !isNaN(newCapital)) {
                document.getElementById('workingCapital').value = newCapital;
                updateAllocation();
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def dashboard():
    """Trading Intelligence Dashboard"""
    return TRADING_DASHBOARD

@app.route('/api/v2/grid-recommendations', methods=['GET'])
def grid_recommendations():
    """Get actionable GRID bot recommendations"""
    try:
        # This would connect to your actual GRID vs HOLD analysis engine
        recommendations = [
            {
                "pair": "BTC/USDT",
                "entry_price": "67,234",
                "expected_roi": "+8.5%",
                "confidence": 0.78,
                "time_frame": "7-10 days",
                "risk_level": "Medium",
                "reasoning": "Strong support at $65K with high volatility. Grid range $65K-$72K optimal for 8-12% returns. Volume increased 40% in last 3 days.",
                "grid_settings": {
                    "lower_bound": 65000,
                    "upper_bound": 72000,
                    "grid_count": 20,
                    "investment_per_grid": 0.05
                }
            },
            {
                "pair": "ETH/USDT", 
                "entry_price": "3,765",
                "expected_roi": "+12.3%",
                "confidence": 0.82,
                "time_frame": "5-8 days",
                "risk_level": "Medium-Low",
                "reasoning": "Ethereum showing strong momentum with upcoming upgrade news. Grid strategy outperforming HOLD by 4.2% this month. Low correlation with BTC movements.",
                "grid_settings": {
                    "lower_bound": 3600,
                    "upper_bound": 4200,
                    "grid_count": 15,
                    "investment_per_grid": 0.067
                }
            },
            {
                "pair": "XRP/USDT",
                "entry_price": "3.55", 
                "expected_roi": "+15.7%",
                "confidence": 0.75,
                "time_frame": "3-7 days",
                "risk_level": "Medium-High",
                "reasoning": "Regulatory clarity driving volatility. Perfect for grid trading. 30-day grid performance: +18.2% vs HOLD +7.1%. High profit opportunity.",
                "grid_settings": {
                    "lower_bound": 3.20,
                    "upper_bound": 4.20,
                    "grid_count": 25,
                    "investment_per_grid": 0.04
                }
            }
        ]
        
        return jsonify({
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "recommendations": recommendations,
            "market_conditions": {
                "overall_sentiment": "Bullish",
                "volatility": "High",
                "grid_vs_hold_advantage": "+3.7%"
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/api/v2/grid-vs-hold-performance', methods=['GET'])
def grid_vs_hold_performance():
    """30-day GRID vs HOLD performance comparison"""
    try:
        # Mock historical performance data (replace with real data)
        performance_data = {
            "period": "30_days",
            "grid_performance": {
                "total_return": 12.4,
                "avg_daily_return": 0.41,
                "volatility": 2.8,
                "sharpe_ratio": 1.47,
                "max_drawdown": -4.2,
                "win_rate": 73.3,
                "total_trades": 847,
                "profitable_trades": 621
            },
            "hold_performance": {
                "total_return": 8.7,
                "avg_daily_return": 0.29,
                "volatility": 3.1,
                "sharpe_ratio": 0.94,
                "max_drawdown": -8.7,
                "win_rate": None,
                "total_trades": None,
                "profitable_trades": None
            },
            "comparison": {
                "grid_advantage": 3.7,
                "risk_adjusted_advantage": 1.8,
                "consistency_score": 8.6
            },
            "top_performing_pairs": [
                {"pair": "XRP/USDT", "grid_return": 18.2, "hold_return": 7.1, "advantage": 11.1},
                {"pair": "ETH/USDT", "grid_return": 14.5, "hold_return": 10.3, "advantage": 4.2},
                {"pair": "BTC/USDT", "grid_return": 8.9, "hold_return": 8.2, "advantage": 0.7}
            ]
        }
        
        return jsonify({
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "performance": performance_data
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/api/v2/capital-allocation', methods=['POST'])
def capital_allocation():
    """Calculate optimal capital allocation based on ROI potential"""
    try:
        data = request.json
        working_capital = data.get('working_capital', 25000)
        risk_tolerance = data.get('risk_tolerance', 'medium')
        time_horizon = data.get('time_horizon', 10)  # days
        
        # Mock allocation algorithm (replace with real optimization)
        allocations = [
            {
                "pair": "BTC/USDT",
                "allocation_percentage": 40,
                "allocation_amount": working_capital * 0.4,
                "expected_10day_return": 2.8,
                "confidence": 0.78,
                "risk_score": 6.2
            },
            {
                "pair": "ETH/USDT", 
                "allocation_percentage": 30,
                "allocation_amount": working_capital * 0.3,
                "expected_10day_return": 3.2,
                "confidence": 0.82,
                "risk_score": 5.8
            },
            {
                "pair": "XRP/USDT",
                "allocation_percentage": 20, 
                "allocation_amount": working_capital * 0.2,
                "expected_10day_return": 4.1,
                "confidence": 0.75,
                "risk_score": 7.1
            },
            {
                "pair": "SOL/USDT",
                "allocation_percentage": 10,
                "allocation_amount": working_capital * 0.1, 
                "expected_10day_return": 3.9,
                "confidence": 0.68,
                "risk_score": 7.8
            }
        ]
        
        total_expected_return = sum(alloc['expected_10day_return'] * alloc['allocation_percentage'] / 100 for alloc in allocations)
        
        return jsonify({
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "working_capital": working_capital,
            "allocations": allocations,
            "portfolio_metrics": {
                "total_expected_return": round(total_expected_return, 2),
                "portfolio_risk_score": 6.4,
                "diversification_score": 8.7,
                "liquidity_score": 9.2
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# Keep existing endpoints for compatibility
@app.route('/api/v2/market-data', methods=['GET'])
def market_data():
    """Real-time market data"""
    try:
        data = [
            {"symbol": "BTC", "name": "Bitcoin", "price": 67234, "change_24h": 0.31, "volume": "28.9B"},
            {"symbol": "ETH", "name": "Ethereum", "price": 3765.55, "change_24h": 5.30, "volume": "49.1B"},
            {"symbol": "XRP", "name": "XRP", "price": 3.55, "change_24h": 3.40, "volume": "7.1B"},
            {"symbol": "SOL", "name": "Solana", "price": 182.33, "change_24h": 2.84, "volume": "13.1B"}
        ]
        return jsonify({"status": "success", "data": data, "timestamp": datetime.now().isoformat()})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/api/v2/trading-signals', methods=['GET'])
def trading_signals():
    """Enhanced trading signals with actionable recommendations"""
    try:
        signals = {
            "timestamp": datetime.now().isoformat(),
            "signals": [
                {
                    "symbol": "BTC",
                    "action": "GRID",
                    "confidence": 0.78,
                    "price_target": "$72,000",
                    "current_price": "$67,234",
                    "reasoning": "High volatility with strong support levels ideal for grid trading",
                    "expected_return": "8.5%",
                    "time_frame": "7-10 days"
                },
                {
                    "symbol": "ETH", 
                    "action": "GRID",
                    "confidence": 0.82,
                    "price_target": "$4,200",
                    "current_price": "$3,765",
                    "reasoning": "Strong momentum with upcoming upgrades, grid outperforming HOLD",
                    "expected_return": "12.3%",
                    "time_frame": "5-8 days"
                }
            ],
            "market_sentiment": "Bullish",
            "grid_vs_hold_advantage": "+3.7%"
        }
        return jsonify(signals)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    try:
        print("🚀 Starting Project Lima Trading Intelligence Platform...")
        print("📊 ROI-focused GRID Bot & Swing Trading Intelligence")
        print("💰 Actionable capital allocation recommendations")
        print("📡 Available at: http://0.0.0.0:8000")
        app.run(host='0.0.0.0', port=8000, debug=False, threaded=True)
    except Exception as e:
        print(f"❌ Failed to start web service: {e}")
        sys.exit(1)
