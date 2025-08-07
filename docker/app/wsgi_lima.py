import sys
sys.path.insert(0, '/home/ec2-user/project_lima')

# Import warehouse app
exec(open('web_app_with_warehouse.py').read())

# Add operations route directly
@app.route('/operations')
def operations_center():
    return '''<!DOCTYPE html>
<html><head><title>Project Lima Operations</title></head>
<body style="background:#1a1a1a;color:#fff;font-family:Arial;padding:40px;text-align:center;">
<h1>🚀 PROJECT LIMA OPERATIONS CENTER</h1>
<div style="background:#2d2d2d;padding:30px;border-radius:10px;margin:20px;">
<h2>System Status</h2>
<p>✅ Document Warehouse: ONLINE (20 documents)</p>
<p>❌ Trading Platform: OFFLINE</p>
<p>✅ Database: PRESENT</p>
</div>
<div style="background:#2d2d2d;padding:20px;border-radius:10px;margin:20px;">
<button onclick="location.reload()" style="padding:15px 30px;background:#28a745;color:white;border:none;border-radius:5px;font-size:16px;margin:10px;">🔄 Refresh</button>
<button onclick="window.open('/api/warehouse/list','_blank')" style="padding:15px 30px;background:#007acc;color:white;border:none;border-radius:5px;font-size:16px;margin:10px;">📊 View Warehouse</button>
</div>
</body></html>'''

if __name__ == "__main__":
    app.run(debug=True)
