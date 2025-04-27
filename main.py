from flask import Flask, jsonify
from routes import home_bp, ssti_bp, ssto_bp

app = Flask(__name__)
app.register_blueprint(home_bp)
app.register_blueprint(ssti_bp)
app.register_blueprint(ssto_bp)

@app.route("/debug/ping", methods=["GET"])
def ping():
    return jsonify({"status": "ok"}), 200

@app.route("/debug/routes", methods=["GET"])
def list_routes():
    return jsonify([str(rule) for rule in app.url_map.iter_rules()])

@app.route("/", methods=["GET"])
def index():
    return "Lima Flask App is running.", 200
