import os
import logging
from logging.handlers import RotatingFileHandler

def setup_logging(app):
    log_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'logs')
    os.makedirs(log_dir, exist_ok=True)

    log_path = os.path.join(log_dir, 'app.log')

    file_handler = RotatingFileHandler(log_path, maxBytes=1_000_000, backupCount=5)
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    )
    file_handler.setFormatter(formatter)

    if not app.logger.handlers:
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)

    app.logger.info("✅ Logging initialized.")
