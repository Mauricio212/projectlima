#!/bin/bash
# Project Lima Web Interface Startup Script (Updated)
cd /home/ec2-user/project_lima/

echo "🚀 Starting Project Lima Web Interface..."
echo "📍 Directory: /home/ec2-user/project_lima/"
echo "🌐 URL: http://localhost:8000"
echo "📊 API Docs: http://localhost:8000/docs"
echo ""

# Try simple API server first, fallback to main.py
if [ -f "lima_api_server.py" ]; then
    echo "Using Project Lima API Server..."
    python3 lima_api_server.py
else
    echo "Using main.py..."
    python3 main.py
fi
