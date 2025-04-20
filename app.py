from flask import Flask
from routes import register_routes
from config.config import Config
from utils.logger import setup_logging

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    register_routes(app)
    setup_logging(app)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=app.config["DEBUG"])
