# routes/ssti.py

from flask import Blueprint, request, jsonify

ssti_bp = Blueprint('ssti', __name__)

@ssti_bp.route('/ssti/test', methods=['GET'])
def test_ssti():
    return '✅ SSTI is working', 200
