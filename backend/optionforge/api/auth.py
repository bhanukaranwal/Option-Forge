# backend/optionforge/api/auth.py

from flask import request, jsonify
from . import api_bp
from optionforge.models import User
from optionforge import db

@api_bp.route('/auth/register', methods=['POST'])
def register():
    """Registers a new user."""
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Email and password are required'}), 400

    user = User.query.filter_by(email=data['email']).first()
    if user:
        return jsonify({'message': 'User already exists'}), 400

    try:
        new_user = User(email=data['email'], password=data['password'])
        db.session.add(new_user)
        db.session.commit()
        auth_token = new_user.encode_auth_token()
        response = {
            'status': 'success',
            'message': 'Successfully registered.',
            'auth_token': auth_token
        }
        return jsonify(response), 201
    except Exception as e:
        response = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return jsonify(response), 401


@api_bp.route('/auth/login', methods=['POST'])
def login():
    """Logs in a user and returns an auth token."""
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Email and password are required'}), 400

    try:
        user = User.query.filter_by(email=data.get('email')).first()
        if user and user.check_password(data.get('password')):
            auth_token = user.encode_auth_token()
            if auth_token:
                response = {
                    'status': 'success',
                    'message': 'Successfully logged in.',
                    'auth_token': auth_token
                }
                return jsonify(response), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 404
    except Exception as e:
        return jsonify({'message': 'Login failed. Please try again.'}), 500
