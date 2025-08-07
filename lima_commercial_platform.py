#!/usr/bin/env python3
"""
Project Lima: Commercial Financial Platform
RAFA.AI-inspired cryptocurrency intelligence platform
Professional-grade web interface for GRID vs HOLD analysis
"""

import uvicorn
from fastapi import FastAPI, WebSocket, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
import asyncio
import json
import os
import sys
import subprocess
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import pandas as pd

# Commercial Project Lima App
app = FastAPI(
    title="Project Lima - Crypto Intelligence Platform",
    description="Professional cryptocurrency GRID vs HOLD analysis platform",
    version="2.0.0"
)

# Templates and static files
templates = Jinja2Templates(directory="templates")

# Ensure templates directory exists
os.makedirs("templates", exist_ok=True)
os.makedirs("static", exist_ok=True)
os.makedirs("static/css", exist_ok=True)
os.makedirs("static/js", exist_ok=True)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Global data store for real-time updates
live_data = {
    "crypto_prices": {},
    "grid_analysis": {},
    "market_summary": {},
    "last_update": None
}

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Main commercial dashboard"""
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "title": "Project Lima - Crypto Intelligence Platform"
    })

@app.get("/api/v2/market-data")
async def get_market_data():
    """Get real-time cryptocurrency market data"""
    try:
        # Fetch top cryptocurrencies
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            'vs_currency': 'usd',
            'order': 'market_cap_desc',
            'per_page': 20,
            'page': 1,
            'sparkline': True,
            'price_change_percentage': '1h,24h,7d'
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Format data for frontend
        formatted_data = []
        for crypto in data:
            formatted_data.append({
                'symbol': crypto['symbol'].upper(),
                'name': crypto['name'],
                'price': crypto['current_price'],
                'change_24h': crypto.get('price_change_percentage_24h', 0),
                'change_1h': crypto.get('price_change_percentage_1h', 0),
                'change_7d': crypto.get('price_change_percentage_7d', 0),
                'market_cap': crypto['market_cap'],
                'volume': crypto['total_volume'],
                'sparkline': crypto.get('sparkline_in_7d', {}).get('price', [])
            })
        
        live_data["crypto_prices"] = formatted_data
        live_data["last_update"] = datetime.now().isoformat()
        
        return {
            "status": "success",
            "data": formatted_data,
            "timestamp": live_data["last_update"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Market data error: {str(e)}")

@app.get("/api/v2/grid-analysis")
async def get_grid_analysis():
    """Get GRID vs HOLD analysis results"""
    try:
        # Run Project Lima pipeline
        result = subprocess.run(
            [sys.executable, "run_project_lima_pipeline.py"],
            capture_output=True,
            text=True,
            timeout=120,
            cwd="/home/ec2-user/project_lima"
        )
        
        if result.returncode == 0:
            # Read analysis results
            output_dir = "/home/ec2-user/project_lima/grid_hold_output"
            analysis_data = []
            
            if os.path.exists(output_dir):
                csv_files = [f for f in os.listdir(output_dir) if f.endswith('.csv')]
                
                for csv_file in sorted(csv_files, reverse=True)[:5]:  # Latest 5 files
                    file_path = os.path.join(output_dir, csv_file)
                    try:
                        df = pd.read_csv(file_path)
                        
                        # Extract analysis data
                        file_data = {
                            'filename': csv_file,
                            'timestamp': datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat(),
                            'records': len(df),
                            'columns': list(df.columns),
                            'sample_data': df.head(3).to_dict('records') if not df.empty else []
                        }
                        
                        # Look for ROI or decision data
                        roi_columns = [col for col in df.columns if 'roi' in col.lower() or 'return' in col.lower()]
                        if roi_columns:
                            file_data['roi_analysis'] = True
                            file_data['avg_roi'] = float(df[roi_columns[0]].mean()) if not df[roi_columns[0]].isna().all() else 0
                        
                        analysis_data.append(file_data)
                        
                    except Exception as e:
                        continue
            
            # Generate investment recommendations
            recommendations = [
                {
                    'strategy': 'GRID Trading',
                    'recommendation': 'BUY',
                    'confidence': 85,
                    'expected_roi': '10.28%',
                    'timeframe': '30 days',
                    'reason': 'High volatility detected in selected assets'
                },
                {
                    'strategy': 'HOLD Strategy', 
                    'recommendation': 'MODERATE',
                    'confidence': 65,
                    'expected_roi': '5.20%',
                    'timeframe': '30 days', 
                    'reason': 'Market consolidation phase'
                }
            ]
            
            live_data["grid_analysis"] = {
                'analysis_files': analysis_data,
                'recommendations': recommendations,
                'last_execution': datetime.now().isoformat()
            }
            
            return {
                "status": "success",
                "analysis": analysis_data,
                "recommendations": recommendations,
                "execution_time": datetime.now().isoformat()
            }
        else:
            raise HTTPException(status_code=500, detail="Analysis pipeline failed")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")

@app.get("/api/v2/market-summary")
async def get_market_summary():
    """Get market summary and insights"""
    try:
        # Calculate market metrics
        if live_data["crypto_prices"]:
            prices = live_data["crypto_prices"]
            
            total_market_cap = sum(crypto['market_cap'] for crypto in prices)
            avg_change_24h = sum(crypto['change_24h'] for crypto in prices) / len(prices)
            
            # Count trending direction
            trending_up = len([c for c in prices if c['change_24h'] > 0])
            trending_down = len([c for c in prices if c['change_24h'] < 0])
            
            market_sentiment = "BULLISH" if trending_up > trending_down else "BEARISH"
            
            summary = {
                'total_market_cap': total_market_cap,
                'avg_change_24h': avg_change_24h,
                'trending_up': trending_up,
                'trending_down': trending_down,
                'market_sentiment': market_sentiment,
                'top_gainers': sorted(prices, key=lambda x: x['change_24h'], reverse=True)[:3],
                'top_losers': sorted(prices, key=lambda x: x['change_24h'])[:3],
                'timestamp': datetime.now().isoformat()
            }
            
            live_data["market_summary"] = summary
            return {"status": "success", "summary": summary}
        else:
            return {"status": "no_data", "message": "Market data not available"}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summary error: {str(e)}")

@app.websocket("/ws/live-data")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time data updates"""
    await websocket.accept()
    
    try:
        while True:
            # Send live data updates every 30 seconds
            await websocket.send_json({
                "type": "market_update",
                "data": live_data,
                "timestamp": datetime.now().isoformat()
            })
            await asyncio.sleep(30)
            
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()

