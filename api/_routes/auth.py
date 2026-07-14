# pyrefly: ignore [missing-import]
from flask import Blueprint
import os
import sys
import logging
# pyrefly: ignore [missing-import]
from flask import jsonify, request

# Removed sys.path modification to avoid ModuleNotFoundError on Vercel

from _services.config import SECRET_KEY, CORS_ORIGINS
from _services.database import get_user_by_username, check_user_credentials
from _services.auth_service import generate_token, verify_token, get_token_from_request

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

auth_bp = Blueprint("auth", __name__)


@auth_bp.route('/api/login', methods=['POST'])
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    try:
        if check_user_credentials(username, password):
            token = generate_token(username)
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'token': token,
                'username': username
            })
        else:
            return jsonify({'error': 'Invalid username or password'}), 401
    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({'error': f"Internal Server Error: {str(e)}"}), 500

@auth_bp.route('/api/logout', methods=['POST'])
@auth_bp.route('/logout', methods=['POST'])
def logout():
    return jsonify({'success': True, 'message': 'Logged out successfully'})

@auth_bp.route('/api/auth/status', methods=['GET'])
@auth_bp.route('/auth/status', methods=['GET'])
def auth_status():
    token = get_token_from_request()
    if not token:
        return jsonify({'logged_in': False})

    payload = verify_token(token)
    if payload:
        return jsonify({
            'logged_in': True,
            'username': payload.get('sub')
        })
    else:
        return jsonify({'logged_in': False})


