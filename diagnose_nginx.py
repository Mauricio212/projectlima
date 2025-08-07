#!/usr/bin/env python3
import subprocess

def diagnose_nginx():
    print("🔍 NGINX DIAGNOSIS")
    print("="*50)
    
    # Test 1: Check localhost connection
    print("1. Testing localhost connection...")
    try:
        result = subprocess.run(["curl", "-I", "http://localhost:8000"], 
                              capture_output=True, text=True, timeout=10)
        print(f"Status: {result.returncode}")
        print(f"Output: {result.stdout}")
        if result.stderr:
            print(f"Error: {result.stderr}")
    except Exception as e:
        print(f"Curl failed: {e}")
    
    print("\n" + "="*50)
    
    # Test 2: Check nginx config
    print("2. Testing nginx configuration...")
    try:
        result = subprocess.run(["sudo", "nginx", "-t"], 
                              capture_output=True, text=True)
        print(f"Status: {result.returncode}")
        print(f"Output: {result.stdout}")
        if result.stderr:
            print(f"Error: {result.stderr}")
    except Exception as e:
        print(f"Nginx test failed: {e}")
    
    print("\n" + "="*50)
    
    # Test 3: Check nginx status
    print("3. Checking nginx service status...")
    try:
        result = subprocess.run(["sudo", "systemctl", "status", "nginx"], 
                              capture_output=True, text=True)
        print(f"Status: {result.returncode}")
        print(f"Output: {result.stdout}")
    except Exception as e:
        print(f"Nginx status failed: {e}")

if __name__ == "__main__":
    diagnose_nginx()
