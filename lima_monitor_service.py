#!/usr/bin/env python3
"""
Project Lima Active Monitoring Service
Integrates with advanced_monitoring and logs system health
"""
import sys
import time
import json
import psutil
from datetime import datetime

sys.path.append('/home/ec2-user/project_lima')
import advanced_monitoring

def get_system_metrics():
    """Get current system metrics"""
    return {
        'cpu': psutil.cpu_percent(interval=1),
        'memory': psutil.virtual_memory().percent,
        'disk': psutil.disk_usage('/').percent,
        'timestamp': datetime.now().isoformat()
    }

def calculate_health_score(cpu, memory, response_time=0.5):
    """Calculate system health score (0-100)"""
    cpu_health = max(0, 100 - cpu)
    memory_health = max(0, 100 - memory) 
    response_health = max(0, 100 - (response_time * 100))
    return round((cpu_health + memory_health + response_health) / 3, 1)

def log_monitoring_data():
    """Log monitoring data with alerts"""
    metrics = get_system_metrics()
    health = calculate_health_score(metrics['cpu'], metrics['memory'])
    
    # Log to file
    log_entry = {
        'timestamp': metrics['timestamp'],
        'cpu': metrics['cpu'],
        'memory': metrics['memory'], 
        'disk': metrics['disk'],
        'health_score': health,
        'alerts': []
    }
    
    # Generate alerts
    if metrics['cpu'] > 80:
        log_entry['alerts'].append(f"HIGH CPU: {metrics['cpu']:.1f}%")
    if metrics['memory'] > 80:
        log_entry['alerts'].append(f"HIGH MEMORY: {metrics['memory']:.1f}%")
    if metrics['disk'] > 85:
        log_entry['alerts'].append(f"HIGH DISK: {metrics['disk']:.1f}%")
    
    # Write to log
    with open('/home/ec2-user/project_lima/logs/monitoring.log', 'a') as f:
        f.write(json.dumps(log_entry) + '\n')
    
    print(f"[{metrics['timestamp']}] Health: {health}% | CPU: {metrics['cpu']:.1f}% | Memory: {metrics['memory']:.1f}% | Disk: {metrics['disk']:.1f}% | Alerts: {len(log_entry['alerts'])}")
    
    return log_entry

if __name__ == '__main__':
    print("🚀 Project Lima Monitoring Service Starting...")
    
    # Create logs directory if needed
    import os
    os.makedirs('/home/ec2-user/project_lima/logs', exist_ok=True)
    
    # Single monitoring run (for cron job)
    if len(sys.argv) > 1 and sys.argv[1] == '--single':
        log_monitoring_data()
    else:
        # Continuous monitoring
        print("📊 Continuous monitoring active (Ctrl+C to stop)")
        try:
            while True:
                log_monitoring_data()
                time.sleep(300)  # 5 minutes
        except KeyboardInterrupt:
            print("\n✅ Monitoring service stopped")