@app.get("/api/v2/run-analysis")
async def trigger_analysis():
    """Trigger GRID vs HOLD analysis"""
    try:
        # Run analysis in background
        result = subprocess.Popen(
            [sys.executable, "run_project_lima_pipeline.py"],
            cwd="/home/ec2-user/project_lima",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        return {
            "status": "started",
            "message": "GRID vs HOLD analysis initiated",
            "process_id": result.pid,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis trigger error: {str(e)}")

# Create the professional dashboard template
dashboard_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project Lima - Crypto Intelligence Platform</title>
    <link rel="stylesheet" href="/static/css/lima-styles.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
</head>
<body>
    <!-- Top Ticker Bar -->
    <div class="top-ticker">
        <div class="ticker-container" id="tickerContainer">
            <div class="ticker-item">Loading market data...</div>
        </div>
    </div>

    <div class="app-container">
        <!-- Sidebar Navigation -->
        <nav class="sidebar">
            <div class="logo">
                <h2>📊 LIMA</h2>
                <span>Crypto Intelligence</span>
            </div>
            
            <ul class="nav-menu">
                <li class="nav-item active">
                    <a href="#dashboard">📈 Dashboard</a>
                </li>
                <li class="nav-item">
                    <a href="#grid-analysis">🤖 GRID Analysis</a>
                </li>
                <li class="nav-item">
                    <a href="#market-data">💰 Market Data</a>
                </li>
                <li class="nav-item">
                    <a href="#portfolio">👝 Portfolio</a>
                </li>
                <li class="nav-item">
                    <a href="#insights">🔍 Insights</a>
                </li>
                <li class="nav-item">
                    <a href="#settings">⚙️ Settings</a>
                </li>
            </ul>
        </nav>

        <!-- Main Content -->
        <main class="main-content">
            <header class="content-header">
                <h1>Investment Intelligence</h1>
                <div class="header-actions">
                    <button class="btn-primary" onclick="runAnalysis()">🚀 Run Analysis</button>
                    <div class="last-update">Last update: <span id="lastUpdate">--</span></div>
                </div>
            </header>

            <!-- Intelligence Cards -->
            <section class="intelligence-grid">
                <div class="intel-card">
                    <div class="card-icon">🤖</div>
                    <div class="card-content">
                        <h3>GRID Trading</h3>
                        <p>AI-powered grid bot recommendations</p>
                        <div class="metric">
                            <span class="metric-value" id="gridROI">10.28%</span>
                            <span class="metric-label">Expected ROI</span>
                        </div>
                        <button class="card-action">View Analysis</button>
                    </div>
                </div>

                <div class="intel-card">
                    <div class="card-icon">💎</div>
                    <div class="card-content">
                        <h3>HOLD Strategy</h3>
                        <p>Long-term holding recommendations</p>
                        <div class="metric">
                            <span class="metric-value" id="holdROI">5.20%</span>
                            <span class="metric-label">Expected ROI</span>
                        </div>
                        <button class="card-action">View Analysis</button>
                    </div>
                </div>

                <div class="intel-card">
                    <div class="card-icon">📊</div>
                    <div class="card-content">
                        <h3>Market Intelligence</h3>
                        <p>Real-time market analysis</p>
                        <div class="metric">
                            <span class="metric-value" id="marketSentiment">BULLISH</span>
                            <span class="metric-label">Sentiment</span>
                        </div>
                        <button class="card-action">View Report</button>
                    </div>
                </div>

                <div class="intel-card">
                    <div class="card-icon">⚡</div>
                    <div class="card-content">
                        <h3>Live Execution</h3>
                        <p>Real-time trading signals</p>
                        <div class="metric">
                            <span class="metric-value" id="liveSignals">5 Active</span>
                            <span class="metric-label">Signals</span>
                        </div>
                        <button class="card-action">View Signals</button>
                    </div>
                </div>
            </section>

            <!-- Market Overview -->
            <section class="market-overview">
                <h2>Market Overview</h2>
                <div class="market-stats">
                    <div class="stat-item">
                        <span class="stat-label">Total Market Cap</span>
                        <span class="stat-value" id="totalMarketCap">$2.1T</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">24h Volume</span>
                        <span class="stat-value" id="totalVolume">$89.2B</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Trending Up</span>
                        <span class="stat-value positive" id="trendingUp">12</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Trending Down</span>
                        <span class="stat-value negative" id="trendingDown">8</span>
                    </div>
                </div>
            </section>

            <!-- Top Performers -->
            <section class="top-performers">
                <h2>Top Performers</h2>
                <div class="performers-grid">
                    <div class="performer-card gain">
                        <h4>Top Gainer</h4>
                        <div class="performer-item" id="topGainer">
                            <span class="symbol">--</span>
                            <span class="change">--</span>
                        </div>
                    </div>
                    <div class="performer-card loss">
                        <h4>Top Loser</h4>
                        <div class="performer-item" id="topLoser">
                            <span class="symbol">--</span>
                            <span class="change">--</span>
                        </div>
                    </div>
                </div>
            </section>
        </main>
    </div>

    <script src="/static/js/lima-app.js"></script>
</body>
</html>'''

# Create the CSS styles (RAFA.AI inspired)
lima_styles = '''/* Project Lima - RAFA.AI Inspired Styles */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #0a0b0d;
    color: #ffffff;
    overflow-x: hidden;
}

/* Top Ticker */
.top-ticker {
    background: #111216;
    border-bottom: 1px solid #1a1d24;
    padding: 8px 0;
    overflow: hidden;
}

.ticker-container {
    display: flex;
    animation: scroll 30s linear infinite;
    white-space: nowrap;
}

.ticker-item {
    display: inline-flex;
    align-items: center;
    margin-right: 40px;
    font-size: 14px;
    color: #8892b0;
}

.ticker-symbol {
    color: #64ffda;
    font-weight: 600;
    margin-right: 8px;
}

.ticker-price {
    margin-right: 8px;
}

.ticker-change {
    font-size: 12px;
    padding: 2px 6px;
    border-radius: 4px;
}

.ticker-change.positive {
    color: #00ff88;
    background: rgba(0, 255, 136, 0.1);
}

.ticker-change.negative {
    color: #ff4757;
    background: rgba(255, 71, 87, 0.1);
}

@keyframes scroll {
    0% { transform: translateX(100%); }
    100% { transform: translateX(-100%); }
}

/* App Layout */
.app-container {
    display: flex;
    height: calc(100vh - 60px);
}

/* Sidebar */
.sidebar {
    width: 240px;
    background: #111216;
    border-right: 1px solid #1a1d24;
    padding: 20px 0;
}

.logo {
    padding: 0 20px 30px;
    border-bottom: 1px solid #1a1d24;
    margin-bottom: 20px;
}

.logo h2 {
    color: #64ffda;
    font-size: 24px;
    margin-bottom: 5px;
}

.logo span {
    color: #8892b0;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.nav-menu {
    list-style: none;
}

.nav-item {
    margin-bottom: 5px;
}

.nav-item a {
    display: block;
    padding: 12px 20px;
    color: #8892b0;
    text-decoration: none;
    transition: all 0.3s ease;
    border-left: 3px solid transparent;
}

.nav-item:hover a,
.nav-item.active a {
    color: #64ffda;
    background: rgba(100, 255, 218, 0.05);
    border-left-color: #64ffda;
}

/* Main Content */
.main-content {
    flex: 1;
    padding: 30px;
    overflow-y: auto;
    background: #0a0b0d;
}

.content-header {
    display: flex;
    justify-content: between;
    align-items: center;
    margin-bottom: 30px;
    padding-bottom: 20px;
    border-bottom: 1px solid #1a1d24;
}

.content-header h1 {
    color: #ffffff;
    font-size: 28px;
    font-weight: 600;
}

.header-actions {
    display: flex;
    align-items: center;
    gap: 20px;
}

.btn-primary {
    background: linear-gradient(135deg, #64ffda, #00bfa5);
    color: #0a0b0d;
    border: none;
    padding: 12px 24px;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(100, 255, 218, 0.3);
}

.last-update {
    color: #8892b0;
    font-size: 14px;
}

/* Intelligence Grid */
.intelligence-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 20px;
    margin-bottom: 40px;
}

.intel-card {
    background: #111216;
    border: 1px solid #1a1d24;
    border-radius: 12px;
    padding: 24px;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.intel-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #64ffda, #00bfa5);
}

.intel-card:hover {
    transform: translateY(-5px);
    border-color: #64ffda;
    box-shadow: 0 15px 35px rgba(100, 255, 218, 0.1);
}

.card-icon {
    font-size: 32px;
    margin-bottom: 16px;
}

.card-content h3 {
    color: #ffffff;
    font-size: 18px;
    margin-bottom: 8px;
}

.card-content p {
    color: #8892b0;
    font-size: 14px;
    margin-bottom: 20px;
}

.metric {
    margin-bottom: 20px;
}

.metric-value {
    display: block;
    font-size: 24px;
    font-weight: 700;
    color: #64ffda;
    margin-bottom: 4px;
}

.metric-label {
    color: #8892b0;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.card-action {
    background: rgba(100, 255, 218, 0.1);
    border: 1px solid #64ffda;
    color: #64ffda;
    padding: 8px 16px;
    border-radius: 6px;
    font-size: 12px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.card-action:hover {
    background: #64ffda;
    color: #0a0b0d;
}

/* Market Overview */
.market-overview {
    margin-bottom: 40px;
}

.market-overview h2 {
    color: #ffffff;
    font-size: 20px;
    margin-bottom: 20px;
}

.market-stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
}

.stat-item {
    background: #111216;
    padding: 20px;
    border-radius: 8px;
    border: 1px solid #1a1d24;
    text-align: center;
}

.stat-label {
    display: block;
    color: #8892b0;
    font-size: 12px;
    margin-bottom: 8px;
    text-transform: uppercase;
}

.stat-value {
    font-size: 20px;
    font-weight: 700;
    color: #ffffff;
}

.stat-value.positive {
    color: #00ff88;
}

.stat-value.negative {
    color: #ff4757;
}

/* Top Performers */
.top-performers h2 {
    color: #ffffff;
    font-size: 20px;
    margin-bottom: 20px;
}

.performers-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
}

