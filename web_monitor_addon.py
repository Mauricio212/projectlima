# Lima System Web Monitor - Add to existing Flask app
from flask import render_template_string
import subprocess
import json
import os
from datetime import datetime

def add_monitor_routes(app):
    """Add web monitoring routes to existing Flask app"""
    
    @app.route('/monitor')
    def system_monitor():
        # Get system status (same logic as your dashboard script)
        try:
            # Check trading platform
            trading_status = "OFFLINE"
            try:
                result = subprocess.run(['curl', '-s', '--connect-timeout', '3', 
                                       'http://localhost:8001/health'], 
                                     capture_output=True, timeout=5)
                if result.returncode == 0:
                    trading_status = "ONLINE"
            except:
                pass
            
            # Check warehouse (we know it's online since we're running)
            warehouse_status = "ONLINE"
            doc_count = "20+"
            
            # Check database
            db_status = "PRESENT" if os.path.exists('/home/ec2-user/project_lima/lima_trading.db') else "MISSING"
            if db_status == "PRESENT":
                db_size = os.path.getsize('/home/ec2-user/project_lima/lima_trading.db')
            else:
                db_size = 0
            
            # Check workers
            try:
                result = subprocess.run(['pgrep', '-f', 'gunicorn'], 
                                      capture_output=True, text=True)
                worker_count = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
            except:
                worker_count = 0
            
            # Get current time
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
            
            return render_template_string(MONITOR_TEMPLATE, 
                                        trading_status=trading_status,
                                        warehouse_status=warehouse_status,
                                        doc_count=doc_count,
                                        db_status=db_status,
                                        db_size=db_size,
                                        worker_count=worker_count,
                                        current_time=current_time)
        except Exception as e:
            return f"<h1>Monitor Error</h1><p>{str(e)}</p>"

# HTML Template for the monitor page
MONITOR_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Project Lima - System Monitor</title>
    <meta http-equiv="refresh" content="30">
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #1a1a1a; color: #fff; }
        .header { text-align: center; margin-bottom: 40px; }
        .status-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .status-card { background: #2d2d2d; padding: 20px; border-radius: 8px; border-left: 4px solid #007acc; }
        .online { border-left-color: #28a745; }
        .offline { border-left-color: #dc3545; }
        .status-title { font-size: 18px; font-weight: bold; margin-bottom: 10px; }
        .status-value { font-size: 24px; margin: 10px 0; }
        .status-detail { color: #aaa; font-size: 14px; }
        .footer { text-align: center; margin-top: 40px; color: #666; }
        .timestamp { font-size: 12px; color: #888; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 PROJECT LIMA SYSTEM MONITOR</h1>
        <p class="timestamp">Last Update: {{ current_time }}</p>
        <p style="color: #666;">Auto-refresh every 30 seconds</p>
    </div>
    
    <div class="status-grid">
        <div class="status-card {% if trading_status == 'ONLINE' %}online{% else %}offline{% endif %}">
            <div class="status-title">Trading Platform</div>
            <div class="status-value">{{ trading_status }}</div>
            <div class="status-detail">Port 8001 • FastAPI + SQLite</div>
        </div>
        
        <div class="status-card online">
            <div class="status-title">Document Warehouse</div>
            <div class="status-value">{{ warehouse_status }}</div>
            <div class="status-detail">Port 8080 • {{ doc_count }} documents</div>
        </div>
        
        <div class="status-card {% if db_status == 'PRESENT' %}online{% else %}offline{% endif %}">
            <div class="status-title">Database</div>
            <div class="status-value">{{ db_status }}</div>
            <div class="status-detail">lima_trading.db • {{ "%.1f"|format(db_size/1024) }} KB</div>
        </div>
        
        <div class="status-card {% if worker_count > 0 %}online{% else %}offline{% endif %}">
            <div class="status-title">Service Workers</div>
            <div class="status-value">{{ worker_count }} Active</div>
            <div class="status-detail">Gunicorn WSGI processes</div>
        </div>
    </div>
    
    <div class="footer">
        <p>🎯 Project Lima Operations Monitor</p>
        <p style="font-size: 12px;">
            <a href="/api/warehouse/list" style="color: #007acc;">Warehouse API</a> • 
            <a href="http://52.200.101.103:8001" style="color: #007acc;">Trading Platform</a>
        </p>
    </div>
</body>
</html>
'''
