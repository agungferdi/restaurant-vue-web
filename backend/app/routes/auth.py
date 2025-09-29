from flask import Blueprint, request, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.admin import Admin

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Username and password are required'}), 400
        
        username = data['username']
        password = data['password']
        
        admin = Admin.query.filter_by(username=username).first()
        
        if admin and admin.check_password(password):
            login_user(admin)
            return jsonify({
                'message': 'Login successful',
                'user': admin.to_dict()
            }), 200
        else:
            return jsonify({'error': 'Invalid username or password'}), 401
            
    except Exception as e:
        return jsonify({'error': 'Login failed', 'details': str(e)}), 500

@bp.route('/logout', methods=['POST'])
@login_required
def logout():
    try:
        logout_user()
        return jsonify({'message': 'Logout successful'}), 200
    except Exception as e:
        return jsonify({'error': 'Logout failed', 'details': str(e)}), 500

@bp.route('/me', methods=['GET'])
@login_required
def get_current_user():
    try:
        return jsonify({'user': current_user.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to get user info', 'details': str(e)}), 500

@bp.route('/status', methods=['GET'])
def auth_status():
    """Check if user is authenticated"""
    if current_user.is_authenticated:
        return jsonify({
            'authenticated': True,
            'user': current_user.to_dict()
        }), 200
    else:
        return jsonify({'authenticated': False}), 200