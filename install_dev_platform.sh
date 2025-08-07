#!/bin/bash
set -e

echo "🔧 Updating system..."
sudo apt update && sudo apt upgrade -y

echo "📦 Installing system dependencies..."
sudo apt install -y python3-pip python3-venv nginx git curl ufw

echo "🐍 Creating Python virtual environment..."
python3 -m venv ~/devenv
source ~/devenv/bin/activate

echo "🐍 Installing FastAPI backend dependencies..."
pip install --upgrade pip
pip install fastapi uvicorn python-dotenv

echo "📁 Creating project folder..."
mkdir -p ~/project-lima/{backend/frontend,nginx}

echo "📄 Writing FastAPI entrypoint..."
cat <<EOF > ~/project-lima/backend/main.py
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    return "<h1>✅ FastAPI is live from EC2!</h1>"
EOF

echo "🌍 Installing Node.js (via NVM)..."
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
export NVM_DIR="\$HOME/.nvm"
source "\$NVM_DIR/nvm.sh"
nvm install --lts

echo "🧱 Setting up Vite + Bootstrap frontend..."
cd ~/project-lima/frontend
npm create vite@latest . --template vanilla
npm install
npm install bootstrap
echo 'import "bootstrap/dist/css/bootstrap.min.css";' >> src/main.js

echo "🔁 Starting Vite dev server in background..."
nohup npm run dev -- --host 0.0.0.0 > ~/project-lima/frontend/vite.log 2>&1 &

echo "📡 Starting FastAPI server in background..."
cd ~/project-lima/backend
nohup uvicorn main:app --host 0.0.0.0 --port 8000 > ~/project-lima/backend/api.log 2>&1 &

echo "✅ Deployment complete."
echo "🌐 TEST 1: FastAPI → Visit: http://52.200.101.103:8000"
echo "🌐 TEST 2: Vite + Bootstrap → Visit: http://52.200.101.103:5173"
