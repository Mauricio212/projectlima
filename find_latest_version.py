import os
import glob
from datetime import datetime

def find_latest_version():
    # Find all web_app files
    web_app_files = glob.glob("web_app*.py*")
    
    print("🔍 FINDING LATEST VERSION BY DATE:")
    print("="*60)
    
    file_dates = []
    
    for file in web_app_files:
        try:
            # Get modification time
            mod_time = os.path.getmtime(file)
            mod_date = datetime.fromtimestamp(mod_time)
            file_dates.append((file, mod_date, mod_time))
            
            print(f"📅 {mod_date.strftime('%Y-%m-%d %H:%M:%S')} | {file}")
        except:
            print(f"❌ Could not read date for {file}")
    
    # Sort by modification time (newest first)
    file_dates.sort(key=lambda x: x[2], reverse=True)
    
    print("\n" + "="*60)
    print("🏆 NEWEST FILES FIRST:")
    print("="*60)
    
    for i, (file, date, _) in enumerate(file_dates[:5]):
        status = "🥇 NEWEST" if i == 0 else f"#{i+1}"
        print(f"{status} | {date.strftime('%Y-%m-%d %H:%M:%S')} | {file}")
    
    if file_dates:
        newest_file = file_dates[0][0]
        print(f"\n✅ LATEST VERSION: {newest_file}")
        print(f"🚀 Run with: python {newest_file}")
        
        return newest_file
    
    return None

if __name__ == "__main__":
    find_latest_version()
