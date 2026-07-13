from flask import Blueprint
import os
import sys
import re
from flask import Flask, jsonify
from flask_cors import CORS

# Add the root api directory to the sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _services.config import CORS_ORIGINS
from _services.database import connect_db

health_bp = Blueprint("health", __name__)


@health_bp.route('/api/health', methods=['GET'])
@health_bp.route('/health', methods=['GET'])
def health():
    db_status = "unknown"
    db_error = None
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        conn.close()
        db_status = "connected"
    except Exception as e:
        db_status = "disconnected"
        db_error = str(e)

    return jsonify({
        'status': 'ok' if db_status == 'connected' else 'error',
        'message': 'Backend running successfully',
        'database': db_status,
        'database_error': db_error
    }), 200 if db_status == 'connected' else 500
