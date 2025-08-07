#!/bin/bash
# PROJECT LIMA - Port 80 Setup Script
echo "🌐 PROJECT LIMA - Setting up Port 80 routing..."

# Update system and install nginx
sudo yum update -y
sudo yum install nginx -y
sudo systemctl stop nginx

# Create nginx configuration
sudo tee /etc/nginx/nginx.conf > /dev/null << 'NGINXEOF'
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /run/nginx.pid;

events {
    worker_connections 1024;
}

http {
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                   '$status $body_bytes_sent "$http_referer" '
                   '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 4096;
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    server {
        listen 80;
        server_name 52.200.101.103;
        
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header X-Content-Type-Options "nosniff" always;
        
        location / {
            proxy_pass http://127.0.0.1:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_buffering off;
            proxy_redirect off;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }
        
        location /static/ {
            proxy_pass http://127.0.0.1:8000;
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
        
        location /api/ {
            proxy_pass http://127.0.0.1:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
}
NGINXEOF

# Test and start nginx
sudo nginx -t
if [ $? -eq 0 ]; then
    sudo systemctl start nginx
    sudo systemctl enable nginx
    sudo firewall-cmd --permanent --add-service=http
    sudo firewall-cmd --reload
    echo "🎉 SUCCESS! Platform accessible at: http://52.200.101.103"
else
    echo "❌ Nginx configuration error"
fi
