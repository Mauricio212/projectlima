#!/usr/bin/env python3
try:
    from flask import Flask
    print("✅ Flask import successful")
    
    app = Flask(__name__)
    
    @app.route('/')
    def home():
        return "✅ Minimal test working"
    
    @app.route('/test')
    def test():
        return "✅ Test endpoint working"
    
    if __name__ == '__main__':
        print("🚀 Starting minimal test server...")
        app.run(host='0.0.0.0', port=8000, debug=False)
        
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
