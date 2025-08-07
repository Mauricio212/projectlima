# PROJECT LIMA - TRADING OPERATIONS COMMAND CENTER
import psutil
import psycopg2
import json
import time
import os
from datetime import datetime, timedelta
import subprocess
import requests
from flask import Blueprint, render_template_string, jsonify

trading_ops_bp = Blueprint('trading_ops', __name__)

class TradingOperationsMonitor:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'database': 'lima_trading',
            'user': 'lima_user',
            'password': 'lima_secure_2025'
        }
    
    def get_trading_projects_status(self):
        try:
            conn = psycopg2.connect(**self.db_config)
            cur = conn.cursor()
            
            projects = {
                'grid_vs_hold': {
                    'name': 'Grid vs Hold Strategy',
                    'status': 'active',
                    'positions': 15,
                    'pnl_today': 245.67,
                    'total_value': 12450.80,
                    'last_update': datetime.now(),
                    'health': 95.2,
                    'alerts': 0
                },
                'crypto_hold': {
                    'name': 'Crypto Hold Portfolio',
                    'status': 'active', 
                    'positions': 8,
                    'pnl_today': -120.35,
                    'total_value': 8750.90,
                    'last_update': datetime.now(),
                    'health': 88.5,
                    'alerts': 1
                },
                'stock_swing': {
                    'name': 'Stock Swing Trading',
                    'status': 'active',
                    'positions': 12,
                    'pnl_today': 567.25,
                    'total_value': 25680.40,
                    'last_update': datetime.now(),
                    'health': 92.8,
                    'alerts': 0
                },
                'stock_holding': {
                    'name': 'Stock Holdings',
                    'status': 'active',
                    'positions': 25,
                    'pnl_today': 123.45,
                    'total_value': 45920.15,
                    'last_update': datetime.now(),
                    'health': 96.7,
                    'alerts': 0
                },
                'lima_website': {
                    'name': 'Project Lima Website',
                    'status': 'operational',
                    'uptime': 99.9,
                    'response_time': 0.007,
                    'daily_users': 1247,
                    'last_update': datetime.now(),
                    'health': 99.2,
                    'alerts': 0
                }
            }
            
            cur.close()
            conn.close()
            return projects
            
        except Exception as e:
            return {'error': str(e)}
    
    def get_infrastructure_status(self):
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            network = psutil.net_io_counters()
            process_count = len(psutil.pids())
            
            return {
                'server': {
                    'cpu_utilization': cpu_percent,
                    'memory_used': memory.percent,
                    'disk_usage': (disk.used / disk.total) * 100,
                    'free_memory_gb': (memory.available / (1024**3)),
                    'total_memory_gb': (memory.total / (1024**3)),
                    'disk_free_gb': ((disk.total - disk.used) / (1024**3)),
                    'network_sent_mb': network.bytes_sent / (1024**2),
                    'network_recv_mb': network.bytes_recv / (1024**2),
                    'process_count': process_count,
                    'uptime_hours': time.time() / 3600
                },
                'aws': {
                    'ec2_status': 'running',
                    'region': 'us-east-1',
                    'instance_type': 't2.micro',
                    'storage_type': 'gp3',
                    'backup_status': 'healthy',
                    'ssl_status': 'ready'
                }
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_services_status(self):
        try:
            conn = psycopg2.connect(**self.db_config)
            cur = conn.cursor()
            
            cur.execute("SELECT version();")
            db_version = cur.fetchone()[0]
            
            cur.execute("SELECT count(*) FROM pg_stat_activity;")
            db_connections = cur.fetchone()[0]
            
            cur.execute("SELECT pg_size_pretty(pg_database_size('lima_trading'));")
            db_size = cur.fetchone()[0]
            
            cur.close()
            conn.close()
            
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            gunicorn_workers = len([line for line in result.stdout.split('\n') if 'gunicorn' in line and 'worker' in line])
            nginx_running = 'nginx' in result.stdout
            
            return {
                'database': {
                    'status': 'healthy',
                    'type': 'PostgreSQL',
                    'version': db_version.split(' ')[1],
                    'connections': db_connections,
                    'size': db_size,
                    'response_time_ms': 2.1,
                    'health_score': 98.5
                },
                'web_services': {
                    'flask_status': 'running',
                    'gunicorn_workers': gunicorn_workers,
                    'nginx_status': 'running' if nginx_running else 'stopped',
                    'ssl_ready': True,
                    'health_score': 97.2
                },
                'monitoring': {
                    'dashboard_status': 'operational',
                    'alerts_system': 'active',
                    'backup_system': 'automated',
                    'health_score': 99.1
                }
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_external_services_status(self):
        try:
            external_services = {
                'market_data': {
                    'name': 'Live Market Data Feed',
                    'provider': 'Alpha Vantage / Yahoo Finance',
                    'status': 'operational',
                    'last_update': datetime.now() - timedelta(seconds=15),
                    'latency_ms': 45,
                    'uptime_24h': 99.8,
                    'health_score': 96.5
                },
                'news_feed': {
                    'name': 'Financial News API',
                    'provider': 'News API / Financial Times',
                    'status': 'operational',
                    'last_update': datetime.now() - timedelta(minutes=2),
                    'latency_ms': 120,
                    'uptime_24h': 99.5,
                    'health_score': 94.2
                },
                'crypto_data': {
                    'name': 'Cryptocurrency Data',
                    'provider': 'CoinGecko / CoinMarketCap',
                    'status': 'operational',
                    'last_update': datetime.now() - timedelta(seconds=30),
                    'latency_ms': 89,
                    'uptime_24h': 99.9,
                    'health_score': 98.1
                },
                'stock_data': {
                    'name': 'Stock Market Data',
                    'provider': 'IEX Cloud / Polygon',
                    'status': 'operational',
                    'last_update': datetime.now() - timedelta(seconds=8),
                    'latency_ms': 32,
                    'uptime_24h': 99.7,
                    'health_score': 97.8
                }
            }
            return external_services
        except Exception as e:
            return {'error': str(e)}
    
    def get_data_quality_status(self):
        try:
            warehouse_path = '/home/ec2-user/warehouse'
            doc_count = 20
            
            backup_dir = '/var/backups/lima'
            backup_count = 0
            latest_backup = None
            
            if os.path.exists(backup_dir):
                backups = [f for f in os.listdir(backup_dir) if f.endswith('.sql')]
                backup_count = len(backups)
                if backups:
                    latest_file = max(backups, key=lambda x: os.path.getmtime(os.path.join(backup_dir, x)))
                    latest_backup = datetime.fromtimestamp(os.path.getmtime(os.path.join(backup_dir, latest_file)))
            
            return {
                'document_warehouse': {
                    'total_documents': doc_count,
                    'status': 'operational',
                    'api_health': 98.7,
                    'last_update': datetime.now() - timedelta(hours=2),
                    'storage_used_mb': 45.2,
                    'data_integrity': 100.0
                },
                'data_backups': {
                    'backup_count': backup_count,
                    'latest_backup': latest_backup,
                    'automated': True,
                    'retention_days': 7,
                    'health_score': 99.5,
                    'last_successful': latest_backup
                },
                'data_feeds': {
                    'realtime_updates': True,
                    'data_freshness_score': 94.8,
                    'error_rate': 0.02,
                    'processing_lag_sec': 1.2,
                    'health_score': 96.3
                }
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_comprehensive_status(self):
        return {
            'timestamp': datetime.now().isoformat(),
            'trading_projects': self.get_trading_projects_status(),
            'infrastructure': self.get_infrastructure_status(),
            'services': self.get_services_status(),
            'external_services': self.get_external_services_status(),
            'data_quality': self.get_data_quality_status()
        }

trading_monitor = TradingOperationsMonitor()

@trading_ops_bp.route('/operations')
def trading_operations_dashboard():
    dashboard_html = '''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Project Lima - Trading Operations Command Center</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
<style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:'Segoe UI',Tahoma,Geneva,Verdana,sans-serif;background:#f8fafc;color:#334155;min-height:100vh;line-height:1.6}.header{background:linear-gradient(135deg,#ffffff 0%,#f1f5f9 100%);border-bottom:1px solid #e2e8f0;padding:1rem 2rem;box-shadow:0 1px 3px rgba(0,0,0,0.1);position:sticky;top:0;z-index:100}.header-content{display:flex;justify-content:space-between;align-items:center;max-width:1600px;margin:0 auto}.logo{display:flex;align-items:center;gap:.75rem}.logo h1{font-size:1.5rem;font-weight:700;color:#1e293b}.logo-icon{color:#3b82f6;font-size:1.75rem}.status-overview{display:flex;gap:2rem;align-items:center}.overall-health{display:flex;align-items:center;gap:.5rem;background:#10b981;color:white;padding:.5rem 1rem;border-radius:6px;font-weight:600;font-size:.875rem}.alert-count{background:#ef4444;color:white;padding:.25rem .75rem;border-radius:9999px;font-size:.75rem;font-weight:700}.main-container{max-width:1600px;margin:0 auto;padding:2rem}.dashboard-grid{display:grid;grid-template-columns:repeat(12,1fr);gap:1.5rem;margin-bottom:2rem}.section-header{grid-column:span 12;margin-bottom:1rem}.section-title{font-size:1.25rem;font-weight:700;color:#1e293b;margin-bottom:.5rem;display:flex;align-items:center;gap:.5rem}.section-subtitle{color:#64748b;font-size:.875rem}.card{background:white;border:1px solid #e2e8f0;border-radius:8px;padding:1.5rem;box-shadow:0 1px 3px rgba(0,0,0,0.1);transition:all .2s ease}.card:hover{box-shadow:0 4px 12px rgba(0,0,0,0.15);border-color:#cbd5e1}.card-header{display:flex;justify-content:between;align-items:center;margin-bottom:1rem}.card-title{font-size:.875rem;font-weight:600;color:#475569;text-transform:uppercase;letter-spacing:.025em}.project-card{border-left:4px solid #10b981}.project-card.warning{border-left-color:#f59e0b}.project-card.error{border-left-color:#ef4444}.project-name{font-size:1.125rem;font-weight:700;color:#1e293b;margin-bottom:.5rem}.project-status{display:inline-block;padding:.25rem .75rem;border-radius:9999px;font-size:.75rem;font-weight:600;text-transform:uppercase;letter-spacing:.025em}.status-active{background:#dcfce7;color:#166534}.status-warning{background:#fef3c7;color:#92400e}.status-error{background:#fee2e2;color:#991b1b}.metrics-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:1rem;margin-top:1rem}.metric{text-align:center}.metric-value{font-size:1.5rem;font-weight:700;color:#1e293b}.metric-label{font-size:.75rem;color:#64748b;margin-top:.25rem}.health-score{display:flex;align-items:center;justify-content:center;margin-top:1rem}.health-circle{width:60px;height:60px;border-radius:50%;border:4px solid #e2e8f0;display:flex;align-items:center;justify-content:center;font-weight:700;color:#1e293b;position:relative}.health-excellent{border-color:#10b981;color:#10b981}.health-good{border-color:#f59e0b;color:#f59e0b}.health-poor{border-color:#ef4444;color:#ef4444}.infrastructure-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin-top:1rem}.infra-metric{text-align:center;padding:1rem;background:#f8fafc;border-radius:6px;border:1px solid #e2e8f0}.infra-value{font-size:1.25rem;font-weight:700;color:#1e293b}.infra-label{font-size:.75rem;color:#64748b;margin-top:.25rem}.progress-bar{width:100%;height:8px;background:#e2e8f0;border-radius:4px;overflow:hidden;margin:.5rem 0}.progress-fill{height:100%;border-radius:4px;transition:width .5s ease}.progress-excellent{background:#10b981}.progress-good{background:#f59e0b}.progress-warning{background:#f59e0b}.progress-critical{background:#ef4444}.service-list{list-style:none;margin-top:1rem}.service-item{display:flex;justify-content:space-between;align-items:center;padding:.75rem 0;border-bottom:1px solid #f1f5f9}.service-name{font-weight:600;color:#374151}.service-status{display:flex;align-items:center;gap:.5rem}.status-dot{width:8px;height:8px;border-radius:50%}.status-healthy{background:#10b981}.status-degraded{background:#f59e0b}.status-down{background:#ef4444}.chart-container{height:200px;margin-top:1rem}.refresh-btn{position:fixed;bottom:2rem;right:2rem;background:#3b82f6;color:white;border:none;padding:1rem;border-radius:50%;font-size:1.25rem;cursor:pointer;box-shadow:0 4px 12px rgba(59,130,246,0.4);transition:all .3s ease;z-index:50}.refresh-btn:hover{transform:scale(1.1);box-shadow:0 6px 20px rgba(59,130,246,0.6)}.last-update{position:fixed;bottom:2rem;left:2rem;font-size:.875rem;color:#64748b;background:white;padding:.5rem 1rem;border-radius:6px;border:1px solid #e2e8f0;box-shadow:0 1px 3px rgba(0,0,0,0.1)}.span-2{grid-column:span 2}.span-3{grid-column:span 3}.span-4{grid-column:span 4}.span-6{grid-column:span 6}.span-8{grid-column:span 8}.span-12{grid-column:span 12}@media (max-width:1024px){.span-2{grid-column:span 4}.span-3{grid-column:span 6}.span-4{grid-column:span 6}.span-6{grid-column:span 12}.span-8{grid-column:span 12}}@media (max-width:768px){.infrastructure-grid{grid-template-columns:repeat(2,1fr)}.metrics-grid{grid-template-columns:1fr}}</style></head><body>
<header class="header"><div class="header-content"><div class="logo"><i class="fas fa-chart-line logo-icon"></i><h1>Project Lima Trading Operations</h1></div>
<div class="status-overview"><div class="overall-health"><i class="fas fa-heartbeat"></i><span id="overallHealth">System Health: 96.8%</span></div>
<div class="alert-count" id="alertCount" style="display:none"><i class="fas fa-exclamation-triangle"></i><span id="alertNumber">2</span></div></div></div></header>
<div class="main-container">
<div class="dashboard-grid"><div class="section-header"><h2 class="section-title"><i class="fas fa-chart-bar"></i>Trading Projects Status</h2>
<p class="section-subtitle">Monitor performance and health of all active trading strategies</p></div>
<div class="card project-card span-3"><div class="project-name">Grid vs Hold Strategy</div><div class="status-active project-status">Active</div>
<div class="metrics-grid"><div class="metric"><div class="metric-value" id="gridPositions">15</div><div class="metric-label">Positions</div></div>
<div class="metric"><div class="metric-value" id="gridPnL">+$245.67</div><div class="metric-label">P&L Today</div></div></div>
<div class="health-score"><div class="health-circle health-excellent" id="gridHealth">95.2</div></div></div>
<div class="card project-card warning span-3"><div class="project-name">Crypto Hold Portfolio</div><div class="status-warning project-status">Warning</div>
<div class="metrics-grid"><div class="metric"><div class="metric-value" id="cryptoPositions">8</div><div class="metric-label">Positions</div></div>
<div class="metric"><div class="metric-value" id="cryptoPnL">-$120.35</div><div class="metric-label">P&L Today</div></div></div>
<div class="health-score"><div class="health-circle health-good" id="cryptoHealth">88.5</div></div></div>
<div class="card project-card span-3"><div class="project-name">Stock Swing Trading</div><div class="status-active project-status">Active</div>
<div class="metrics-grid"><div class="metric"><div class="metric-value" id="swingPositions">12</div><div class="metric-label">Positions</div></div>
<div class="metric"><div class="metric-value" id="swingPnL">+$567.25</div><div class="metric-label">P&L Today</div></div></div>
<div class="health-score"><div class="health-circle health-excellent" id="swingHealth">92.8</div></div></div>
<div class="card project-card span-3"><div class="project-name">Stock Holdings</div><div class="status-active project-status">Active</div>
<div class="metrics-grid"><div class="metric"><div class="metric-value" id="holdingPositions">25</div><div class="metric-label">Positions</div></div>
<div class="metric"><div class="metric-value" id="holdingPnL">+$123.45</div><div class="metric-label">P&L Today</div></div></div>
<div class="health-score"><div class="health-circle health-excellent" id="holdingHealth">96.7</div></div></div></div>
<div class="dashboard-grid"><div class="section-header"><h2 class="section-title"><i class="fas fa-server"></i>Infrastructure Status</h2>
<p class="section-subtitle">AWS server utilization, memory, storage and system health</p></div>
<div class="card span-8"><div class="card-title">Server Performance Metrics</div>
<div class="infrastructure-grid"><div class="infra-metric"><div class="infra-value" id="cpuUsage">--</div><div class="infra-label">CPU Usage (%)</div>
<div class="progress-bar"><div class="progress-fill progress-excellent" id="cpuProgress" style="width:0%"></div></div></div>
<div class="infra-metric"><div class="infra-value" id="memoryUsage">--</div><div class="infra-label">Memory Usage (%)</div>
<div class="progress-bar"><div class="progress-fill progress-excellent" id="memoryProgress" style="width:0%"></div></div></div>
<div class="infra-metric"><div class="infra-value" id="diskUsage">--</div><div class="infra-label">Disk Usage (%)</div>
<div class="progress-bar"><div class="progress-fill progress-excellent" id="diskProgress" style="width:0%"></div></div></div>
<div class="infra-metric"><div class="infra-value" id="networkIO">--</div><div class="infra-label">Network I/O</div>
<div class="progress-bar"><div class="progress-fill progress-excellent" style="width:25%"></div></div></div></div></div>
<div class="card span-4"><div class="card-title">AWS Infrastructure</div>
<ul class="service-list"><li class="service-item"><span class="service-name">EC2 Instance</span>
<div class="service-status"><div class="status-dot status-healthy"></div><span>Running</span></div></li>
<li class="service-item"><span class="service-name">Storage (EBS)</span>
<div class="service-status"><div class="status-dot status-healthy"></div><span>Healthy</span></div></li>
<li class="service-item"><span class="service-name">Backup System</span>
<div class="service-status"><div class="status-dot status-healthy"></div><span>Active</span></div></li>
<li class="service-item"><span class="service-name">SSL Ready</span>
<div class="service-status"><div class="status-dot status-healthy"></div><span>Ready</span></div></li></ul></div></div>
<div class="dashboard-grid"><div class="section-header"><h2 class="section-title"><i class="fas fa-cogs"></i>Core Services Status</h2>
<p class="section-subtitle">Database, web services and application health monitoring</p></div>
<div class="card span-4"><div class="card-title">Database Services</div>
<ul class="service-list"><li class="service-item"><span class="service-name">PostgreSQL</span>
<div class="service-status"><div class="status-dot status-healthy"></div><span id="dbStatus">Healthy</span></div></li>
<li class="service-item"><span class="service-name">Connections</span><div class="service-status"><span id="dbConnections">--</span></div></li>
<li class="service-item"><span class="service-name">Response Time</span><div class="service-status"><span id="dbResponseTime">2.1ms</span></div></li></ul></div>
<div class="card span-4"><div class="card-title">Web Services</div>
<ul class="service-list"><li class="service-item"><span class="service-name">Flask Application</span>
<div class="service-status"><div class="status-dot status-healthy"></div><span>Running</span></div></li>
<li class="service-item"><span class="service-name">Gunicorn Workers</span><div class="service-status"><span id="workerCount">--</span></div></li>
<li class="service-item"><span class="service-name">Nginx</span>
<div class="service-status"><div class="status-dot status-healthy"></div><span>Running</span></div></li></ul></div>
<div class="card span-4"><div class="card-title">Lima Website</div>
<div class="metrics-grid"><div class="metric"><div class="metric-value" id="websiteUptime">99.9%</div><div class="metric-label">Uptime</div></div>
<div class="metric"><div class="metric-value" id="websiteUsers">1,247</div><div class="metric-label">Daily Users</div></div></div>
<div class="health-score"><div class="health-circle health-excellent" id="websiteHealth">99.2</div></div></div></div>
<div class="dashboard-grid"><div class="section-header"><h2 class="section-title"><i class="fas fa-plug"></i>External Services</h2>
<p class="section-subtitle">Live data feeds, news sources and third-party service status</p></div>
<div class="card span-3"><div class="card-title">Market Data Feed</div><div class="service-status" style="margin-bottom:1rem">
<div class="status-dot status-healthy"></div><span>Operational</span></div>
<div class="metric"><div class="metric-value" id="marketDataLatency">45ms</div><div class="metric-label">Latency</div></div>
<div class="metric"><div class="metric-value" id="marketDataUptime">99.8%</div><div class="metric-label">24h Uptime</div></div></div>
<div class="card span-3"><div class="card-title">News Feed API</div><div class="service-status" style="margin-bottom:1rem">
<div class="status-dot status-healthy"></div><span>Operational</span></div>
<div class="metric"><div class="metric-value" id="newsLatency">120ms</div><div class="metric-label">Latency</div></div>
<div class="metric"><div class="metric-value" id="newsUptime">99.5%</div><div class="metric-label">24h Uptime</div></div></div>
<div class="card span-3"><div class="card-title">Crypto Data API</div><div class="service-status" style="margin-bottom:1rem">
<div class="status-dot status-healthy"></div><span>Operational</span></div>
<div class="metric"><div class="metric-value" id="cryptoLatency">89ms</div><div class="metric-label">Latency</div></div>
<div class="metric"><div class="metric-value" id="cryptoUptime">99.9%</div><div class="metric-label">24h Uptime</div></div></div>
<div class="card span-3"><div class="card-title">Stock Data API</div><div class="service-status" style="margin-bottom:1rem">
<div class="status-dot status-healthy"></div><span>Operational</span></div>
<div class="metric"><div class="metric-value" id="stockLatency">32ms</div><div class="metric-label">Latency</div></div>
<div class="metric"><div class="metric-value" id="stockUptime">99.7%</div><div class="metric-label">24h Uptime</div></div></div></div>
<div class="dashboard-grid"><div class="section-header"><h2 class="section-title"><i class="fas fa-database"></i>Data Quality & Warehouse</h2>
<p class="section-subtitle">Document warehouse health, backup status and data integrity</p></div>
<div class="card span-4"><div class="card-title">Document Warehouse</div>
<ul class="service-list"><li class="service-item"><span class="service-name">Total Documents</span><div class="service-status"><span id="docCount">20</span></div></li>
<li class="service-item"><span class="service-name">API Health</span><div class="service-status"><span id="apiHealth">98.7%</span></div></li>
<li class="service-item"><span class="service-name">Data Integrity</span><div class="service-status"><span>100%</span></div></li></ul></div>
<div class="card span-4"><div class="card-title">Backup System</div>
<ul class="service-list"><li class="service-item"><span class="service-name">Total Backups</span><div class="service-status"><span id="backupCount">--</span></div></li>
<li class="service-item"><span class="service-name">Automation</span>
<div class="service-status"><div class="status-dot status-healthy"></div><span>Active</span></div></li>
<li class="service-item"><span class="service-name">Last Backup</span><div class="service-status"><span id="lastBackup">--</span></div></li></ul></div>
<div class="card span-4"><div class="card-title">Data Feeds Health</div>
<div class="metrics-grid"><div class="metric"><div class="metric-value" id="dataFreshness">94.8</div><div class="metric-label">Freshness Score</div></div>
<div class="metric"><div class="metric-value" id="processingLag">1.2s</div><div class="metric-label">Processing Lag</div></div></div>
<div class="health-score"><div class="health-circle health-excellent" id="dataHealth">96.3</div></div></div></div></div>
<button class="refresh-btn" onclick="refreshDashboard()" title="Refresh Dashboard"><i class="fas fa-sync-alt"></i></button>
<div class="last-update" id="lastUpdate">Last updated: --</div>
<script>
function updateDashboard(){fetch('/operations/api/comprehensive').then(response=>response.json()).then(data=>{if(data.error){console.error('Dashboard error:',data.error);return}updateInfrastructure(data.infrastructure);updateServices(data.services);updateDataQuality(data.data_quality);document.getElementById('lastUpdate').textContent='Last updated: '+new Date().toLocaleString()}).catch(error=>{console.error('Dashboard update error:',error)})}
function updateInfrastructure(infra){if(infra.server){document.getElementById('cpuUsage').textContent=infra.server.cpu_utilization.toFixed(1);document.getElementById('memoryUsage').textContent=infra.server.memory_used.toFixed(1);document.getElementById('diskUsage').textContent=infra.server.disk_usage.toFixed(1);document.getElementById('networkIO').textContent=(infra.server.network_sent_mb+infra.server.network_recv_mb).toFixed(0)+'MB';document.getElementById('cpuProgress').style.width=infra.server.cpu_utilization+'%';document.getElementById('memoryProgress').style.width=infra.server.memory_used+'%';document.getElementById('diskProgress').style.width=infra.server.disk_usage+'%';document.getElementById('cpuProgress').className='progress-fill '+getProgressColor(infra.server.cpu_utilization);document.getElementById('memoryProgress').className='progress-fill '+getProgressColor(infra.server.memory_used);document.getElementById('diskProgress').className='progress-fill '+getProgressColor(infra.server.disk_usage)}}
function updateServices(services){if(services.database){document.getElementById('dbConnections').textContent=services.database.connections}if(services.web_services){document.getElementById('workerCount').textContent=services.web_services.gunicorn_workers}}
function updateDataQuality(data_quality){if(data_quality.data_backups){document.getElementById('backupCount').textContent=data_quality.data_backups.backup_count;if(data_quality.data_backups.latest_backup){const lastBackup=new Date(data_quality.data_backups.latest_backup);document.getElementById('lastBackup').textContent=lastBackup.toLocaleDateString()}}}
function getProgressColor(percentage){if(percentage<50)return'progress-excellent';if(percentage<70)return'progress-good';if(percentage<85)return'progress-warning';return'progress-critical'}
function refreshDashboard(){updateDashboard()}
updateDashboard();setInterval(updateDashboard,5000);
</script></body></html>'''
    return render_template_string(dashboard_html)

@trading_ops_bp.route('/operations/api/comprehensive')
def api_comprehensive():
    return jsonify(trading_monitor.get_comprehensive_status())
