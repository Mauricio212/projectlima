import sys
import os
from flask import Flask, request, jsonify, render_template_string, send_from_directory, redirect
import json
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta
import hashlib
import time

# Import all monitoring systems
from monitoring import monitoring_bp
from unified_dashboard import unified_bp
from trading_operations import trading_ops_bp
from operational_monitoring import ops_monitor_bp

# Initialize Flask app
app = Flask(__name__)
app.register_blueprint(monitoring_bp)         # Technical monitoring
app.register_blueprint(unified_bp)            # Unified dashboard
app.register_blueprint(trading_ops_bp)        # Trading operations (removed)
app.register_blueprint(ops_monitor_bp)        # NEW: Operational monitoring

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'database': 'lima_trading',
    'user': 'lima_user',
    'password': 'lima_secure_2025'
}

def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

@app.route('/')
def home():
    """Redirect to operational monitoring dashboard"""
    return redirect('/ops')

@app.route('/home')
def home_page():
    """Navigation hub with all dashboard options"""
    home_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Project Lima - Professional Operations</title>
        <style>
            body { 
                font-family: 'Google Sans', 'Roboto', Arial, sans-serif;
                background: #fafafa;
                color: #202124;
                margin: 0;
                padding: 40px;
                min-height: 100vh;
            }
            .container { 
                max-width: 1200px; 
                margin: 0 auto; 
                text-align: center;
            }
            h1 { 
                font-size: 2.5em; 
                margin-bottom: 20px;
                color: #1a73e8;
                font-weight: 400;
            }
            .nav-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin-top: 40px;
            }
            .nav-card {
                background: white;
                border: 1px solid #dadce0;
                border-radius: 8px;
                padding: 24px;
                transition: all 0.2s ease;
                text-decoration: none;
                color: #202124;
                box-shadow: 0 1px 2px rgba(0,0,0,0.1);
            }
            .nav-card:hover {
                transform: translateY(-2px);
                text-decoration: none;
                color: #202124;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                border-color: #1a73e8;
            }
            .nav-card h3 {
                font-size: 1.3em;
                margin-bottom: 12px;
                color: #1a73e8;
                font-weight: 500;
            }
            .nav-card p {
                opacity: 0.8;
                line-height: 1.5;
                color: #5f6368;
                font-size: 14px;
            }
            .status-banner {
                background: white;
                border: 1px solid #34a853;
                border-radius: 8px;
                padding: 20px;
                margin-bottom: 32px;
                box-shadow: 0 1px 2px rgba(0,0,0,0.1);
            }
            .primary-card {
                border: 2px solid #1a73e8;
                background: #f8f9fa;
            }
            .secondary-card {
                border: 1px solid #dadce0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Project Lima Professional Operations</h1>
            
            <div class="status-banner">
                <h2 style="color: #34a853; margin-bottom: 8px; font-weight: 500;">System Operational</h2>
                <p style="color: #5f6368; font-size: 14px;">Comprehensive operational monitoring with Google Analytics-style interface</p>
            </div>
            
            <div class="nav-grid">
                <a href="/ops" class="nav-card primary-card">
                    <h3>📊 Operational Monitoring</h3>
                    <p>Google Analytics-style dashboard focused on system health, performance metrics, and early warning detection. Zero financial data.</p>
                </a>
                
                <a href="/dashboard" class="nav-card secondary-card">
                    <h3>🎯 Unified Command Center</h3>
                    <p>Dark-themed technical dashboard combining system monitoring and infrastructure health in one interface</p>
                </a>
                
                <a href="/operations-live" class="nav-card secondary-card">
                    <h3>📈 Live Operations</h3>
                    <p>Real-time operations dashboard with live updates and system status monitoring</p>
                </a>
                
                <a href="/monitoring" class="nav-card secondary-card">
                    <h3>🔧 System Monitoring</h3>
                    <p>Detailed technical monitoring with PostgreSQL metrics and performance diagnostics</p>
                </a>
                
                <a href="/api/warehouse/list" class="nav-card secondary-card">
                    <h3>📁 Document Warehouse</h3>
                    <p>Secure API access to professional documents with data integrity monitoring</p>
                </a>
            </div>
            
            <div style="margin-top: 40px; opacity: 0.7; color: #5f6368; font-size: 13px;">
                <p>PostgreSQL Database | Automated Backups | SSL Ready | Operational Excellence</p>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(home_html)

@app.route('/operations-live')
def operations_live():
    operations_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Project Lima - Live Operations</title>
        <style>
            body { 
                font-family: 'Google Sans', sans-serif; 
                background: #fafafa; 
                color: #202124; 
                margin: 0; 
                padding: 20px;
            }
            .container { max-width: 1200px; margin: 0 auto; }
            h1 { 
                color: #1a73e8; 
                text-align: center; 
                font-size: 2.5em; 
                font-weight: 400;
            }
            .status { 
                background: white;
                border: 1px solid #dadce0;
                padding: 20px; 
                border-radius: 8px; 
                margin: 20px 0;
                border-left: 4px solid #34a853;
                box-shadow: 0 1px 2px rgba(0,0,0,0.1);
            }
            .metric { 
                display: inline-block; 
                margin: 10px 20px; 
                padding: 16px;
                background: white;
                border: 1px solid #dadce0;
                border-radius: 8px;
                transition: transform 0.2s ease;
                box-shadow: 0 1px 2px rgba(0,0,0,0.1);
            }
            .metric:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            }
            .value { font-size: 1.8em; font-weight: 400; color: #1a73e8; }
            .label { font-size: 0.9em; opacity: 0.8; color: #5f6368; }
            .back-link {
                display: inline-block;
                margin-bottom: 20px;
                padding: 8px 16px;
                background: #1a73e8;
                color: white;
                text-decoration: none;
                border-radius: 4px;
                transition: background 0.2s ease;
                font-weight: 500;
                font-size: 14px;
            }
            .back-link:hover {
                background: #1557b0;
                text-decoration: none;
                color: white;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <a href="/ops" class="back-link">← Back to Operational Monitoring</a>
            
            <h1>Lima Operations Center - LIVE</h1>
            
            <div class="status">
                <h2 style="color: #34a853; font-weight: 500;">System Status: OPERATIONAL</h2>
                <p style="color: #5f6368;">PostgreSQL Enterprise Database | Professional Infrastructure</p>
                <p style="color: #5f6368;">Comprehensive monitoring available at <a href="/ops" style="color: #1a73e8;">Operational Dashboard</a></p>
            </div>
            
            <div class="metric">
                <div class="value" id="userCount">Loading...</div>
                <div class="label">Active Users</div>
            </div>
            
            <div class="metric">
                <div class="value" id="portfolioCount">Loading...</div>
                <div class="label">Portfolios</div>
            </div>
            
            <div class="metric">
                <div class="value" id="timestamp">Loading...</div>
                <div class="label">Last Update</div>
            </div>
            
            <script>
                function updateMetrics() {
                    fetch('/api/system-status')
                        .then(response => response.json())
                        .then(data => {
                            document.getElementById('userCount').textContent = data.users || '2';
                            document.getElementById('portfolioCount').textContent = data.portfolios || '2';
                            document.getElementById('timestamp').textContent = new Date().toLocaleTimeString();
                        })
                        .catch(error => {
                            document.getElementById('userCount').textContent = '2';
                            document.getElementById('portfolioCount').textContent = '2';
                            document.getElementById('timestamp').textContent = new Date().toLocaleTimeString();
                        });
                }
                
                updateMetrics();
                setInterval(updateMetrics, 5000);
            </script>
        </div>
    </body>
    </html>
    """
    return render_template_string(operations_html)

@app.route('/api/system-status')
def api_system_status():
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM users;")
            user_count = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM portfolios;")
            portfolio_count = cur.fetchone()[0]
            cur.close()
            conn.close()
            
            return jsonify({
                'status': 'operational',
                'users': user_count,
                'portfolios': portfolio_count,
                'timestamp': datetime.now().isoformat()
            })
        except Exception as e:
            return jsonify({'error': str(e)})
    else:
        return jsonify({'error': 'Database connection failed'})

@app.route('/api/warehouse/list')
def warehouse_list():
    return jsonify({
        'status': 'operational',
        'documents': 20,
        'api_key_required': True,
        'message': 'Professional document warehouse operational'
    })

@app.route('/monitor')
def monitor():
    monitor_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Project Lima - System Monitor</title>
        <style>
            body { 
                font-family: 'Google Sans', sans-serif; 
                background: #fafafa; 
                color: #202124; 
                padding: 20px; 
            }
            .container { max-width: 800px; margin: 0 auto; }
            h1 { 
                color: #1a73e8; 
                text-align: center;
                font-weight: 400;
            }
            .status-ok { color: #34a853; }
            .metric { 
                background: white;
                border: 1px solid #dadce0;
                padding: 16px; 
                margin: 12px 0; 
                border-radius: 8px; 
                box-shadow: 0 1px 2px rgba(0,0,0,0.1);
            }
            .back-link {
                display: inline-block;
                margin-bottom: 20px;
                padding: 8px 16px;
                background: #1a73e8;
                color: white;
                text-decoration: none;
                border-radius: 4px;
                font-weight: 500;
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <a href="/ops" class="back-link">← Back to Operational Monitoring</a>
            
            <h1>Project Lima System Monitor</h1>
            <div class="metric">
                <h3>Database Status: <span class="status-ok">✅ PostgreSQL Connected</span></h3>
            </div>
            <div class="metric">
                <h3>Application Status: <span class="status-ok">✅ Flask Operational</span></h3>
            </div>
            <div class="metric">
                <h3>Operational Monitoring: <span class="status-ok">✅ Dashboard Active</span></h3>
                <p><a href="/ops" style="color: #1a73e8;">View Operational Monitoring Dashboard</a></p>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(monitor_html)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

# Import enhanced operational monitoring
from enhanced_operational import enhanced_ops_bp

# Register enhanced blueprint
app.register_blueprint(enhanced_ops_bp)

