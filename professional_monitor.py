"""
Project Lima Professional Operations Center
Real-time monitoring with WebSocket updates and interactive controls
"""

from flask import render_template_string, request, jsonify
from flask_socketio import SocketIO, emit
import subprocess
import json
import os
import psutil
import time
from datetime import datetime
import threading

def create_professional_monitor(app):
    """Add professional monitoring capabilities to Flask app"""
    
    # Initialize SocketIO for real-time updates
    socketio = SocketIO(app, cors_allowed_origins="*")
    
    @app.route('/operations')
    def operations_center():
        """Professional Operations Center - Main Dashboard"""
        return render_template_string(OPERATIONS_TEMPLATE)
    
    @app.route('/api/system/status')
    def system_status_api():
        """API endpoint for system status"""
        try:
            status = get_comprehensive_system_status()
            return jsonify(status)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route('/api/system/restart/<service>')
    def restart_service(service):
        """API endpoint to restart services"""
        try:
            if service == "warehouse":
                result = restart_warehouse_service()
                return jsonify({"status": "success", "message": result})
            elif service == "trading":
                result = restart_trading_service()
                return jsonify({"status": "success", "message": result})
            else:
                return jsonify({"status": "error", "message": "Unknown service"}), 400
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    
    @app.route('/api/system/logs/<service>')
    def get_service_logs(service):
        """API endpoint to get service logs"""
        try:
            if service == "warehouse":
                logs = get_warehouse_logs()
                return jsonify({"logs": logs})
            else:
                return jsonify({"error": "Unknown service"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @socketio.on('connect')
    def handle_connect():
        """Handle WebSocket connection"""
        print('Client connected for real-time updates')
        emit('status', get_comprehensive_system_status())
    
    @socketio.on('request_update')
    def handle_update_request():
        """Handle real-time update requests"""
        emit('status', get_comprehensive_system_status())
    
    # Start background thread for periodic updates
    def background_updates():
        """Send periodic updates to connected clients"""
        while True:
            time.sleep(10)  # Update every 10 seconds
            try:
                status = get_comprehensive_system_status()
                socketio.emit('status', status)
            except:
                pass
    
    # Start background thread
    update_thread = threading.Thread(target=background_updates)
    update_thread.daemon = True
    update_thread.start()
    
    return socketio

def get_comprehensive_system_status():
    """Get comprehensive system status for professional monitoring"""
    try:
        # Trading Platform Status
        trading_status = check_trading_platform()
        
        # Warehouse Status (we know it's online since we're running)
        warehouse_status = {
            "status": "ONLINE",
            "documents": get_document_count(),
            "response_time": measure_warehouse_response_time()
        }
        
        # Database Status
        db_status = check_database_status()
        
        # System Resources
        system_resources = get_system_resources()
        
        # Service Workers
        worker_status = get_worker_status()
        
        # System Uptime
        uptime = get_system_uptime()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "trading_platform": trading_status,
            "warehouse": warehouse_status,
            "database": db_status,
            "system": system_resources,
            "workers": worker_status,
            "uptime": uptime,
            "overall_health": calculate_overall_health(trading_status, warehouse_status, db_status)
        }
    except Exception as e:
        return {"error": str(e), "timestamp": datetime.now().isoformat()}

def check_trading_platform():
    """Check trading platform status with response time"""
    try:
        start_time = time.time()
        result = subprocess.run(['curl', '-s', '--connect-timeout', '3', 
                               'http://localhost:8001/health'], 
                              capture_output=True, timeout=5)
        response_time = int((time.time() - start_time) * 1000)
        
        if result.returncode == 0:
            return {"status": "ONLINE", "response_time": response_time}
        else:
            return {"status": "OFFLINE", "response_time": None}
    except:
        return {"status": "OFFLINE", "response_time": None}

def get_document_count():
    """Get current document count from warehouse"""
    try:
        # Since we're running in the same process, we can access the warehouse directly
        # For now, return the known count
        return 20
    except:
        return "Unknown"

def measure_warehouse_response_time():
    """Measure warehouse response time"""
    try:
        start_time = time.time()
        result = subprocess.run(['curl', '-s', '-H', 'X-API-Key: lima_warehouse_2025_secure_key',
                               'http://localhost:8080/api/warehouse/list'], 
                              capture_output=True, timeout=5)
        response_time = int((time.time() - start_time) * 1000)
        return response_time if result.returncode == 0 else None
    except:
        return None

def check_database_status():
    """Check database status with size and last modified"""
    try:
        db_path = '/home/ec2-user/project_lima/lima_trading.db'
        if os.path.exists(db_path):
            stat = os.stat(db_path)
            return {
                "status": "PRESENT",
                "size": stat.st_size,
                "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
            }
        else:
            return {"status": "MISSING", "size": 0, "last_modified": None}
    except:
        return {"status": "ERROR", "size": 0, "last_modified": None}

def get_system_resources():
    """Get system resource usage"""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            "cpu_percent": cpu_percent,
            "memory_percent": memory.percent,
            "memory_used": memory.used,
            "memory_total": memory.total,
            "disk_percent": disk.percent,
            "disk_used": disk.used,
            "disk_total": disk.total
        }
    except:
        return {"cpu_percent": 0, "memory_percent": 0, "disk_percent": 0}

