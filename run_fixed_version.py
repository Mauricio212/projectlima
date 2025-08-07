import re

def run_fixed_version_on_different_port():
    # Read the fixed version
    with open("web_app_professional_fixed.py", "r") as f:
        content = f.read()
    
    # Change port from 8000 to 8002
    content = re.sub(r'port=8000', 'port=8002', content)
    content = re.sub(r'host="0\.0\.0\.0", port=8000', 'host="0.0.0.0", port=8002', content)
    content = re.sub(r':8000', ':8002', content)
    
    # Write to new file
    with open("web_app_professional_fixed_port8002.py", "w") as f:
        f.write(content)
    
    print("✅ Fixed version ready on port 8002")
    print("🚀 Starting: python web_app_professional_fixed_port8002.py")
    
    import os
    os.system("python web_app_professional_fixed_port8002.py")

if __name__ == "__main__":
    run_fixed_version_on_different_port()
