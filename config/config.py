# config/config.py
import os
from dotenv import load_dotenv

# Automatically load environment variables from .env
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(base_dir, ".env"))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default-fallback-secret")
    DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1")
    ENV = os.getenv("FLASK_ENV", "production")
