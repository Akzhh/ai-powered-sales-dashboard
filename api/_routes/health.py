from flask import Blueprint
import os
import sys
import re
from flask import Flask, jsonify
from flask_cors import CORS

# Add the root api directory to the sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _services.config import CORS_ORIGINS

health_bp = Blueprint("health", __name__)


@health_bp.route('/api/health', methods=['GET'])
@health_bp.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'message': 'Backend running successfully'
    })