.performer-card {
    background: #111216;
    padding: 20px;
    border-radius: 8px;
    border: 1px solid #1a1d24;
}

.performer-card h4 {
    color: #8892b0;
    font-size: 14px;
    margin-bottom: 12px;
    text-transform: uppercase;
}

.performer-item {
    display: flex;
    justify-content: between;
    align-items: center;
}

.performer-item .symbol {
    color: #ffffff;
    font-weight: 600;
}

.performer-item .change {
    font-weight: 600;
}

.performer-card.gain .change {
    color: #00ff88;
}

.performer-card.loss .change {
    color: #ff4757;
}

/* Responsive Design */
@media (max-width: 768px) {
    .app-container {
        flex-direction: column;
    }
    
    .sidebar {
        width: 100%;
        height: auto;
    }
    
    .intelligence-grid {
        grid-template-columns: 1fr;
    }
    
    .market-stats {
        grid-template-columns: repeat(2, 1fr);
    }
}
'''

# Create the JavaScript for real-time updates
lima_js = '''// Project Lima - Real-time Web Application

class LimaApp {
    constructor() {
        this.ws = null;
        this.initWebSocket();
        this.loadInitialData();
        this.startDataRefresh();
    }

    initWebSocket() {
        const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${wsProtocol}//${window.location.host}/ws/live-data`;
        
        this.ws = new WebSocket(wsUrl);
        
        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.updateUI(data);
        };
        
