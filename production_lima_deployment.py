#!/usr/bin/env python3
import subprocess
import os
import sys

def deploy_production_lima():
    print("🏭 PRODUCTION-GRADE PROJECT LIMA DEPLOYMENT")
    print("🔧 Installing production components...")
    
    # Step 1: Install production dependencies
    subprocess.run([sys.executable, "-m", "pip", "install", "gunicorn"], check=True)
    subprocess.run(["sudo", "yum", "install", "-y", "nginx"], check=True)
    
    # Step 2: Kill existing development servers
    subprocess.run(["pkill", "-f", "flask"], stderr=subprocess.DEVNULL)
    subprocess.run(["pkill", "-f", "web_app"], stderr=subprocess.DEVNULL)
    
    # Step 3: Create production WSGI entry point
    wsgi_content = '''#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, '/home/ec2-user/project_lima')

# Import the modal backup version (working GRID bot config)
exec(open('web_app_professional_secured.py.modal_backup').read())

if __name__ == "__main__":
    app.run()
'''
    
    with open("wsgi_lima.py", "w") as f:
        f.write(wsgi_content)
    
    # Step 4: Create systemd service file
    service_content = '''[Unit]
Description=Project Lima Production Server
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/home/ec2-user/project_lima
Environment=PATH=/home/ec2-user/project_lima/lima_env/bin
ExecStart=/home/ec2-user/project_lima/lima_env/bin/gunicorn --bind 127.0.0.1:8000 --workers 3 --timeout 300 --keep-alive 2 --max-requests 1000 wsgi_lima:app
Restart=always
RestartSec=3
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
'''
    
    # Write service file
    with open("/tmp/lima-production.service", "w") as f:
        f.write(service_content)
    
    # Step 5: Install and configure systemd service
    subprocess.run(["sudo", "mv", "/tmp/lima-production.service", "/etc/systemd/system/"], check=True)
    subprocess.run(["sudo", "systemctl", "daemon-reload"], check=True)
    subprocess.run(["sudo", "systemctl", "enable", "lima-production"], check=True)
    
    # Step 6: Configure Nginx reverse proxy
    nginx_config = '''server {
    listen 8000;
    server_name 52.200.101.103;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }
}'''
    
    with open("/tmp/lima.conf", "w") as f:
        f.write(nginx_config)
    
    subprocess.run(["sudo", "mv", "/tmp/lima.conf", "/etc/nginx/conf.d/"], check=True)
    subprocess.run(["sudo", "systemctl", "enable", "nginx"], check=True)
    subprocess.run(["sudo", "systemctl", "restart", "nginx"], check=True)
    
    # Step 7: Start production services
    subprocess.run(["sudo", "systemctl", "start", "lima-production"], check=True)
    
    print("✅ PRODUCTION DEPLOYMENT COMPLETE")
    print("🌐 URL: http://52.200.101.103:8000")
    print("🔧 Auto-restart: ENABLED")
    print("📊 Status: sudo systemctl status lima-production")
    print("📋 Logs: sudo journalctl -u lima-production -f")
    
    # Verify deployment
    import time
    time.sleep(5)
    result = subprocess.run(["sudo", "systemctl", "is-active", "lima-production"], 
                          capture_output=True, text=True)
    
    if result.stdout.strip() == "active":
        print("🏆 PRODUCTION SERVER: ACTIVE AND STABLE")
    else:
        print("❌ DEPLOYMENT FAILED")
        subprocess.run(["sudo", "journalctl", "-u", "lima-production", "--no-pager", "-l"])

if __name__ == "__main__":
    deploy_production_lima()

