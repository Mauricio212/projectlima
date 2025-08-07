#!/usr/bin/env python3

def check_grid_config():
    print("🔍 CHECKING GRID BOT CONFIGURATION")
    
    try:
        with open("web_app_professional_secured.py.modal_backup", "r") as f:
            content = f.read()
        
        # Search for Grid-related content
        if "Configure Grid" in content:
            print("✅ Found 'Configure Grid' text")
        else:
            print("❌ No 'Configure Grid' text found")
        
        if "3Commas" in content:
            print("✅ Found '3Commas' text")
        else:
            print("❌ No '3Commas' text found")
        
        if "Generic" in content:
            print("✅ Found 'Generic' text")
        else:
            print("❌ No 'Generic' text found")
        
        # Look for button text
        import re
        buttons = re.findall(r'<button[^>]*>([^<]+)</button>', content, re.IGNORECASE)
        print(f"\n📋 Buttons found: {buttons[:10]}")  # First 10 buttons
        
        # Look for modal content
        modals = re.findall(r'modal[^"\']*["\']([^"\']*)', content, re.IGNORECASE)
        print(f"\n🪟 Modal references: {modals[:5]}")  # First 5 modal refs
        
    except Exception as e:
        print(f"❌ Error reading file: {e}")
    
    print("\n🔧 Current button text in live site - check browser")

if __name__ == "__main__":
    check_grid_config()

