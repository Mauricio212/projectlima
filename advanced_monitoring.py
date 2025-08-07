"""
Project Lima Advanced Monitoring - Real-Time Charts & Analytics
Phase 1: Performance Charts with Chart.js integration
"""

import json
import time
from datetime import datetime, timedelta
from collections import deque
import threading

# Global data storage for charts (in-memory for now)
performance_history = {
    "cpu": deque(maxlen=60),      # Last 60 data points (10 minutes at 10s intervals)
    "memory": deque(maxlen=60),
    "response_times": deque(maxlen=60),
    "health_scores": deque(maxlen=60),
    "timestamps": deque(maxlen=60)
}

def add_advanced_monitoring(app, socketio):
    """Add advanced monitoring with real-time charts"""
    
    @app.route('/dashboard')
    def advanced_dashboard():
        """Advanced Operations Dashboard with Charts"""
        return render_template_string(ADVANCED_DASHBOARD_TEMPLATE)
    
    @app.route('/api/performance/history')
    def get_performance_history():
        """API endpoint for chart data"""
        try:
            return jsonify({
                "cpu": list(performance_history["cpu"]),
                "memory": list(performance_history["memory"]),
                "response_times": list(performance_history["response_times"]),
                "health_scores": list(performance_history["health_scores"]),
                "timestamps": list(performance_history["timestamps"]),
                "status": "success"
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route('/api/performance/live')
    def get_live_performance():
        """Get current performance data"""
        try:
            current_data = get_current_performance_data()
            
            # Add to history
            now = datetime.now()
            performance_history["cpu"].append(current_data["cpu"])
            performance_history["memory"].append(current_data["memory"])
            performance_history["response_times"].append(current_data["response_time"])
            performance_history["health_scores"].append(current_data["health_score"])
            performance_history["timestamps"].append(now.strftime("%H:%M:%S"))
            
            return jsonify(current_data)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    # Enhanced WebSocket events for charts
    @socketio.on('request_chart_data')
    def handle_chart_data_request():
        """Handle chart data requests"""
        chart_data = {
            "cpu": list(performance_history["cpu"]),
            "memory": list(performance_history["memory"]),
            "response_times": list(performance_history["response_times"]),
            "health_scores": list(performance_history["health_scores"]),
            "timestamps": list(performance_history["timestamps"])
        }
        emit('chart_data', chart_data)
    
    # Background thread for collecting performance data
    def collect_performance_data():
        """Continuously collect performance data for charts"""
        while True:
            try:
                current_data = get_current_performance_data()
                now = datetime.now()
                
                performance_history["cpu"].append(current_data["cpu"])
                performance_history["memory"].append(current_data["memory"])
                performance_history["response_times"].append(current_data["response_time"])
                performance_history["health_scores"].append(current_data["health_score"])
                performance_history["timestamps"].append(now.strftime("%H:%M:%S"))
                
                # Emit to all connected clients
                socketio.emit('performance_update', {
                    "latest": current_data,
                    "history": {
                        "cpu": list(performance_history["cpu"])[-10:],  # Last 10 points
                        "memory": list(performance_history["memory"])[-10:],
                        "response_times": list(performance_history["response_times"])[-10:],
                        "health_scores": list(performance_history["health_scores"])[-10:],
                        "timestamps": list(performance_history["timestamps"])[-10:]
                    }
                })
                
                time.sleep(10)  # Collect every 10 seconds
            except Exception as e:
                print(f"Performance collection error: {e}")
                time.sleep(10)
    
    # Start background data collection
    perf_thread = threading.Thread(target=collect_performance_data)
    perf_thread.daemon = True
    perf_thread.start()

def get_current_performance_data():
    """Get current system performance data"""
    import psutil
    import subprocess
    
    try:
        # CPU and Memory
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        
        # Response time test
        start_time = time.time()
        try:
            result = subprocess.run(['curl', '-s', '--connect-timeout', '2', 
                                   'http://localhost:8080/api/warehouse/list'],
                                  capture_output=True, timeout=3)
            response_time = int((time.time() - start_time) * 1000)
            if result.returncode != 0:
                response_time = None
        except:
            response_time = None
        
        # Calculate health score
        health_score = calculate_health_score(cpu_percent, memory.percent, response_time)
        
        return {
            "cpu": round(cpu_percent, 1),
            "memory": round(memory.percent, 1),
            "response_time": response_time,
            "health_score": health_score,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "cpu": 0,
            "memory": 0, 
            "response_time": None,
            "health_score": 0,
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }

def calculate_health_score(cpu, memory, response_time):
    """Calculate system health score based on metrics"""
    score = 100
    
    # CPU penalty
    if cpu > 80:
        score -= 30
    elif cpu > 60:
        score -= 15
    elif cpu > 40:
        score -= 5
    
    # Memory penalty
    if memory > 90:
        score -= 25
    elif memory > 75:
        score -= 10
    elif memory > 60:
        score -= 5
    
    # Response time penalty
    if response_time is None:
        score -= 40
    elif response_time > 2000:
        score -= 20
    elif response_time > 1000:
        score -= 10
    elif response_time > 500:
        score -= 5
    
    return max(0, min(100, score))

# Advanced Dashboard Template with Charts
ADVANCED_DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project Lima - Advanced Operations Dashboard</title>
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
        
        .dashboard-container {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 20px;
            padding: 20px;
            max-width: 1600px;
            margin: 0 auto;
        }
        
        .charts-section {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        
        .chart-card {
            background: linear-gradient(145deg, #2d2d2d, #3a3a3a);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            border: 1px solid rgba(255,255,255,0.1);
        }
        
        .chart-title {
            font-size: 1.3em;
            font-weight: 600;
            margin-bottom: 15px;
            text-align: center;
        }
        
        .chart-container {
            position: relative;
            height: 250px;
        }
        
        .stats-sidebar {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        
        .stat-card {
            background: linear-gradient(145deg, #2d2d2d, #3a3a3a);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }
        
        .stat-value {
            font-size: 2.5em;
            font-weight: bold;
            margin: 10px 0;
        }
        
        .stat-label {
            color: #aaa;
            font-size: 1.1em;
        }
        
        .controls-section {
            background: linear-gradient(145deg, #2d2d2d, #3a3a3a);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }
        
        .control-button {
            width: 100%;
            padding: 12px;
            margin: 8px 0;
            background: linear-gradient(45deg, #10ac84, #00d2d3);
            border: none;
            border-radius: 8px;
            color: white;
            font-weight: bold;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .control-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(16,172,132,0.4);
        }
        
        .timestamp {
            color: #666;
            font-size: 1.0em;
            text-align: center;
            margin: 15px 0;
        }
        
        .online { color: #28a745; }
        .warning { color: #ffc107; }
        .critical { color: #dc3545; }
        
        @media (max-width: 1200px) {
            .dashboard-container {
                grid-template-columns: 1fr;
            }
            .charts-section {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 PROJECT LIMA ADVANCED OPERATIONS</h1>
        <div class="subtitle">Real-Time Performance Monitoring & Analytics</div>
        <div class="timestamp" id="lastUpdate">Initializing charts...</div>
    </div>
    
    <div class="dashboard-container">
        <div class="charts-section">
            <!-- CPU Usage Chart -->
            <div class="chart-card">
                <div class="chart-title">🖥️ CPU Usage Over Time</div>
                <div class="chart-container">
                    <canvas id="cpuChart"></canvas>
                </div>
            </div>
            
            <!-- Memory Usage Chart -->
            <div class="chart-card">
                <div class="chart-title">💾 Memory Usage Over Time</div>
                <div class="chart-container">
                    <canvas id="memoryChart"></canvas>
                </div>
            </div>
            
            <!-- Response Time Chart -->
            <div class="chart-card">
                <div class="chart-title">⚡ Response Time Trends</div>
                <div class="chart-container">
                    <canvas id="responseChart"></canvas>
                </div>
            </div>
            
            <!-- Health Score Chart -->
            <div class="chart-card">
                <div class="chart-title">❤️ System Health Score</div>
                <div class="chart-container">
                    <canvas id="healthChart"></canvas>
                </div>
            </div>
        </div>
        
        <div class="stats-sidebar">
            <!-- Current Stats -->
            <div class="stat-card">
                <div class="stat-label">Current CPU</div>
                <div class="stat-value online" id="currentCpu">--%</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-label">Current Memory</div>
                <div class="stat-value online" id="currentMemory">--%</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-label">Response Time</div>
                <div class="stat-value online" id="currentResponse">--ms</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-label">Health Score</div>
                <div class="stat-value online" id="currentHealth">--</div>
            </div>
            
            <!-- Controls -->
            <div class="controls-section">
                <h3 style="margin-bottom: 15px; text-align: center;">🎛️ Dashboard Controls</h3>
                
                <button class="control-button" onclick="refreshCharts()">
                    📊 Refresh Charts
                </button>
                
                <button class="control-button" onclick="clearHistory()">
                    🗑️ Clear History
                </button>
                
                <button class="control-button" onclick="exportData()">
                    💾 Export Data
                </button>
                
                <button class="control-button" onclick="window.open('/operations', '_blank')">
                    🎛️ Operations Center
                </button>
            </div>
        </div>
    </div>

    <script>
        // Initialize Socket.IO
        const socket = io();
        
        // Chart instances
        let cpuChart, memoryChart, responseChart, healthChart;
        
        // Initialize charts
        function initializeCharts() {
            const chartOptions = {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(255,255,255,0.1)'
                        },
                        ticks: {
                            color: '#aaa'
                        }
                    },
                    x: {
                        grid: {
                            color: 'rgba(255,255,255,0.1)'
                        },
                        ticks: {
                            color: '#aaa'
                        }
                    }
                }
            };
            
            // CPU Chart
            cpuChart = new Chart(document.getElementById('cpuChart'), {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'CPU %',
                        data: [],
                        borderColor: '#3498db',
                        backgroundColor: 'rgba(52, 152, 219, 0.1)',
                        fill: true,
                        tension: 0.4
                    }]
                },
                options: {
                    ...chartOptions,
                    scales: {
                        ...chartOptions.scales,
                        y: { ...chartOptions.scales.y, max: 100 }
                    }
                }
            });
            
            // Memory Chart
            memoryChart = new Chart(document.getElementById('memoryChart'), {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Memory %',
                        data: [],
                        borderColor: '#e74c3c',
                        backgroundColor: 'rgba(231, 76, 60, 0.1)',
                        fill: true,
                        tension: 0.4
                    }]
                },
                options: {
                    ...chartOptions,
                    scales: {
                        ...chartOptions.scales,
                        y: { ...chartOptions.scales.y, max: 100 }
                    }
                }
            });
            
            // Response Time Chart
            responseChart = new Chart(document.getElementById('responseChart'), {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Response Time (ms)',
                        data: [],
                        borderColor: '#f39c12',
                        backgroundColor: 'rgba(243, 156, 18, 0.1)',
                        fill: true,
                        tension: 0.4
                    }]
                },
                options: chartOptions
            });
            
            // Health Score Chart
            healthChart = new Chart(document.getElementById('healthChart'), {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Health Score',
                        data: [],
                        borderColor: '#2ecc71',
                        backgroundColor: 'rgba(46, 204, 113, 0.1)',
                        fill: true,
                        tension: 0.4
                    }]
                },
                options: {
                    ...chartOptions,
                    scales: {
                        ...chartOptions.scales,
                        y: { ...chartOptions.scales.y, max: 100 }
                    }
                }
            });
        }
        
        // Update charts with new data
        function updateCharts(data) {
            const { cpu, memory, response_times, health_scores, timestamps } = data;
            
            // Update CPU chart
            cpuChart.data.labels = timestamps;
            cpuChart.data.datasets[0].data = cpu;
            cpuChart.update('none');
            
            // Update Memory chart
            memoryChart.data.labels = timestamps;
            memoryChart.data.datasets[0].data = memory;
            memoryChart.update('none');
            
            // Update Response Time chart
            responseChart.data.labels = timestamps;
            responseChart.data.datasets[0].data = response_times;
            responseChart.update('none');
            
            // Update Health Score chart
            healthChart.data.labels = timestamps;
            healthChart.data.datasets[0].data = health_scores;
            healthChart.update('none');
        }
        
        // Update current stats
        function updateCurrentStats(data) {
            document.getElementById('currentCpu').textContent = data.cpu + '%';
            document.getElementById('currentMemory').textContent = data.memory + '%';
            document.getElementById('currentResponse').textContent = data.response_time ? data.response_time + 'ms' : 'N/A';
            document.getElementById('currentHealth').textContent = data.health_score;
            
            // Update colors based on values
            const cpuElement = document.getElementById('currentCpu');
            const memoryElement = document.getElementById('currentMemory');
            const healthElement = document.getElementById('currentHealth');
            
            // CPU color coding
            cpuElement.className = 'stat-value ' + (data.cpu > 80 ? 'critical' : data.cpu > 60 ? 'warning' : 'online');
            
            // Memory color coding
            memoryElement.className = 'stat-value ' + (data.memory > 80 ? 'critical' : data.memory > 60 ? 'warning' : 'online');
            
            // Health color coding
            healthElement.className = 'stat-value ' + (data.health_score < 50 ? 'critical' : data.health_score < 70 ? 'warning' : 'online');
        }
        
        // Socket event handlers
        socket.on('connect', function() {
            document.getElementById('lastUpdate').textContent = 'Connected - Loading chart data...';
            socket.emit('request_chart_data');
        });
        
        socket.on('chart_data', function(data) {
            updateCharts(data);
            if (data.timestamps.length > 0) {
                const latest = {
                    cpu: data.cpu[data.cpu.length - 1],
                    memory: data.memory[data.memory.length - 1],
                    response_time: data.response_times[data.response_times.length - 1],
                    health_score: data.health_scores[data.health_scores.length - 1]
                };
                updateCurrentStats(latest);
            }
            document.getElementById('lastUpdate').textContent = 'Last Update: ' + new Date().toLocaleString();
        });
        
        socket.on('performance_update', function(data) {
            updateCurrentStats(data.latest);
            updateCharts({
                cpu: data.history.cpu,
                memory: data.history.memory,
                response_times: data.history.response_times,
                health_scores: data.history.health_scores,
                timestamps: data.history.timestamps
            });
            document.getElementById('lastUpdate').textContent = 'Last Update: ' + new Date().toLocaleString();
        });
        
        // Control functions
        function refreshCharts() {
            socket.emit('request_chart_data');
        }
        
        function clearHistory() {
            if (confirm('Clear all chart history? This cannot be undone.')) {
                fetch('/api/performance/clear', { method: 'POST' })
                    .then(() => refreshCharts());
            }
        }
        
        function exportData() {
            fetch('/api/performance/history')
                .then(response => response.json())
                .then(data => {
                    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'lima-performance-data.json';
                    a.click();
                });
        }
        
        // Initialize everything
        document.addEventListener('DOMContentLoaded', function() {
            initializeCharts();
        });
    </script>
</body>
</html>
'''
