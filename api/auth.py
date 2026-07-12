import os
import sys
import re
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS

# Add the root api directory to the sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.config import SECRET_KEY, CORS_ORIGINS
from services.database import get_user_by_username, check_user_credentials
from services.auth_service import generate_token, verify_token, get_token_from_request

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Enable CORS
CORS(app, supports_credentials=True, origins=CORS_ORIGINS)

@app.route('/api/login', methods=['POST'])
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

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

@app.route('/api/logout', methods=['POST'])
@app.route('/logout', methods=['POST'])
def logout():
    return jsonify({'success': True, 'message': 'Logged out successfully'})

@app.route('/api/auth/status', methods=['GET'])
@app.route('/auth/status', methods=['GET'])
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

if __name__ == '__main__':
    app.run(debug=True, port=5000)
