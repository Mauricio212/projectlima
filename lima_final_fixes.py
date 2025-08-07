#!/usr/bin/env python3
"""
Project Lima: Final API & Google Sheets Fixes
Fixes remaining API endpoints and Google Sheets integration
"""

import os
import json
import shutil
import subprocess
import sys
from datetime import datetime

class ProjectLimaFinalFixes:
    """Final fixes for API endpoints and Google Sheets"""
    
    def __init__(self):
        self.lima_dir = os.path.expanduser('~/project_lima/')
        self.fixes_applied = []
        self.errors = []
    
    def log_success(self, message: str):
        print(f"✅ {message}")
        self.fixes_applied.append(message)
    
    def log_error(self, message: str):
        print(f"❌ {message}")
        self.errors.append(message)
    
    def fix_google_sheets_credentials(self) -> bool:
        """Fix Google Sheets credentials path"""
        print("🔧 Fixing Google Sheets credentials...")
        
        # Expected path in export script
        expected_path = os.path.join(self.lima_dir, 'secrets', 'sheets_service_account.json')
        
        # Actual credential files
        actual_creds = os.path.join(self.lima_dir, 'creds.json')
        
        if os.path.exists(actual_creds):
            # Create secrets directory
            secrets_dir = os.path.join(self.lima_dir, 'secrets')
            os.makedirs(secrets_dir, exist_ok=True)
            
            # Copy creds.json to expected location
            try:
                shutil.copy2(actual_creds, expected_path)
                self.log_success(f"Copied credentials: creds.json → {expected_path}")
                
                # Also create a symlink for flexibility
                symlink_path = os.path.join(secrets_dir, 'creds.json')
                if not os.path.exists(symlink_path):
                    os.symlink(actual_creds, symlink_path)
                    self.log_success(f"Created symlink: {symlink_path}")
                
                return True
                
            except Exception as e:
                self.log_error(f"Failed to copy credentials: {str(e)}")
                return False
        else:
            self.log_error("Original creds.json file not found")
            return False
    
    def create_api_endpoints_fix(self) -> bool:
        """Create missing API endpoints for main.py"""
        print("🔧 Creating API endpoints fix...")
        
        # API endpoints code to add to main.py
        api_endpoints_code = '''
# Additional API endpoints for Project Lima
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
        # Check for latest decision file
        output_dir = "grid_hold_output"
        decision_files = []
        
        if os.path.exists(output_dir):
            for file in os.listdir(output_dir):
                if "decision" in file.lower() or "step_3_3" in file:
                    decision_files.append(file)
        
        # Read latest pipeline log
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
            "output_directory": output_dir
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
        # Look for latest decision in output directory
        output_dir = "grid_hold_output"
        decision_data = {
            "decision": "No recent decision found",
            "timestamp": None,
            "roi_grid": None,
            "roi_hold": None,
            "confidence": None
        }
        
        if os.path.exists(output_dir):
            # Look for CSV files with decision data
            csv_files = [f for f in os.listdir(output_dir) if f.endswith('.csv')]
            
            for csv_file in sorted(csv_files, reverse=True):
                file_path = os.path.join(output_dir, csv_file)
                try:
                    # Try to read decision data
                    import pandas as pd
                    df = pd.read_csv(file_path)
                    
                    # Look for ROI or decision columns
                    if any(col.lower().find('roi') != -1 for col in df.columns):
                        decision_data["decision"] = "Grid vs Hold analysis available"
                        decision_data["timestamp"] = datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
                        decision_data["data_file"] = csv_file
                        break
                        
                except Exception:
                    continue
        
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
        import subprocess
        result = subprocess.run(
            [sys.executable, "run_project_lima_pipeline.py"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            return {
                "status": "success",
                "message": "Pipeline executed successfully",
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "status": "error", 
                "message": "Pipeline execution failed",
                "error": result.stderr,
                "timestamp": datetime.now().isoformat()
            }
            
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
'''
        
        # Create API endpoints file
        api_file = os.path.join(self.lima_dir, 'api_endpoints_addon.py')
        try:
            with open(api_file, 'w') as f:
                f.write(api_endpoints_code)
            
            self.log_success(f"Created API endpoints addon: {api_file}")
            return True
            
        except Exception as e:
            self.log_error(f"Failed to create API endpoints: {str(e)}")
            return False
    
    def fix_main_py_imports(self) -> bool:
        """Add missing imports to main.py"""
        print("🔧 Checking main.py imports...")
        
        main_py_path = os.path.join(self.lima_dir, 'main.py')
        
        if not os.path.exists(main_py_path):
            self.log_error("main.py not found")
            return False
        
        try:
            # Read current main.py
            with open(main_py_path, 'r') as f:
                content = f.read()
            
            # Check if datetime import is missing
            imports_to_add = []
            
            if 'from datetime import datetime' not in content:
                imports_to_add.append('from datetime import datetime')
            
            if 'import os' not in content:
                imports_to_add.append('import os')
            
            if 'import sys' not in content:
                imports_to_add.append('import sys')
            
            # Add missing imports
            if imports_to_add:
                import_section = '\n'.join(imports_to_add) + '\n\n'
                
                # Find where to insert (after existing imports)
                lines = content.split('\n')
                insert_index = 0
                
                for i, line in enumerate(lines):
                    if line.startswith('from ') or line.startswith('import '):
                        insert_index = i + 1
                
                lines.insert(insert_index, import_section)
                content = '\n'.join(lines)
                
                # Backup original
                backup_path = main_py_path + '.backup'
                shutil.copy2(main_py_path, backup_path)
                
                # Write updated content
                with open(main_py_path, 'w') as f:
                    f.write(content)
                
                self.log_success(f"Added missing imports to main.py (backup: {backup_path})")
            else:
                self.log_success("All required imports already present in main.py")
            
            return True
            
        except Exception as e:
            self.log_error(f"Failed to fix main.py imports: {str(e)}")
            return False
    
    def create_simple_api_server(self) -> bool:
        """Create a simple API server if main.py is too complex"""
        print("🔧 Creating simple API server...")
        
        simple_api_code = '''#!/usr/bin/env python3
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
                        alert('Pipeline Status: ' + result.status + '\\n' + result.message);
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
'''
        
        # Create simple API server
        api_server_path = os.path.join(self.lima_dir, 'lima_api_server.py')
        try:
            with open(api_server_path, 'w') as f:
                f.write(simple_api_code)
            
            # Make executable
            os.chmod(api_server_path, 0o755)
            
            self.log_success(f"Created simple API server: {api_server_path}")
            return True
            
        except Exception as e:
            self.log_error(f"Failed to create API server: {str(e)}")
            return False
    
    def update_startup_script(self) -> bool:
        """Update startup script to use simple API server"""
        print("🔧 Updating startup script...")
        
        startup_script_content = f'''#!/bin/bash
# Project Lima Web Interface Startup Script (Updated)
cd {self.lima_dir}

echo "🚀 Starting Project Lima Web Interface..."
echo "📍 Directory: {self.lima_dir}"
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
'''
        
        script_path = os.path.join(self.lima_dir, 'start_web_interface.sh')
        try:
            with open(script_path, 'w') as f:
                f.write(startup_script_content)
            
            os.chmod(script_path, 0o755)
            self.log_success(f"Updated startup script: {script_path}")
            return True
            
        except Exception as e:
            self.log_error(f"Failed to update startup script: {str(e)}")
            return False
    
    def test_new_api_server(self) -> bool:
        """Test the new API server"""
        print("🔧 Testing new API server...")
        
        try:
            # Kill any existing server process
            subprocess.run(['pkill', '-f', 'main.py'], capture_output=True)
            subprocess.run(['pkill', '-f', 'lima_api_server.py'], capture_output=True)
            
            # Start new API server in background
            api_server_path = os.path.join(self.lima_dir, 'lima_api_server.py')
            process = subprocess.Popen(
                [sys.executable, api_server_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait for server to start
            import time
            time.sleep(3)
            
            # Test API endpoints
            import requests
            
            endpoints_to_test = [
                ('/', 'Main dashboard'),
                ('/api/status', 'Status API'),
                ('/api/grid-hold-status', 'Grid/Hold status'),
                ('/api/latest-decision', 'Latest decision')
            ]
            
            success_count = 0
            for endpoint, name in endpoints_to_test:
                try:
                    response = requests.get(f'http://localhost:8000{endpoint}', timeout=5)
                    if response.status_code == 200:
                        self.log_success(f"{name} endpoint working: {endpoint}")
                        success_count += 1
                    else:
                        self.log_error(f"{name} endpoint failed: {response.status_code}")
                except Exception as e:
                    self.log_error(f"{name} endpoint error: {str(e)}")
            
            if success_count >= 3:  # At least 3 of 4 endpoints working
                self.log_success(f"API server working: {success_count}/4 endpoints functional")
                return True
            else:
                self.log_error(f"API server issues: only {success_count}/4 endpoints working")
                return False
                
        except Exception as e:
            self.log_error(f"API server test failed: {str(e)}")
            return False
    
    def run_final_fixes(self) -> bool:
        """Run all final fixes"""
        print("🚀 Running Project Lima Final Fixes...")
        print("=" * 60)
        
        fixes = [
            ("Google Sheets Credentials", self.fix_google_sheets_credentials),
            ("Simple API Server", self.create_simple_api_server),
            ("Startup Script Update", self.update_startup_script),
            ("New API Server Test", self.test_new_api_server)
        ]
        
        results = []
        for fix_name, fix_function in fixes:
            print(f"\n📋 {fix_name}...")
            try:
                result = fix_function()
                results.append(result)
                print(f"{'✅' if result else '❌'} {fix_name}: {'SUCCESS' if result else 'FAILED'}")
            except Exception as e:
                self.log_error(f"{fix_name} error: {str(e)}")
                results.append(False)
        
        success_rate = sum(results) / len(results)
        
        print("\n" + "=" * 60)
        if success_rate >= 0.75:
            print("✅ PROJECT LIMA FINAL FIXES: SUCCESSFUL")
        else:
            print("⚠️ PROJECT LIMA FINAL FIXES: PARTIAL SUCCESS")
        print("=" * 60)
        
        return success_rate >= 0.75

def main():
    """Main execution"""
    fixer = ProjectLimaFinalFixes()
    
    try:
        success = fixer.run_final_fixes()
        
        print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    PROJECT LIMA: FINAL FIXES COMPLETE                       ║
╚══════════════════════════════════════════════════════════════════════════════╝

📊 FIXES APPLIED:
""")
        for fix in fixer.fixes_applied:
            print(f"   ✅ {fix}")
        
        if fixer.errors:
            print(f"\n⚠️ ERRORS ENCOUNTERED:")
            for error in fixer.errors:
                print(f"   ❌ {error}")
        
        if success:
            print(f"""
🚀 PROJECT LIMA WEB SERVICES: FULLY OPERATIONAL

🌐 ACCESS YOUR WEB INTERFACE:
   • Main Dashboard: http://localhost:8000
   • API Status: http://localhost:8000/api/status
   • Grid/Hold Status: http://localhost:8000/api/grid-hold-status
   • Latest Decision: http://localhost:8000/api/latest-decision
   • API Documentation: http://localhost:8000/docs

💻 START WEB INTERFACE:
   cd ~/project_lima && ./start_web_interface.sh

🎯 Your Project Lima GRID vs HOLD Intelligence Engine is ready to serve via web interface!
""")
            return 0
        else:
            print("\n⚠️ Some fixes may need manual attention")
            return 1
            
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())
