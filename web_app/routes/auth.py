from flask import Blueprint, request, jsonify, session
from services.database import check_user_credentials

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    if check_user_credentials(username, password):
        session['logged_in'] = True
        return jsonify({'success': True, 'message': 'Login successful'})
    else:
        return jsonify({'error': 'Invalid username or password'}), 401


@auth_bp.route('/api/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)
    return jsonify({'success': True, 'message': 'Logged out successfully'})


@auth_bp.route('/api/auth/status', methods=['GET'])
def auth_status():
    return jsonify({'logged_in': session.get('logged_in', False)})
