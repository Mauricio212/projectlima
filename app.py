from flask import Flask
from routes.ssti import ssti_bp
from routes.ssto import ssto_bp

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(ssti_bp)
app.register_blueprint(ssto_bp, url_prefix='/ssto')

@app.route('/')
def index():
    return '✅ Lima Project is running', 200

# Main execution
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