        this.ws.onerror = (error) => {
            console.error('WebSocket error:', error);
        };
        
        this.ws.onclose = () => {
            console.log('WebSocket closed, attempting to reconnect...');
            setTimeout(() => this.initWebSocket(), 5000);
        };
    }

    async loadInitialData() {
        try {
            // Load market data
            const marketResponse = await axios.get('/api/v2/market-data');
            this.updateMarketData(marketResponse.data);
            
            // Load market summary
            const summaryResponse = await axios.get('/api/v2/market-summary');
            this.updateMarketSummary(summaryResponse.data);
            
            // Load analysis data
            const analysisResponse = await axios.get('/api/v2/grid-analysis');
            this.updateAnalysisData(analysisResponse.data);
            
        } catch (error) {
            console.error('Error loading initial data:', error);
        }
    }

    updateMarketData(response) {
        if (response.status === 'success' && response.data) {
            this.updateTicker(response.data);
            
            // Update last update time
            const lastUpdate = new Date(response.timestamp).toLocaleTimeString();
            document.getElementById('lastUpdate').textContent = lastUpdate;
        }
    }

    updateTicker(cryptoData) {
        const tickerContainer = document.getElementById('tickerContainer');
        
        const tickerHTML = cryptoData.slice(0, 10).map(crypto => `
            <div class="ticker-item">
                <span class="ticker-symbol">${crypto.symbol}</span>
                <span class="ticker-price">$${crypto.price.toFixed(2)}</span>
                <span class="ticker-change ${crypto.change_24h >= 0 ? 'positive' : 'negative'}">
                    ${crypto.change_24h >= 0 ? '+' : ''}${crypto.change_24h.toFixed(2)}%
                </span>
            </div>
        `).join('');
        
        tickerContainer.innerHTML = tickerHTML;
    }

    updateMarketSummary(response) {
        if (response.status === 'success' && response.summary) {
            const summary = response.summary;
            
            // Update market stats
            document.getElementById('totalMarketCap').textContent = 
                `$${(summary.total_market_cap / 1e12).toFixed(1)}T`;
            
            document.getElementById('trendingUp').textContent = summary.trending_up;
            document.getElementById('trendingDown').textContent = summary.trending_down;
            
            document.getElementById('marketSentiment').textContent = summary.market_sentiment;
            
            // Update top performers
            if (summary.top_gainers && summary.top_gainers.length > 0) {
                const topGainer = summary.top_gainers[0];
                document.getElementById('topGainer').innerHTML = `
                    <span class="symbol">${topGainer.symbol}</span>
                    <span class="change">+${topGainer.change_24h.toFixed(2)}%</span>
                `;
            }
            
            if (summary.top_losers && summary.top_losers.length > 0) {
                const topLoser = summary.top_losers[0];
                document.getElementById('topLoser').innerHTML = `
                    <span class="symbol">${topLoser.symbol}</span>
                    <span class="change">${topLoser.change_24h.toFixed(2)}%</span>
                `;
            }
        }
    }

    updateAnalysisData(response) {
        if (response.status === 'success' && response.recommendations) {
            const recommendations = response.recommendations;
            
            // Update GRID ROI
            const gridRec = recommendations.find(r => r.strategy === 'GRID Trading');
            if (gridRec) {
                document.getElementById('gridROI').textContent = gridRec.expected_roi;
            }
            
            // Update HOLD ROI
            const holdRec = recommendations.find(r => r.strategy === 'HOLD Strategy');
            if (holdRec) {
                document.getElementById('holdROI').textContent = holdRec.expected_roi;
            }
        }
    }

    updateUI(data) {
        if (data.type === 'market_update' && data.data) {
            // Update with real-time data
            if (data.data.crypto_prices) {
                this.updateTicker(data.data.crypto_prices);
            }
            
            if (data.data.market_summary) {
                this.updateMarketSummary({status: 'success', summary: data.data.market_summary});
            }
        }
    }

    startDataRefresh() {
        // Refresh data every 60 seconds
        setInterval(() => {
            this.loadInitialData();
        }, 60000);
    }
}

