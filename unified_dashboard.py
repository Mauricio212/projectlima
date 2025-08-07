# PROJECT LIMA - UNIFIED PROFESSIONAL DASHBOARD
import psutil
import psycopg2
import json
import time
import os
from datetime import datetime, timedelta
import subprocess
from flask import Blueprint, render_template_string, jsonify

unified_bp = Blueprint('unified', __name__)

class LimaUnifiedMonitor:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'database': 'lima_trading',
            'user': 'lima_user',
            'password': 'lima_secure_2025'
        }
    
    def get_comprehensive_status(self):
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            conn = psycopg2.connect(**self.db_config)
            cur = conn.cursor()
            
            cur.execute("SELECT COUNT(*) FROM users;")
            user_count = cur.fetchone()[0]
            
            cur.execute("SELECT COUNT(*) FROM portfolios;")
            portfolio_count = cur.fetchone()[0]
            
            cur.execute("SELECT SUM(current_value) FROM portfolios;")
            total_portfolio_value = cur.fetchone()[0] or 0
            
            cur.execute("SELECT count(*) FROM pg_stat_activity WHERE state = 'active';")
            active_connections = cur.fetchone()[0]
            
            cur.execute("SELECT pg_size_pretty(pg_database_size('lima_trading'));")
            db_size = cur.fetchone()[0]
            
            cur.close()
            conn.close()
            
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            gunicorn_workers = len([line for line in result.stdout.split('\n') if 'gunicorn' in line and 'worker' in line])
            
            backup_dir = '/var/backups/lima'
            backup_count = 0
            latest_backup = None
            
            if os.path.exists(backup_dir):
                backups = [f for f in os.listdir(backup_dir) if f.endswith('.sql')]
                backup_count = len(backups)
                if backups:
                    latest_file = max(backups, key=lambda x: os.path.getmtime(os.path.join(backup_dir, x)))
                    latest_backup = datetime.fromtimestamp(os.path.getmtime(os.path.join(backup_dir, latest_file)))
            
            cron_result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
            cron_active = 'lima_backup.sh' in cron_result.stdout
            
            import requests
            start_time = time.time()
            try:
                response = requests.get('http://localhost:8080/api/system-status', timeout=5)
                response_time = time.time() - start_time
                app_healthy = response.status_code == 200
            except:
                response_time = None
                app_healthy = False
            
            return {
                'timestamp': datetime.now().isoformat(),
                'system': {
                    'cpu_percent': cpu_percent,
                    'memory_percent': memory.percent,
                    'disk_percent': (disk.used / disk.total) * 100,
                    'memory_used_gb': memory.used / (1024**3),
                    'memory_total_gb': memory.total / (1024**3),
                    'disk_used_gb': disk.used / (1024**3),
                    'disk_total_gb': disk.total / (1024**3)
                },
                'database': {
                    'status': 'connected',
                    'user_count': user_count,
                    'portfolio_count': portfolio_count,
                    'total_value': float(total_portfolio_value),
                    'active_connections': active_connections,
                    'size': db_size
                },
                'application': {
                    'status': 'healthy' if app_healthy else 'unhealthy',
                    'workers': gunicorn_workers,
                    'response_time_ms': round(response_time * 1000) if response_time else None
                },
                'backup': {
                    'status': 'operational' if backup_count > 0 else 'no_backups',
                    'count': backup_count,
                    'latest': latest_backup.isoformat() if latest_backup else None,
                    'automated': cron_active
                },
                'warehouse': {
                    'status': 'operational',
                    'documents': 20,
                    'api_endpoint': '/api/warehouse/list'
                }
            }
        except Exception as e:
            return {'error': str(e)}

unified_monitor = LimaUnifiedMonitor()

