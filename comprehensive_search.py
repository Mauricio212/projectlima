#!/usr/bin/env python3
import subprocess
import os

def comprehensive_search():
    print("🔍 COMPREHENSIVE SEARCH FOR GRID BOT CONFIGURATION")
    print("="*60)
    
    # Search all Python files for Grid bot configuration
    print("1. Searching for 'Configure Grid Bots' text...")
    result = subprocess.run(['grep', '-r', '-l', 'Configure Grid Bots', '/home/ec2-user/', '--include=*.py'], 
                          capture_output=True, text=True, stderr=subprocess.DEVNULL)
    if result.stdout:
        print(f"Found in: {result.stdout}")
    else:
        print("❌ Not found")
    
    print("\n2. Searching for '3Commas Integration' text...")
    result = subprocess.run(['grep', '-r', '-l', '3Commas Integration', '/home/ec2-user/', '--include=*.py'], 
                          capture_output=True, text=True, stderr=subprocess.DEVNULL)
    if result.stdout:
        print(f"Found in: {result.stdout}")
    else:
        print("❌ Not found")
    
    print("\n3. Searching for 'Generic Configurations' text...")
    result = subprocess.run(['grep', '-r', '-l', 'Generic Configurations', '/home/ec2-user/', '--include=*.py'], 
                          capture_output=True, text=True, stderr=subprocess.DEVNULL)
    if result.stdout:
        print(f"Found in: {result.stdout}")
    else:
        print("❌ Not found")
    
    print("\n4. Searching for 'generate3CommasConfig' function...")
    result = subprocess.run(['grep', '-r', '-l', 'generate3CommasConfig', '/home/ec2-user/', '--include=*.py'], 
                          capture_output=True, text=True, stderr=subprocess.DEVNULL)
    if result.stdout:
        print(f"Found in: {result.stdout}")
    
    print("\n5. Listing all web_app files with dates...")
    try:
        os.chdir('/home/ec2-user/project_lima')
        result = subprocess.run(['ls', '-la', 'web_app*'], capture_output=True, text=True)
        print(result.stdout)
    except:
        pass

if __name__ == "__main__":
    comprehensive_search()

