#!/usr/bin/env python3
import subprocess

def fix_to_port_8080():
    print("🔧 MOVING TO PORT 8080")
    
    # Stop current service
    subprocess.run(["sudo", "systemctl", "stop", "lima-production"])
    
    # Update service to use port 8080
    service_content = '''[Unit]
Description=Project Lima Production Server
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/home/ec2-user/project_lima
Environment=PATH=/home/ec2-user/project_lima/lima_env/bin
ExecStart=/home/ec2-user/project_lima/lima_env/bin/gunicorn --bind 0.0.0.0:8080 --workers 3 --timeout 300 --keep-alive 2 --max-requests 1000 wsgi_lima:app
Restart=always
RestartSec=3
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
'''
    
    with open("/tmp/lima-production.service", "w") as f:
        f.write(service_content)
    
    # Install and start on port 8080
    subprocess.run(["sudo", "mv", "/tmp/lima-production.service", "/etc/systemd/system/"])
    subprocess.run(["sudo", "systemctl", "daemon-reload"])
    subprocess.run(["sudo", "systemctl", "start", "lima-production"])
    
    print("✅ MOVED TO PORT 8080")
    print("🌐 URL: http://52.200.101.103:8080")
    print("📊 Production server with GRID bot configuration")

if __name__ == "__main__":
    fix_to_port_8080()
