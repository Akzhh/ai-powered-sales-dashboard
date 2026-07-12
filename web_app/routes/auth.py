from flask import Blueprint, request, jsonify
from services.database import get_user_by_username, check_user_credentials
from services.auth_service import generate_token, verify_token, get_token_from_request

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/api/login', methods=['POST'])
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


@auth_bp.route('/api/logout', methods=['POST'])
def logout():
    # Stateless JWT — logout is handled client-side by discarding the token
    return jsonify({'success': True, 'message': 'Logged out successfully'})


@auth_bp.route('/api/auth/status', methods=['GET'])
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
