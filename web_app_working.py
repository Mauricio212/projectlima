#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.getcwd())

try:
    from flask import Flask, jsonify, request
    import json
    from datetime import datetime
    print("✅ All imports successful")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

app = Flask(__name__)

@app.route('/')
def dashboard():
    return '''
    <h1>🚀 Project Lima - Cryptocurrency Intelligence Platform</h1>
    <h3>📡 Available Endpoints:</h3>
    <ul>
        <li><a href="/api/v2/market-data">GET /api/v2/market-data</a> - Market data</li>
        <li><a href="/api/v2/trading-signals">GET /api/v2/trading-signals</a> - Trading signals</li>
        <li><a href="/api/v2/market-summary">GET /api/v2/market-summary</a> - Market summary</li>
        <li><a href="/ws/live-data">GET /ws/live-data</a> - Live data</li>
    </ul>
    '''

@app.route('/api/v2/market-data', methods=['GET'])
def market_data():
    try:
        data = [
            {"symbol": "BTC", "name": "Bitcoin", "price": 118443, "change_24h": 0.31},
            {"symbol": "ETH", "name": "Ethereum", "price": 3765.55, "change_24h": 5.30},
            {"symbol": "XRP", "name": "XRP", "price": 3.55, "change_24h": 3.40},
            {"symbol": "SOL", "name": "Solana", "price": 182.33, "change_24h": 2.84}
        ]
        return jsonify({"status": "success", "data": data, "timestamp": datetime.now().isoformat()})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/api/v2/trading-signals', methods=['GET'])
def trading_signals():
    try:
        signals = {
            "timestamp": datetime.now().isoformat(),
            "signals": [
                {"symbol": "BTC", "action": "GRID", "confidence": 0.78, "price_target": "$125,000"},
                {"symbol": "ETH", "action": "HOLD", "confidence": 0.82, "price_target": "$4,200"}
            ],
            "market_sentiment": "Cautiously Optimistic"
        }
        return jsonify(signals)
    except Exception as e:
        return jsonify({"error": str(e)})

# THE MISSING ENDPOINTS - CORRECTLY PLACED BEFORE app.run()
@app.route('/api/v2/market-summary', methods=['GET'])  
def market_summary():
    try:
        return jsonify({
            "total_market_cap": "3.1T",
            "total_volume_24h": "138.2B",
            "btc_dominance": "56.2%", 
            "market_sentiment": "Cautiously Optimistic",
            "last_updated": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/ws/live-data', methods=['GET'])
def ws_live_data():
    try:
        return jsonify({
            "type": "live_update",
            "timestamp": datetime.now().isoformat(),
            "prices": {"BTC": 118443, "ETH": 3765.55, "XRP": 3.55},
            "status": "live"
        })
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    try:
        print("🚀 Starting Project Lima Web Service...")
        print("📡 Available at: http://0.0.0.0:8000")
        app.run(host='0.0.0.0', port=8000, debug=False, threaded=True)
    except Exception as e:
        print(f"❌ Failed to start web service: {e}")
        sys.exit(1)
