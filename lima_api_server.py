#!/usr/bin/env python3
"""
Project Lima: Simple API Server
Provides basic API endpoints for Grid vs Hold system
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI(title="Project Lima API", version="1.0.0")

# Serve static files if they exist
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    """Main dashboard"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Project Lima - Grid vs Hold Intelligence</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
            .status { background: #e8f5e8; padding: 15px; border-radius: 5px; margin: 20px 0; }
            .api-link { display: inline-block; margin: 10px; padding: 10px 20px; background: #3498db; color: white; text-decoration: none; border-radius: 5px; }
            .api-link:hover { background: #2980b9; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 Project Lima - Grid vs Hold Intelligence Engine</h1>
            
            <div class="status">
                <h3>✅ System Status: Operational</h3>
                <p><strong>Last Updated:</strong> """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
                <p><strong>Web Interface:</strong> Active</p>
                <p><strong>Pipeline:</strong> Ready for execution</p>
            </div>
            
            <h3>🔗 API Endpoints:</h3>
            <a href="/api/status" class="api-link">System Status</a>
            <a href="/api/grid-hold-status" class="api-link">Grid/Hold Status</a>
            <a href="/api/latest-decision" class="api-link">Latest Decision</a>
            <a href="/api/run-pipeline" class="api-link">Run Pipeline</a>
            
            <h3>📊 Grid vs Hold Intelligence:</h3>
            <p>This system analyzes cryptocurrency market data and provides intelligent recommendations for GRID trading vs HOLD strategies based on ROI calculations and market conditions.</p>
            
            <h3>🚀 Quick Actions:</h3>
            <button onclick="runPipeline()" style="padding: 10px 20px; background: #27ae60; color: white; border: none; border-radius: 5px; cursor: pointer;">Run Analysis</button>
            
            <script>
                async function runPipeline() {
                    try {
                        const response = await fetch('/api/run-pipeline');
                        const result = await response.json();
                        alert('Pipeline Status: ' + result.status + '\n' + result.message);
                    } catch (error) {
                        alert('Error: ' + error.message);
                    }
                }
            </script>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/api/status")
async def get_api_status():
    """Get API status"""
    return {
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "services": {
            "pipeline": "active",
            "grid_hold_engine": "operational", 
            "web_interface": "running"
        }
    }

@app.get("/api/grid-hold-status")
async def get_grid_hold_status():
    """Get current Grid vs Hold status"""
    try:
        output_dir = "grid_hold_output"
        decision_files = []
        
        if os.path.exists(output_dir):
            files = os.listdir(output_dir)
            decision_files = [f for f in files if "decision" in f.lower() or "step_3_3" in f or "selected" in f]
        
        logs_dir = "logs"
        latest_log = None
        if os.path.exists(logs_dir):
            log_files = [f for f in os.listdir(logs_dir) if f.endswith('.csv') or f.endswith('.log')]
            if log_files:
                latest_log = sorted(log_files)[-1]
        
        return {
            "status": "operational",
            "last_execution": datetime.now().isoformat(),
            "decision_files": len(decision_files),
            "latest_log": latest_log,
            "output_directory": output_dir,
            "total_output_files": len(os.listdir(output_dir)) if os.path.exists(output_dir) else 0
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.get("/api/latest-decision") 
async def get_latest_decision():
    """Get latest Grid vs Hold decision"""
    try:
        output_dir = "grid_hold_output"
        decision_data = {
            "decision": "No recent decision found",
            "timestamp": None,
            "files_available": []
        }
        
        if os.path.exists(output_dir):
            files = os.listdir(output_dir)
            csv_files = [f for f in files if f.endswith('.csv')]
            decision_data["files_available"] = len(csv_files)
            
            # Look for latest files
            if csv_files:
                latest_file = sorted(csv_files)[-1]
                file_path = os.path.join(output_dir, latest_file)
                
                decision_data.update({
                    "decision": "Analysis data available",
                    "timestamp": datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat(),
                    "latest_file": latest_file,
                    "status": "Data ready for analysis"
                })
        
        return decision_data
        
    except Exception as e:
        return {
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.get("/api/run-pipeline")
async def run_pipeline():
    """Trigger pipeline execution"""
    try:
        result = subprocess.run(
            [sys.executable, "run_project_lima_pipeline.py"],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            return {
                "status": "success",
                "message": "Pipeline executed successfully",
                "timestamp": datetime.now().isoformat(),
                "output": result.stdout[:500] if result.stdout else "Execution completed"
            }
        else:
            return {
                "status": "error",
                "message": "Pipeline execution failed", 
                "error": result.stderr[:500] if result.stderr else "Unknown error",
                "timestamp": datetime.now().isoformat()
            }
            
    except subprocess.TimeoutExpired:
        return {
            "status": "timeout",
            "message": "Pipeline execution timed out",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

if __name__ == "__main__":
    print("🚀 Starting Project Lima API Server...")
    print("🌐 Web Interface: http://localhost:8000")
    print("📊 API Documentation: http://localhost:8000/docs")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
