# PROJECT LIMA - PROFESSIONAL MONITORING DASHBOARD
import psutil
import psycopg2
import json
import time
import os
from datetime import datetime, timedelta
import subprocess
from flask import Blueprint, render_template_string, jsonify

monitoring_bp = Blueprint('monitoring', __name__)

class LimaMonitor:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'database': 'lima_trading',
            'user': 'lima_user',
            'password': 'lima_secure_2025'
        }
    
    def get_system_metrics(self):
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            network = psutil.net_io_counters()
            
            try:
                load_avg = os.getloadavg()
            except:
                load_avg = [0, 0, 0]
            
            return {
                'timestamp': datetime.now().isoformat(),
                'cpu_percent': cpu_percent,
                'memory_total': memory.total,
                'memory_used': memory.used,
                'memory_percent': memory.percent,
                'disk_total': disk.total,
                'disk_used': disk.used,
                'disk_percent': (disk.used / disk.total) * 100,
                'network_sent': network.bytes_sent,
                'network_recv': network.bytes_recv,
                'load_avg_1min': load_avg[0]
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_database_metrics(self):
        try:
            conn = psycopg2.connect(**self.db_config)
            cur = conn.cursor()
            
            cur.execute("SELECT pg_size_pretty(pg_database_size('lima_trading'));")
            db_size = cur.fetchone()[0]
            
            cur.execute("SELECT count(*) FROM pg_stat_activity WHERE state = 'active';")
            active_connections = cur.fetchone()[0]
            
            cur.execute("SELECT COUNT(*) FROM users;")
            user_count = cur.fetchone()[0]
            
            cur.execute("SELECT COUNT(*) FROM portfolios;")
            portfolio_count = cur.fetchone()[0]
            
            cur.close()
            conn.close()
            
            return {
                'timestamp': datetime.now().isoformat(),
                'database_size': db_size,
                'active_connections': active_connections,
                'user_count': user_count,
                'portfolio_count': portfolio_count,
                'status': 'connected'
            }
        except Exception as e:
            return {'error': str(e), 'status': 'disconnected'}
    
    def get_application_metrics(self):
        try:
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            gunicorn_workers = len([line for line in result.stdout.split('\n') if 'gunicorn' in line and 'worker' in line])
            
            import requests
            start_time = time.time()
            try:
                response = requests.get('http://localhost:8080/operations-live', timeout=5)
                response_time = time.time() - start_time
                app_status = 'healthy' if response.status_code == 200 else 'unhealthy'
            except:
                response_time = None
                app_status = 'unreachable'
            
            return {
                'timestamp': datetime.now().isoformat(),
                'gunicorn_workers': gunicorn_workers,
                'response_time': response_time,
                'app_status': app_status
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_backup_status(self):
        try:
            backup_dir = '/var/backups/lima'
            backups = []
            
            if os.path.exists(backup_dir):
                for file in os.listdir(backup_dir):
                    if file.endswith('.sql'):
                        file_path = os.path.join(backup_dir, file)
                        stat = os.stat(file_path)
                        backups.append({
                            'filename': file,
                            'size': stat.st_size,
                            'created': datetime.fromtimestamp(stat.st_mtime).isoformat()
                        })
            
            backups.sort(key=lambda x: x['created'], reverse=True)
            
            result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
            cron_scheduled = 'lima_backup.sh' in result.stdout
            
            return {
                'timestamp': datetime.now().isoformat(),
                'backup_count': len(backups),
                'latest_backups': backups[:5],
                'cron_scheduled': cron_scheduled,
                'status': 'operational' if backups else 'no_backups'
            }
        except Exception as e:
            return {'error': str(e)}

monitor = LimaMonitor()

@monitoring_bp.route('/monitoring')
def dashboard():
    dashboard_html = '''<!DOCTYPE html>
<html><head><title>Project Lima - Professional Monitoring</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Segoe UI',sans-serif;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:white;min-height:100vh;padding:20px}
.header{text-align:center;margin-bottom:30px;padding:20px;background:rgba(255,255,255,0.1);border-radius:15px;backdrop-filter:blur(10px)}
.header h1{font-size:2.5em;margin-bottom:10px}
.status-indicator{display:inline-block;padding:5px 15px;border-radius:20px;background:#00ff88;color:#000;font-weight:bold;margin-left:15px}
.dashboard-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(400px,1fr));gap:20px;margin-bottom:30px}
.metric-card{background:rgba(255,255,255,0.15);border-radius:15px;padding:25px;backdrop-filter:blur(10px);border:1px solid rgba(255,255,255,0.2);transition:transform 0.3s ease}
.metric-card:hover{transform:translateY(-5px)}
.metric-card h3{font-size:1.3em;margin-bottom:20px;display:flex;align-items:center}
.metric-card .icon{font-size:1.5em;margin-right:10px}
.metric-value{font-size:2.2em;font-weight:bold;color:#00ff88;margin-bottom:10px}
.metric-label{font-size:0.9em;opacity:0.8;margin-bottom:15px}
.progress-bar{width:100%;height:8px;background:rgba(255,255,255,0.2);border-radius:4px;overflow:hidden;margin-bottom:10px}
.progress-fill{height:100%;border-radius:4px;transition:width 0.3s ease}
.progress-good{background:#00ff88}
.progress-warning{background:#ffa500}
.progress-danger{background:#ff4444}
.chart-container{background:rgba(255,255,255,0.15);border-radius:15px;padding:25px;backdrop-filter:blur(10px);border:1px solid rgba(255,255,255,0.2);margin-bottom:20px}
.chart-container h3{margin-bottom:20px;font-size:1.3em}
.backup-list{max-height:200px;overflow-y:auto}
.backup-item{background:rgba(255,255,255,0.1);padding:10px;border-radius:8px;margin-bottom:8px;font-size:0.9em}
.refresh-btn{background:linear-gradient(45deg,#00ff88,#00cc6a);color:#000;border:none;padding:12px 25px;border-radius:25px;font-weight:bold;cursor:pointer;transition:transform 0.2s ease;margin:20px auto;display:block}
.refresh-btn:hover{transform:scale(1.05)}
.timestamp{text-align:center;margin-top:20px;opacity:0.7;font-size:0.9em}
@media (max-width:768px){.dashboard-grid{grid-template-columns:1fr}.header h1{font-size:2em}.status-indicator{display:block;margin:10px 0}}
</style></head><body>
<div class="header">
<h1>🚀 Project Lima Professional Monitoring</h1>
<div class="status-indicator">🟢 SYSTEM OPERATIONAL</div>
<div style="margin-top:15px;font-size:1.1em">PostgreSQL Enterprise Infrastructure | Real-time Monitoring</div>
</div>
<div class="dashboard-grid">
<div class="metric-card">
<h3><span class="icon">💻</span>System Performance</h3>
<div class="metric-value" id="cpuUsage">--</div>
<div class="metric-label">CPU Usage</div>
<div class="progress-bar"><div class="progress-fill progress-good" id="cpuProgress" style="width:0%"></div></div>
<div class="metric-value" id="memoryUsage">--</div>
<div class="metric-label">Memory Usage</div>
<div class="progress-bar"><div class="progress-fill progress-good" id="memoryProgress" style="width:0%"></div></div>
</div>
<div class="metric-card">
<h3><span class="icon">🗄️</span>PostgreSQL Database</h3>
<div class="metric-value" id="dbStatus">--</div>
<div class="metric-label">Connection Status</div>
<div style="display:flex;justify-content:space-between;margin-top:15px">
<div><div class="metric-value" style="font-size:1.5em" id="userCount">--</div><div class="metric-label">Users</div></div>
<div><div class="metric-value" style="font-size:1.5em" id="portfolioCount">--</div><div class="metric-label">Portfolios</div></div>
<div><div class="metric-value" style="font-size:1.5em" id="dbConnections">--</div><div class="metric-label">Connections</div></div>
</div></div>
<div class="metric-card">
<h3><span class="icon">🌐</span>Flask Application</h3>
<div class="metric-value" id="appStatus">--</div>
<div class="metric-label">Application Status</div>
<div style="display:flex;justify-content:space-between;margin-top:15px">
<div><div class="metric-value" style="font-size:1.5em" id="responseTime">--</div><div class="metric-label">Response Time (ms)</div></div>
<div><div class="metric-value" style="font-size:1.5em" id="workerCount">--</div><div class="metric-label">Workers</div></div>
</div></div>
<div class="metric-card">
<h3><span class="icon">💾</span>Backup System</h3>
<div class="metric-value" id="backupStatus">--</div>
<div class="metric-label">Backup Status</div>
<div style="display:flex;justify-content:space-between;margin-top:15px">
<div><div class="metric-value" style="font-size:1.5em" id="backupCount">--</div><div class="metric-label">Total Backups</div></div>
<div><div class="metric-value" style="font-size:1.2em" id="cronStatus">--</div><div class="metric-label">Automation</div></div>
</div>
<div class="backup-list" id="backupList"></div>
</div></div>
<div class="chart-container">
<h3>📊 System Performance Over Time</h3>
<canvas id="performanceChart" width="400" height="100"></canvas>
</div>
<button class="refresh-btn" onclick="refreshDashboard()">🔄 Refresh Dashboard</button>
<div class="timestamp" id="lastUpdate">Last updated: --</div>
<script>
const ctx=document.getElementById('performanceChart').getContext('2d');
const performanceChart=new Chart(ctx,{type:'line',data:{labels:[],datasets:[{label:'CPU Usage %',data:[],borderColor:'#00ff88',backgroundColor:'rgba(0,255,136,0.1)',tension:0.4,fill:true},{label:'Memory Usage %',data:[],borderColor:'#ffa500',backgroundColor:'rgba(255,165,0,0.1)',tension:0.4,fill:true}]},options:{responsive:true,scales:{y:{beginAtZero:true,max:100,ticks:{color:'#fff'},grid:{color:'rgba(255,255,255,0.2)'}},x:{ticks:{color:'#fff'},grid:{color:'rgba(255,255,255,0.2)'}}},plugins:{legend:{labels:{color:'#fff'}}}}});
let historicalData=[];
function updateMetrics(){
fetch('/monitoring/api/system').then(response=>response.json()).then(data=>{if(data.error)return;document.getElementById('cpuUsage').textContent=data.cpu_percent.toFixed(1)+'%';document.getElementById('memoryUsage').textContent=data.memory_percent.toFixed(1)+'%';const cpuProgress=document.getElementById('cpuProgress');const memoryProgress=document.getElementById('memoryProgress');cpuProgress.style.width=data.cpu_percent+'%';memoryProgress.style.width=data.memory_percent+'%';cpuProgress.className='progress-fill '+getProgressColor(data.cpu_percent);memoryProgress.className='progress-fill '+getProgressColor(data.memory_percent);const now=new Date().toLocaleTimeString();historicalData.push({time:now,cpu:data.cpu_percent,memory:data.memory_percent});if(historicalData.length>20)historicalData.shift();updateChart()});
fetch('/monitoring/api/database').then(response=>response.json()).then(data=>{if(data.error){document.getElementById('dbStatus').textContent='❌ ERROR';return}document.getElementById('dbStatus').textContent='✅ CONNECTED';document.getElementById('userCount').textContent=data.user_count;document.getElementById('portfolioCount').textContent=data.portfolio_count;document.getElementById('dbConnections').textContent=data.active_connections});
fetch('/monitoring/api/application').then(response=>response.json()).then(data=>{if(data.error){document.getElementById('appStatus').textContent='❌ ERROR';return}document.getElementById('appStatus').textContent=data.app_status==='healthy'?'✅ HEALTHY':'⚠️ '+data.app_status.toUpperCase();document.getElementById('responseTime').textContent=data.response_time?Math.round(data.response_time*1000):'--';document.getElementById('workerCount').textContent=data.gunicorn_workers});
fetch('/monitoring/api/backups').then(response=>response.json()).then(data=>{if(data.error){document.getElementById('backupStatus').textContent='❌ ERROR';return}document.getElementById('backupStatus').textContent=data.status==='operational'?'✅ OPERATIONAL':'⚠️ '+data.status.toUpperCase();document.getElementById('backupCount').textContent=data.backup_count;document.getElementById('cronStatus').textContent=data.cron_scheduled?'✅ ACTIVE':'❌ INACTIVE';const backupList=document.getElementById('backupList');backupList.innerHTML='';data.latest_backups.forEach(backup=>{const item=document.createElement('div');item.className='backup-item';const date=new Date(backup.created).toLocaleString();const size=(backup.size/1024).toFixed(1)+' KB';item.innerHTML='<strong>'+backup.filename+'</strong><br>Size: '+size+' | Created: '+date;backupList.appendChild(item)})});
document.getElementById('lastUpdate').textContent='Last updated: '+new Date().toLocaleString()}
function updateChart(){performanceChart.data.labels=historicalData.map(d=>d.time);performanceChart.data.datasets[0].data=historicalData.map(d=>d.cpu);performanceChart.data.datasets[1].data=historicalData.map(d=>d.memory);performanceChart.update()}
function getProgressColor(percentage){if(percentage<70)return'progress-good';if(percentage<85)return'progress-warning';return'progress-danger'}
function refreshDashboard(){updateMetrics()}
updateMetrics();setInterval(updateMetrics,5000);
</script></body></html>'''
    return render_template_string(dashboard_html)

@monitoring_bp.route('/monitoring/api/system')
def api_system():
    return jsonify(monitor.get_system_metrics())

@monitoring_bp.route('/monitoring/api/database')
def api_database():
    return jsonify(monitor.get_database_metrics())

@monitoring_bp.route('/monitoring/api/application')
def api_application():
    return jsonify(monitor.get_application_metrics())

@monitoring_bp.route('/monitoring/api/backups')
def api_backups():
    return jsonify(monitor.get_backup_status())