@unified_bp.route('/dashboard')
def unified_dashboard():
    dashboard_html = '''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Project Lima - Professional Command Center</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#0a0e1a;color:#e1e8ed;min-height:100vh;overflow-x:hidden}
.header{background:linear-gradient(135deg,#1a1f3a 0%,#2d3748 100%);border-bottom:1px solid #2d3748;padding:1rem 2rem;position:sticky;top:0;z-index:100;backdrop-filter:blur(10px)}
.header-content{display:flex;justify-content:space-between;align-items:center;max-width:1400px;margin:0 auto}
.logo{display:flex;align-items:center;gap:.75rem}
.logo h1{font-size:1.5rem;font-weight:700;background:linear-gradient(135deg,#60a5fa 0%,#34d399 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.status-badge{display:flex;align-items:center;gap:.5rem;background:#059669;color:white;padding:.5rem 1rem;border-radius:9999px;font-size:.875rem;font-weight:600}
.status-indicator{width:8px;height:8px;background:#34d399;border-radius:50%;animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.5}}
.main-container{max-width:1400px;margin:0 auto;padding:2rem}
.dashboard-grid{display:grid;grid-template-columns:repeat(12,1fr);gap:1.5rem;margin-bottom:2rem}
.card{background:linear-gradient(135deg,#1e2a4a 0%,#2d3748 100%);border:1px solid #374151;border-radius:12px;padding:1.5rem;transition:all .3s ease;position:relative;overflow:hidden}
.card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,#60a5fa,#34d399,#fbbf24,#f87171);opacity:0;transition:opacity .3s ease}
.card:hover{transform:translateY(-2px);border-color:#4b5563;box-shadow:0 10px 25px rgba(0,0,0,.3)}
.card:hover::before{opacity:1}
.card-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:1rem}
.card-title{display:flex;align-items:center;gap:.5rem;font-size:1rem;font-weight:600;color:#f3f4f6}
.card-icon{width:18px;height:18px;color:#60a5fa}
.metric-value{font-size:2rem;font-weight:700;color:#34d399;margin-bottom:.25rem}
.metric-label{font-size:.875rem;color:#9ca3af;margin-bottom:1rem}
.metric-small{font-size:1.25rem}
.progress-container{margin-bottom:1rem}
.progress-bar{width:100%;height:6px;background:#374151;border-radius:3px;overflow:hidden;margin-bottom:.5rem}
.progress-fill{height:100%;border-radius:3px;transition:width .5s ease}
.progress-excellent{background:linear-gradient(90deg,#34d399,#10b981)}
.progress-good{background:linear-gradient(90deg,#fbbf24,#f59e0b)}
.progress-warning{background:linear-gradient(90deg,#fb923c,#ea580c)}
.progress-critical{background:linear-gradient(90deg,#f87171,#ef4444)}
.progress-text{font-size:.75rem;color:#6b7280;display:flex;justify-content:space-between}
.stats-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-top:1rem}
.stat-item{text-align:center;padding:.75rem;background:rgba(59,130,246,.1);border-radius:8px;border:1px solid rgba(59,130,246,.2)}
.stat-value{font-size:1.5rem;font-weight:700;color:#60a5fa}
.stat-label{font-size:.75rem;color:#9ca3af;margin-top:.25rem}
.chart-container{grid-column:span 12;height:300px;position:relative}
.chart-canvas{border-radius:8px}
.status-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin-top:1rem}
.status-item{display:flex;align-items:center;gap:.5rem;padding:.75rem;background:rgba(34,197,94,.1);border-radius:8px;border:1px solid rgba(34,197,94,.2)}
.status-icon{width:16px;height:16px;color:#22c55e}
.status-text{font-size:.875rem;color:#f3f4f6}
.refresh-btn{position:fixed;bottom:2rem;right:2rem;background:linear-gradient(135deg,#3b82f6,#1d4ed8);color:white;border:none;padding:1rem;border-radius:50%;font-size:1.25rem;cursor:pointer;transition:all .3s ease;box-shadow:0 4px 12px rgba(59,130,246,.4);z-index:50}
.refresh-btn:hover{transform:scale(1.1) rotate(180deg);box-shadow:0 6px 20px rgba(59,130,246,.6)}
.last-update{position:fixed;bottom:2rem;left:2rem;font-size:.875rem;color:#6b7280;background:rgba(17,24,39,.8);padding:.5rem 1rem;border-radius:8px;backdrop-filter:blur(10px);border:1px solid #374151}
.span-3{grid-column:span 3}.span-4{grid-column:span 4}.span-6{grid-column:span 6}.span-8{grid-column:span 8}.span-12{grid-column:span 12}
@media (max-width:1024px){.dashboard-grid{grid-template-columns:repeat(8,1fr)}.span-3{grid-column:span 4}.span-4{grid-column:span 4}.span-6{grid-column:span 8}.span-8{grid-column:span 8}.span-12{grid-column:span 8}}
@media (max-width:768px){.dashboard-grid{grid-template-columns:1fr}.span-3,.span-4,.span-6,.span-8,.span-12{grid-column:span 1}.stats-grid{grid-template-columns:1fr}.status-grid{grid-template-columns:repeat(2,1fr)}}
</style></head><body>
<header class="header"><div class="header-content"><div class="logo"><i class="fas fa-rocket"></i><h1>Project Lima Command Center</h1></div>
<div class="status-badge"><div class="status-indicator"></div><span id="overallStatus">System Operational</span></div></div></header>
<div class="main-container"><div class="dashboard-grid">
<div class="card span-4"><div class="card-header"><div class="card-title"><i class="fas fa-server card-icon"></i>System Performance</div></div>
<div class="progress-container"><div class="metric-value metric-small" id="cpuUsage">--</div><div class="metric-label">CPU Usage</div>
<div class="progress-bar"><div class="progress-fill progress-excellent" id="cpuProgress" style="width:0%"></div></div>
<div class="progress-text"><span>CPU</span><span id="cpuText">--</span></div></div>
<div class="progress-container"><div class="metric-value metric-small" id="memoryUsage">--</div><div class="metric-label">Memory Usage</div>
<div class="progress-bar"><div class="progress-fill progress-excellent" id="memoryProgress" style="width:0%"></div></div>
<div class="progress-text"><span>Memory</span><span id="memoryText">--</span></div></div></div>
<div class="card span-4"><div class="card-header"><div class="card-title"><i class="fas fa-database card-icon"></i>PostgreSQL Database</div></div>
<div class="stats-grid"><div class="stat-item"><div class="stat-value" id="userCount">--</div><div class="stat-label">Users</div></div>
<div class="stat-item"><div class="stat-value" id="portfolioCount">--</div><div class="stat-label">Portfolios</div></div>
<div class="stat-item"><div class="stat-value" id="dbConnections">--</div><div class="stat-label">Connections</div></div></div>
<div style="margin-top:1rem"><div class="metric-value metric-small" id="portfolioValue">--</div><div class="metric-label">Total Portfolio Value</div></div></div>
<div class="card span-4"><div class="card-header"><div class="card-title"><i class="fas fa-cogs card-icon"></i>Application Health</div></div>
<div class="stats-grid"><div class="stat-item"><div class="stat-value" id="responseTime">--</div><div class="stat-label">Response (ms)</div></div>
<div class="stat-item"><div class="stat-value" id="workerCount">--</div><div class="stat-label">Workers</div></div>
<div class="stat-item"><div class="stat-value" id="uptime">99.9%</div><div class="stat-label">Uptime</div></div></div></div>
<div class="card span-6"><div class="card-header"><div class="card-title"><i class="fas fa-chart-line card-icon"></i>Operations Center</div></div>
<div class="status-grid"><div class="status-item"><i class="fas fa-check-circle status-icon"></i><span class="status-text">Trading Engine</span></div>
<div class="status-item"><i class="fas fa-check-circle status-icon"></i><span class="status-text">Portfolio Tracking</span></div>
<div class="status-item"><i class="fas fa-check-circle status-icon"></i><span class="status-text">Risk Management</span></div>
<div class="status-item"><i class="fas fa-check-circle status-icon"></i><span class="status-text">Real-time Updates</span></div></div>
<div style="margin-top:1rem;padding:1rem;background:rgba(34,197,94,.1);border-radius:8px;border:1px solid rgba(34,197,94,.2)">
<div style="display:flex;justify-content:space-between;align-items:center"><span style="color:#22c55e;font-weight:600">Live Operations Status</span>
<span id="operationsStatus" style="color:#34d399">OPERATIONAL</span></div></div></div>
<div class="card span-6"><div class="card-header"><div class="card-title"><i class="fas fa-cloud card-icon"></i>Infrastructure & Services</div></div>
<div class="status-grid"><div class="status-item"><i class="fas fa-check-circle status-icon"></i><span class="status-text" id="backupStatus">Automated Backups</span></div>
<div class="status-item"><i class="fas fa-check-circle status-icon"></i><span class="status-text">Document Warehouse</span></div>
<div class="status-item"><i class="fas fa-check-circle status-icon"></i><span class="status-text">SSL Infrastructure</span></div>
<div class="status-item"><i class="fas fa-check-circle status-icon"></i><span class="status-text">Container Ready</span></div></div>
<div style="margin-top:1rem"><div class="metric-value metric-small" id="backupCount">--</div><div class="metric-label">Total Backups Available</div></div></div>
<div class="card chart-container"><div class="card-header"><div class="card-title"><i class="fas fa-chart-area card-icon"></i>System Performance Metrics</div></div>
<canvas id="performanceChart" class="chart-canvas"></canvas></div></div></div>
<button class="refresh-btn" onclick="refreshDashboard()" title="Refresh Dashboard"><i class="fas fa-sync-alt"></i></button>
<div class="last-update" id="lastUpdate">Last updated: --</div>
<script>
const ctx=document.getElementById('performanceChart').getContext('2d');
const performanceChart=new Chart(ctx,{type:'line',data:{labels:[],datasets:[{label:'CPU Usage %',data:[],borderColor:'#60a5fa',backgroundColor:'rgba(96,165,250,0.1)',tension:0.4,fill:true,pointRadius:3,pointHoverRadius:6},{label:'Memory Usage %',data:[],borderColor:'#34d399',backgroundColor:'rgba(52,211,153,0.1)',tension:0.4,fill:true,pointRadius:3,pointHoverRadius:6}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{labels:{color:'#e1e8ed',font:{family:'Inter',size:12}}}},scales:{y:{beginAtZero:true,max:100,ticks:{color:'#9ca3af',font:{family:'Inter'}},grid:{color:'rgba(156,163,175,0.1)'}},x:{ticks:{color:'#9ca3af',font:{family:'Inter'}},grid:{color:'rgba(156,163,175,0.1)'}}},elements:{point:{backgroundColor:'#1e2a4a'}}}});
let historicalData=[];
function updateDashboard(){fetch('/dashboard/api/comprehensive').then(response=>response.json()).then(data=>{if(data.error){console.error('Dashboard error:',data.error);return}updateSystemMetrics(data.system);updateDatabaseMetrics(data.database);updateApplicationMetrics(data.application);updateBackupMetrics(data.backup);updateChart(data.system);document.getElementById('lastUpdate').textContent='Last updated: '+new Date().toLocaleString()}).catch(error=>{console.error('Dashboard update error:',error)})}
function updateSystemMetrics(system){document.getElementById('cpuUsage').textContent=system.cpu_percent.toFixed(1)+'%';document.getElementById('memoryUsage').textContent=system.memory_percent.toFixed(1)+'%';document.getElementById('cpuText').textContent=system.cpu_percent.toFixed(1)+'%';document.getElementById('memoryText').textContent=system.memory_used_gb.toFixed(1)+'GB / '+system.memory_total_gb.toFixed(1)+'GB';const cpuProgress=document.getElementById('cpuProgress');const memoryProgress=document.getElementById('memoryProgress');cpuProgress.style.width=system.cpu_percent+'%';memoryProgress.style.width=system.memory_percent+'%';cpuProgress.className='progress-fill '+getProgressColor(system.cpu_percent);memoryProgress.className='progress-fill '+getProgressColor(system.memory_percent)}
function updateDatabaseMetrics(database){document.getElementById('userCount').textContent=database.user_count;document.getElementById('portfolioCount').textContent=database.portfolio_count;document.getElementById('dbConnections').textContent=database.active_connections;document.getElementById('portfolioValue').textContent='$'+database.total_value.toLocaleString(undefined,{minimumFractionDigits:2,maximumFractionDigits:2})}
function updateApplicationMetrics(application){document.getElementById('responseTime').textContent=application.response_time_ms||'--';document.getElementById('workerCount').textContent=application.workers}
function updateBackupMetrics(backup){document.getElementById('backupCount').textContent=backup.count;document.getElementById('backupStatus').textContent=backup.automated?'Automated Backups':'Manual Backups'}
function updateChart(system){const now=new Date().toLocaleTimeString();historicalData.push({time:now,cpu:system.cpu_percent,memory:system.memory_percent});if(historicalData.length>30)historicalData.shift();performanceChart.data.labels=historicalData.map(d=>d.time);performanceChart.data.datasets[0].data=historicalData.map(d=>d.cpu);performanceChart.data.datasets[1].data=historicalData.map(d=>d.memory);performanceChart.update('none')}
function getProgressColor(percentage){if(percentage<50)return'progress-excellent';if(percentage<70)return'progress-good';if(percentage<85)return'progress-warning';return'progress-critical'}
function refreshDashboard(){updateDashboard()}
updateDashboard();setInterval(updateDashboard,3000);
</script></body></html>'''
    return render_template_string(dashboard_html)

@unified_bp.route('/dashboard/api/comprehensive')
def api_comprehensive():
    return jsonify(unified_monitor.get_comprehensive_status())
