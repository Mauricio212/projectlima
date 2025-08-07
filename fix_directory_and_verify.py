import os
import re

def fix_directory_and_verify():
    # Check current directory
    current_dir = os.getcwd()
    print(f"📍 Current directory: {current_dir}")
    
    # Check if we're in the right place
    if "project-lima" not in current_dir:
        print("❌ Wrong directory!")
        print("🔧 Change to correct directory:")
        print("cd ../project-lima")
        return
    
    # Verify files exist
    required_files = ["lima_backend.py", "working_grid_website.py"]
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
        else:
            print(f"✅ Found: {file}")
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        print("🔧 Run setup_dual_websites.py first")
        return
    
    print("✅ All files present - ready for verification")
    print("🚀 Now run: python verify_dual_site_safety.py")

if __name__ == "__main__":
    fix_directory_and_verify()
