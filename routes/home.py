from flask import Blueprint

home_bp = Blueprint('home', __name__)

@home_bp.route("/", methods=["GET"])
def index():
    return "Welcome to Project Lima Home Page", 200