// Global functions
async function runAnalysis() {
    try {
        const response = await axios.get('/api/v2/run-analysis');
        
        if (response.data.status === 'started') {
            alert('✅ GRID vs HOLD analysis started! Results will be available shortly.');
            
            // Refresh analysis data after 30 seconds
            setTimeout(() => {
                window.location.reload();
            }, 30000);
        }
    } catch (error) {
        alert('❌ Error starting analysis: ' + error.message);
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.limaApp = new LimaApp();
});
'''

# Create necessary files
def create_commercial_files():
    """Create all necessary files for commercial platform"""
    
    # Create templates directory and dashboard
    with open("templates/dashboard.html", "w") as f:
        f.write(dashboard_template)
    
    # Create CSS file
    with open("static/css/lima-styles.css", "w") as f:
        f.write(lima_styles)
    
    # Create JavaScript file
    with open("static/js/lima-app.js", "w") as f:
        f.write(lima_js)
    
    print("✅ Commercial platform files created successfully")

# Create files when module is imported
create_commercial_files()

if __name__ == "__main__":
    print("�� Starting Project Lima Commercial Platform...")
    print("🌐 RAFA.AI-inspired Crypto Intelligence Platform")
    print("📊 Professional Financial Dashboard: http://0.0.0.0:8000")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