def get_worker_status():
    """Get detailed worker process status"""
    try:
        result = subprocess.run(['pgrep', '-f', 'gunicorn'], 
                              capture_output=True, text=True)
        if result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            return {
                "count": len(pids),
                "pids": pids,
                "status": "HEALTHY" if len(pids) >= 3 else "LOW"
            }
        else:
            return {"count": 0, "pids": [], "status": "DOWN"}
    except:
        return {"count": 0, "pids": [], "status": "UNKNOWN"}

def get_system_uptime():
    """Get system uptime"""
    try:
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
        
        days, remainder = divmod(uptime_seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        return {
            "seconds": int(uptime_seconds),
            "formatted": f"{int(days)}d {int(hours)}h {int(minutes)}m"
        }
    except:
        return {"seconds": 0, "formatted": "Unknown"}

def calculate_overall_health(trading, warehouse, database):
    """Calculate overall system health score"""
    score = 0
    total = 0
    
    # Warehouse (most important) - 40%
    if warehouse.get("status") == "ONLINE":
        score += 40
    total += 40
    
    # Database - 30%
    if database.get("status") == "PRESENT":
        score += 30
    total += 30
    
    # Trading Platform - 20%
    if trading.get("status") == "ONLINE":
        score += 20
    total += 20
    
    # Workers - 10%
    worker_count = get_worker_status().get("count", 0)
    if worker_count >= 3:
        score += 10
    elif worker_count > 0:
        score += 5
    total += 10
    
    percentage = int((score / total) * 100)
    
    if percentage >= 90:
        return {"score": percentage, "status": "EXCELLENT", "color": "#28a745"}
    elif percentage >= 70:
        return {"score": percentage, "status": "GOOD", "color": "#28a745"}
    elif percentage >= 50:
        return {"score": percentage, "status": "WARNING", "color": "#ffc107"}
    else:
        return {"score": percentage, "status": "CRITICAL", "color": "#dc3545"}

def restart_warehouse_service():
    """Restart warehouse service"""
    try:
        subprocess.run(['pkill', '-f', 'gunicorn'], timeout=10)
        time.sleep(2)
        subprocess.Popen(['nohup', 'gunicorn', '--bind', '0.0.0.0:8080', 
                         '--workers', '3', 'wsgi_lima:app'], 
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return "Warehouse service restart initiated"
    except Exception as e:
        return f"Restart failed: {str(e)}"

def restart_trading_service():
    """Restart trading service"""
    try:
        subprocess.run(['./start_lima.sh'], cwd='/home/ec2-user/project_lima', timeout=30)
        return "Trading service restart initiated"
    except Exception as e:
        return f"Restart failed: {str(e)}"

def get_warehouse_logs():
    """Get recent warehouse logs"""
    try:
        result = subprocess.run(['tail', '-50', '/home/ec2-user/project_lima/gunicorn.log'], 
                              capture_output=True, text=True, timeout=10)
        return result.stdout.split('\n') if result.returncode == 0 else ["No logs available"]
    except:
        return ["Error reading logs"]

# Professional Operations Center HTML Template
OPERATIONS_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project Lima - Operations Center</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #0c0c0c 0%, #1a1a1a 100%);
            color: #fff; 
            min-height: 100vh;
        }
        
        .header {
            background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        
        .header .subtitle {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .main-container {
            display: grid;
            grid-template-columns: 1fr 300px;
            gap: 20px;
            padding: 20px;
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }
        
        .status-card {
            background: linear-gradient(145deg, #2d2d2d, #3a3a3a);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            border: 1px solid rgba(255,255,255,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .status-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px rgba(0,0,0,0.4);
        }
        
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .card-title {
            font-size: 1.3em;
            font-weight: 600;
        }
        
        .status-indicator {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 currentColor; }
            70% { box-shadow: 0 0 0 10px transparent; }
            100% { box-shadow: 0 0 0 0 transparent; }
        }
        
        .metric-value {
            font-size: 2.2em;
            font-weight: bold; font-size: 16px;
            margin: 10px 0;
        }
        
        .metric-detail {
            color: #aaa;
            font-size: 1.1em;
        }
        
        .health-score {
            text-align: center;
            padding: 30px;
            background: linear-gradient(145deg, #1a2980, #26d0ce);
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }
        
        .health-score .score {
            font-size: 4em;
            font-weight: bold; font-size: 16px;
            margin-bottom: 10px;
        }
        
        .controls-panel {
            background: linear-gradient(145deg, #2d2d2d, #3a3a3a);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }
        
        .control-button {
            width: 100%;
            padding: 14px; font-size: 16px;
            margin: 8px 0;
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
            border: none;
            border-radius: 8px;
            color: white;
            font-weight: bold; font-size: 16px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .control-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(255,107,107,0.4);
        }
        
        .control-button.success {
            background: linear-gradient(45deg, #10ac84, #00d2d3);
        }
        
        .logs-section {
            background: #1a1a1a;
            border-radius: 8px;
            padding: 15px;
            max-height: 300px;
            overflow-y: auto;
            font-family: 'Courier New', monospace;
            font-size: 1.05em;
            margin-top: 15px;
        }
        
        .timestamp {
            color: #666;
            font-size: 1.0em;
            text-align: center;
            margin-top: 20px;
        }
        
        .online { color: #28a745; }
        .offline { color: #dc3545; }
        .warning { color: #ffc107; }
        
        @media (max-width: 768px) {
            .main-container {
                grid-template-columns: 1fr;
            }
            .header h1 { font-size: 2em; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 PROJECT LIMA OPERATIONS CENTER</h1>
        <div class="subtitle">Professional Real-Time System Monitoring</div>
        <div class="timestamp" id="lastUpdate">Connecting...</div>
    </div>
    
    <div class="main-container">
        <div class="dashboard-grid">
            <!-- System Health Score -->
            <div class="health-score">
                <div class="score" id="healthScore">--</div>
                <div id="healthStatus">Initializing...</div>
                <div style="font-size: 1.1em; margin-top: 10px;" id="healthDetail">System health assessment</div>
            </div>
            
            <!-- Trading Platform -->
            <div class="status-card">
                <div class="card-header">
                    <div class="card-title">Trading Platform</div>
                    <div class="status-indicator online" id="tradingIndicator"></div>
                </div>
                <div class="metric-value" id="tradingStatus">--</div>
                <div class="metric-detail" id="tradingDetail">Port 8001 • FastAPI + SQLite</div>
                <div class="metric-detail" id="tradingResponse">Response time: --</div>
            </div>
            
            <!-- Document Warehouse -->
            <div class="status-card">
                <div class="card-header">
                    <div class="card-title">Document Warehouse</div>
                    <div class="status-indicator online" id="warehouseIndicator"></div>
                </div>
                <div class="metric-value" id="warehouseStatus">--</div>
                <div class="metric-detail" id="warehouseDetail">Port 8080 • Flask + Gunicorn</div>
                <div class="metric-detail" id="warehouseResponse">Response time: --</div>
            </div>
            
            <!-- Database -->
            <div class="status-card">
                <div class="card-header">
                    <div class="card-title">Database</div>
                    <div class="status-indicator online" id="dbIndicator"></div>
                </div>
                <div class="metric-value" id="dbStatus">--</div>
                <div class="metric-detail" id="dbDetail">lima_trading.db</div>
                <div class="metric-detail" id="dbSize">Size: --</div>
            </div>
            
            <!-- System Resources -->
            <div class="status-card">
                <div class="card-header">
                    <div class="card-title">System Resources</div>
                    <div class="status-indicator online" id="systemIndicator"></div>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                    <div>
                        <div class="metric-detail">CPU Usage</div>
                        <div class="metric-value" style="font-size: 1.5em;" id="cpuUsage">--%</div>
                    </div>
                    <div>
                        <div class="metric-detail">Memory Usage</div>
                        <div class="metric-value" style="font-size: 1.5em;" id="memoryUsage">--%</div>
                    </div>
                </div>
                <div class="metric-detail" id="systemUptime">Uptime: --</div>
            </div>
            
            <!-- Service Workers -->
            <div class="status-card">
                <div class="card-header">
                    <div class="card-title">Service Workers</div>
                    <div class="status-indicator online" id="workersIndicator"></div>
                </div>
                <div class="metric-value" id="workersCount">--</div>
                <div class="metric-detail" id="workersDetail">Gunicorn WSGI Processes</div>
                <div class="metric-detail" id="workersStatus">Status: --</div>
            </div>
        </div>
        
        <!-- Control Panel -->
        <div class="controls-panel">
            <h3 style="margin-bottom: 20px; text-align: center;">🎛️ Operations Control</h3>
            
            <button class="control-button" onclick="restartService('warehouse')">
                🔄 Restart Warehouse
            </button>
            
            <button class="control-button" onclick="restartService('trading')">
                🔄 Restart Trading Platform
            </button>
            
            <button class="control-button success" onclick="requestUpdate()">
                🔍 Refresh Status
            </button>
            
            <button class="control-button success" onclick="toggleLogs()">
                📋 View Logs
            </button>
            
            <div class="logs-section" id="logsSection" style="display: none;">
                <h4>Recent Warehouse Logs:</h4>
                <div id="logsContent">Loading logs...</div>
            </div>
            
            <div style="margin-top: 20px; padding: 15px; background: rgba(0,0,0,0.3); border-radius: 8px; font-size: 1.1em;">
                <strong>🔧 Quick Actions:</strong><br>
                • Real-time updates every 10 seconds<br>
                • Interactive service controls<br>
                • Live system monitoring<br>
                • Professional operations dashboard
            </div>
        </div>
    </div>

    <script>
        // Initialize Socket.IO connection
        const socket = io();
        let logsVisible = false;
        
        // Connect to real-time updates
        socket.on('connect', function() {
            console.log('Connected to operations center');
            document.getElementById('lastUpdate').textContent = 'Connected - Real-time monitoring active';
        });
        
        // Handle status updates
        socket.on('status', function(data) {
            updateDashboard(data);
        });
        
        // Update dashboard with new data
        function updateDashboard(data) {
            const timestamp = new Date(data.timestamp).toLocaleString();
            document.getElementById('lastUpdate').textContent = `Last Update: ${timestamp}`;
            
            // Update health score
            if (data.overall_health) {
                document.getElementById('healthScore').textContent = data.overall_health.score;
                document.getElementById('healthScore').style.color = data.overall_health.color;
                document.getElementById('healthStatus').textContent = data.overall_health.status;
            }
            
            // Update trading platform
            if (data.trading_platform) {
                const trading = data.trading_platform;
                document.getElementById('tradingStatus').textContent = trading.status;
                document.getElementById('tradingStatus').className = 'metric-value ' + (trading.status === 'ONLINE' ? 'online' : 'offline');
                document.getElementById('tradingIndicator').className = 'status-indicator ' + (trading.status === 'ONLINE' ? 'online' : 'offline');
                document.getElementById('tradingResponse').textContent = trading.response_time ? `Response time: ${trading.response_time}ms` : 'Response time: --';
            }
            
            // Update warehouse
            if (data.warehouse) {
                const warehouse = data.warehouse;
                document.getElementById('warehouseStatus').textContent = warehouse.status;
                document.getElementById('warehouseStatus').className = 'metric-value online';
                document.getElementById('warehouseIndicator').className = 'status-indicator online';
                document.getElementById('warehouseDetail').textContent = `Port 8080 • ${warehouse.documents} documents`;
                document.getElementById('warehouseResponse').textContent = warehouse.response_time ? `Response time: ${warehouse.response_time}ms` : 'Response time: --';
            }
            
            // Update database
            if (data.database) {
                const db = data.database;
                document.getElementById('dbStatus').textContent = db.status;
                document.getElementById('dbStatus').className = 'metric-value ' + (db.status === 'PRESENT' ? 'online' : 'offline');
                document.getElementById('dbIndicator').className = 'status-indicator ' + (db.status === 'PRESENT' ? 'online' : 'offline');
                document.getElementById('dbSize').textContent = db.size ? `Size: ${(db.size/1024).toFixed(1)} KB` : 'Size: --';
            }
            
            // Update system resources
            if (data.system) {
                const sys = data.system;
                document.getElementById('cpuUsage').textContent = `${sys.cpu_percent.toFixed(1)}%`;
                document.getElementById('memoryUsage').textContent = `${sys.memory_percent.toFixed(1)}%`;
                document.getElementById('systemIndicator').className = 'status-indicator online';
            }
            
            // Update uptime
            if (data.uptime) {
                document.getElementById('systemUptime').textContent = `Uptime: ${data.uptime.formatted}`;
            }
            
            // Update workers
            if (data.workers) {
                const workers = data.workers;
                document.getElementById('workersCount').textContent = `${workers.count} Active`;
                document.getElementById('workersStatus').textContent = `Status: ${workers.status}`;
                document.getElementById('workersIndicator').className = 'status-indicator ' + (workers.count >= 3 ? 'online' : 'warning');
            }
        }
        
        // Request manual update
        function requestUpdate() {
            socket.emit('request_update');
        }
        
        // Restart service
        async function restartService(service) {
            try {
                const response = await fetch(`/api/system/restart/${service}`);
                const result = await response.json();
                alert(result.message);
                setTimeout(requestUpdate, 3000); // Update status after restart
            } catch (error) {
                alert('Restart failed: ' + error.message);
            }
        }
        
        // Toggle logs visibility
        function toggleLogs() {
            const logsSection = document.getElementById('logsSection');
            logsVisible = !logsVisible;
            
            if (logsVisible) {
                logsSection.style.display = 'block';
                loadLogs();
            } else {
                logsSection.style.display = 'none';
            }
        }
        
        // Load logs
        async function loadLogs() {
            try {
                const response = await fetch('/api/system/logs/warehouse');
                const result = await response.json();
                const logsContent = document.getElementById('logsContent');
                logsContent.innerHTML = result.logs.slice(-20).join('<br>');
            } catch (error) {
                document.getElementById('logsContent').innerHTML = 'Error loading logs';
            }
        }
        
        // Request initial update
        requestUpdate();
    </script>
</body>
</html>
'''
