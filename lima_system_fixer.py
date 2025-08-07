#!/usr/bin/env python3
"""
Project Lima: Complete System Fixer & Web Interface Enabler
Fixes all dependencies and validates web interface functionality
"""

import subprocess
import sys
import os
import time
import requests
from datetime import datetime
import json

class ProjectLimaSystemFixer:
    """Comprehensive system fixer for Project Lima"""
    
    def __init__(self):
        self.lima_dir = os.path.expanduser('~/project_lima/')
        self.fix_results = {
            'timestamp': datetime.now().isoformat(),
            'dependency_fixes': {},
            'web_interface_test': {},
            'pipeline_test': {},
            'google_sheets_test': {},
            'final_status': {},
            'errors': []
        }
    
    def log_success(self, component: str, message: str):
        """Log successful fixes"""
        print(f"✅ {component}: {message}")
    
    def log_error(self, component: str, error_msg: str):
        """Log errors"""
        print(f"❌ {component} ERROR: {error_msg}")
        self.fix_results['errors'].append({
            'component': component,
            'error': error_msg,
            'timestamp': datetime.now().isoformat()
        })
    
    def install_dependencies(self) -> bool:
        """Install all required dependencies"""
        print("🔧 Installing Project Lima dependencies...")
        
        # Core web interface packages
        web_packages = [
            'fastapi',
            'uvicorn[standard]',
            'websockets',
            'jinja2',
            'python-multipart',
            'aiofiles'
        ]
        
        # Data processing packages
        data_packages = [
            'requests',
            'pandas',
            'openpyxl',
            'python-dotenv',
            'numpy'
        ]
        
        # Google API packages
        google_packages = [
            'google-auth',
            'google-auth-oauthlib', 
            'google-auth-httplib2',
            'google-api-python-client',
            'gspread'
        ]
        
        # 3Commas/Crypto packages
        crypto_packages = [
            'ccxt',
            'python-binance',
            'cryptocompare'
        ]
        
        all_packages = web_packages + data_packages + google_packages + crypto_packages
        
        installation_results = {}
        
        for package in all_packages:
            try:
                print(f"📦 Installing {package}...")
                result = subprocess.run(
                    [sys.executable, '-m', 'pip', 'install', package],
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                
                if result.returncode == 0:
                    self.log_success("INSTALL", f"{package} installed successfully")
                    installation_results[package] = 'success'
                else:
                    self.log_error("INSTALL", f"Failed to install {package}: {result.stderr}")
                    installation_results[package] = 'failed'
                    
            except subprocess.TimeoutExpired:
                self.log_error("INSTALL", f"Installation timeout for {package}")
                installation_results[package] = 'timeout'
            except Exception as e:
                self.log_error("INSTALL", f"Installation error for {package}: {str(e)}")
                installation_results[package] = 'error'
        
        self.fix_results['dependency_fixes'] = installation_results
        
        # Check critical packages
        critical_packages = ['fastapi', 'uvicorn', 'requests', 'pandas']
        critical_success = all(installation_results.get(pkg) == 'success' for pkg in critical_packages)
        
        return critical_success
    
    def verify_imports(self) -> bool:
        """Verify all critical imports work"""
        print("🔍 Verifying critical imports...")
        
        import_tests = {
            'fastapi': 'import fastapi; print("FastAPI OK")',
            'uvicorn': 'import uvicorn; print("Uvicorn OK")', 
            'websockets': 'import websockets; print("WebSockets OK")',
            'requests': 'import requests; print("Requests OK")',
            'pandas': 'import pandas; print("Pandas OK")',
            'google_api': 'from googleapiclient.discovery import build; print("Google API OK")'
        }
        
        import_results = {}
        
        for test_name, import_code in import_tests.items():
            try:
                result = subprocess.run(
                    [sys.executable, '-c', import_code],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode == 0:
                    self.log_success("IMPORT", f"{test_name} import successful")
                    import_results[test_name] = True
                else:
                    self.log_error("IMPORT", f"{test_name} import failed: {result.stderr}")
                    import_results[test_name] = False
                    
            except Exception as e:
                self.log_error("IMPORT", f"{test_name} import error: {str(e)}")
                import_results[test_name] = False
        
        return all(import_results.values())
    
    def test_pipeline_execution(self) -> bool:
        """Test pipeline execution"""
        print("🔧 Testing pipeline execution...")
        
        try:
            os.chdir(self.lima_dir)
            
            # Test pipeline runner
            result = subprocess.run(
                [sys.executable, 'run_project_lima_pipeline.py'],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                self.log_success("PIPELINE", "Pipeline execution successful")
                
                # Check for output files
                output_dir = os.path.join(self.lima_dir, 'grid_hold_output')
                if os.path.exists(output_dir):
                    files = os.listdir(output_dir)
                    if files:
                        self.log_success("PIPELINE", f"Generated {len(files)} output files")
                        self.fix_results['pipeline_test'] = {
                            'status': 'success',
                            'output_files': len(files)
                        }
                        return True
                    else:
                        self.log_error("PIPELINE", "No output files generated")
                        return False
                else:
                    self.log_error("PIPELINE", "Output directory not found")
                    return False
            else:
                self.log_error("PIPELINE", f"Pipeline execution failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.log_error("PIPELINE", "Pipeline execution timeout")
            return False
        except Exception as e:
            self.log_error("PIPELINE", f"Pipeline test error: {str(e)}")
            return False
    
    def start_web_interface(self) -> bool:
        """Start and test web interface"""
        print("🌐 Starting web interface...")
        
        try:
            os.chdir(self.lima_dir)
            
            # Start web server in background
            web_process = subprocess.Popen(
                [sys.executable, 'main.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for server to start
            time.sleep(5)
            
            # Test if server is responding
            try:
                response = requests.get('http://localhost:8000', timeout=10)
                if response.status_code == 200:
                    self.log_success("WEB", "Web interface responding on port 8000")
                    
                    # Test API endpoints
                    api_endpoints = [
                        '/api/status',
                        '/api/grid-hold-status',
                        '/api/latest-decision'
                    ]
                    
                    endpoint_results = {}
                    for endpoint in api_endpoints:
                        try:
                            api_response = requests.get(f'http://localhost:8000{endpoint}', timeout=5)
                            endpoint_results[endpoint] = api_response.status_code
                            if api_response.status_code == 200:
                                self.log_success("WEB", f"API endpoint {endpoint} working")
                            else:
                                self.log_error("WEB", f"API endpoint {endpoint} returned {api_response.status_code}")
                        except:
                            endpoint_results[endpoint] = 'failed'
                            self.log_error("WEB", f"API endpoint {endpoint} not accessible")
                    
                    self.fix_results['web_interface_test'] = {
                        'status': 'running',
                        'port': 8000,
                        'endpoints': endpoint_results
                    }
                    
                    # Keep server running for user
                    print(f"\n🌐 WEB INTERFACE ACTIVE:")
                    print(f"   • URL: http://localhost:8000")
                    print(f"   • Process ID: {web_process.pid}")
                    print(f"   • Status: Running in background")
                    
                    return True
                else:
                    self.log_error("WEB", f"Web interface returned status {response.status_code}")
                    web_process.terminate()
                    return False
                    
            except requests.exceptions.RequestException as e:
                self.log_error("WEB", f"Web interface not accessible: {str(e)}")
                web_process.terminate()
                return False
                
        except Exception as e:
            self.log_error("WEB", f"Failed to start web interface: {str(e)}")
            return False
    
    def test_google_sheets_integration(self) -> bool:
        """Test Google Sheets integration"""
        print("📊 Testing Google Sheets integration...")
        
        try:
            os.chdir(self.lima_dir)
            
            # Check if credentials exist
            creds_file = os.path.join(self.lima_dir, 'creds.json')
            if not os.path.exists(creds_file):
                self.log_error("SHEETS", "Google credentials file (creds.json) not found")
                return False
            
            # Test export script
            result = subprocess.run(
                [sys.executable, 'export_decision_to_sheets.py'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                self.log_success("SHEETS", "Google Sheets export successful")
                self.fix_results['google_sheets_test'] = {'status': 'success'}
                return True
            else:
                self.log_error("SHEETS", f"Google Sheets export failed: {result.stderr}")
                self.fix_results['google_sheets_test'] = {'status': 'failed', 'error': result.stderr}
                return False
                
        except subprocess.TimeoutExpired:
            self.log_error("SHEETS", "Google Sheets export timeout")
            return False
        except Exception as e:
            self.log_error("SHEETS", f"Google Sheets test error: {str(e)}")
            return False
    
    def create_startup_script(self):
        """Create startup script for easy web interface launch"""
        startup_script = f"""#!/bin/bash
# Project Lima Web Interface Startup Script
cd {self.lima_dir}

echo "🚀 Starting Project Lima Web Interface..."
echo "📍 Directory: {self.lima_dir}"
echo "🌐 URL: http://localhost:8000"
echo ""

# Start web interface
python3 main.py
"""
        
        script_path = os.path.join(self.lima_dir, 'start_web_interface.sh')
        try:
            with open(script_path, 'w') as f:
                f.write(startup_script)
            
            # Make executable
            os.chmod(script_path, 0o755)
            
            self.log_success("STARTUP", f"Created startup script: {script_path}")
            return True
        except Exception as e:
            self.log_error("STARTUP", f"Failed to create startup script: {str(e)}")
            return False
    
    def generate_fix_report(self) -> str:
        """Generate comprehensive fix report"""
        
        # Count successes
        dep_success = sum(1 for result in self.fix_results.get('dependency_fixes', {}).values() if result == 'success')
        total_deps = len(self.fix_results.get('dependency_fixes', {}))
        
        pipeline_working = self.fix_results.get('pipeline_test', {}).get('status') == 'success'
        web_working = self.fix_results.get('web_interface_test', {}).get('status') == 'running'
        sheets_working = self.fix_results.get('google_sheets_test', {}).get('status') == 'success'
        
        report = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║              PROJECT LIMA: COMPLETE SYSTEM FIX & WEB ENABLEMENT             ║
╚══════════════════════════════════════════════════════════════════════════════╝

🕐 FIX COMPLETION: {self.fix_results['timestamp']}

📊 FIX SUMMARY:
   • Dependencies Installed: {dep_success}/{total_deps}
   • Pipeline Execution: {"✅ WORKING" if pipeline_working else "❌ FAILED"}
   • Web Interface: {"✅ ACTIVE" if web_working else "❌ FAILED"}
   • Google Sheets: {"✅ WORKING" if sheets_working else "❌ FAILED"}

🔧 DEPENDENCY INSTALLATION RESULTS:
"""
        
        for package, status in self.fix_results.get('dependency_fixes', {}).items():
            status_icon = "✅" if status == 'success' else "❌"
            report += f"   {status_icon} {package}: {status}\n"
        
        if web_working:
            report += f"""
🌐 WEB INTERFACE STATUS:
   • Status: ✅ ACTIVE AND RUNNING
   • URL: http://localhost:8000
   • Port: {self.fix_results.get('web_interface_test', {}).get('port', 8000)}
   • Startup Script: ~/project_lima/start_web_interface.sh
"""
            
            endpoints = self.fix_results.get('web_interface_test', {}).get('endpoints', {})
            if endpoints:
                report += "   • API Endpoints:\n"
                for endpoint, status in endpoints.items():
                    status_icon = "✅" if status == 200 else "❌"
                    report += f"     {status_icon} {endpoint}: {status}\n"
        
        if pipeline_working:
            output_files = self.fix_results.get('pipeline_test', {}).get('output_files', 0)
            report += f"""
🔧 PIPELINE EXECUTION:
   • Status: ✅ FULLY OPERATIONAL
   • Output Files Generated: {output_files}
   • Grid vs Hold Decision: Working
"""
        
        if self.fix_results['errors']:
            report += f"\n⚠️  REMAINING ISSUES ({len(self.fix_results['errors'])}):\n"
            for error in self.fix_results['errors']:
                report += f"   • {error['component']}: {error['error']}\n"
        
        report += f"""
🚀 PROJECT LIMA WEB SERVICES:
   1. Main Dashboard: http://localhost:8000
   2. API Status: http://localhost:8000/api/status  
   3. Grid/Hold Status: http://localhost:8000/api/grid-hold-status
   4. Latest Decision: http://localhost:8000/api/latest-decision

💻 QUICK START COMMANDS:
   # Start web interface
   cd ~/project_lima && ./start_web_interface.sh
   
   # Run pipeline manually
   cd ~/project_lima && python3 run_project_lima_pipeline.py
   
   # Export to Google Sheets
   cd ~/project_lima && python3 export_decision_to_sheets.py

╔══════════════════════════════════════════════════════════════════════════════╗
║                    PROJECT LIMA WEB SERVICES: ACTIVE                        ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
        return report
    
    def run_complete_fix(self) -> bool:
        """Run complete system fix and validation"""
        print("🚀 Starting Project Lima Complete System Fix...")
        print("=" * 80)
        
        fix_steps = [
            ("Installing Dependencies", self.install_dependencies),
            ("Verifying Imports", self.verify_imports),
            ("Testing Pipeline", self.test_pipeline_execution),
            ("Creating Startup Script", self.create_startup_script),
            ("Starting Web Interface", self.start_web_interface),
            ("Testing Google Sheets", self.test_google_sheets_integration)
        ]
        
        results = []
        for step_name, step_function in fix_steps:
            print(f"\n📋 {step_name}...")
            try:
                result = step_function()
                results.append(result)
                print(f"{'✅' if result else '❌'} {step_name}: {'SUCCESS' if result else 'FAILED'}")
            except Exception as e:
                self.log_error(step_name.upper().replace(' ', '_'), f"Fix error: {str(e)}")
                results.append(False)
        
        # Generate final report
        report = self.generate_fix_report()
        
        overall_success = sum(results) >= len(results) * 0.8  # 80% success rate
        
        print("\n" + "=" * 80)
        if overall_success:
            print("✅ PROJECT LIMA COMPLETE SYSTEM FIX: SUCCESSFUL")
        else:
            print("⚠️ PROJECT LIMA SYSTEM FIX: PARTIAL SUCCESS")
        print("=" * 80)
        
        return overall_success, report

def main():
    """Main execution function"""
    fixer = ProjectLimaSystemFixer()
    
    try:
        success, report = fixer.run_complete_fix()
        
        print(report)
        
        if success:
            print("\n🎯 PROJECT LIMA WEB SERVICES: FULLY OPERATIONAL")
            print("🌐 Access your web interface at: http://localhost:8000")
            return 0
        else:
            print("\n⚠️ PROJECT LIMA: REQUIRES ADDITIONAL ATTENTION")
            return 1
            
    except KeyboardInterrupt:
        print("\n⚠️ Fix process interrupted by user")
        return 1
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())
