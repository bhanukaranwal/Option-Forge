# backend/optionforge/api/utils.py

from functools import wraps
from flask import request, jsonify
from optionforge.models import User

def token_required(f):
    """Decorator to protect routes with JWT authentication."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            # Expected format: "Bearer <token>"
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            user_id = User.decode_auth_token(token)
            if isinstance(user_id, str): # Error string was returned
                return jsonify({'message': user_id}), 401
            
            current_user = User.query.get(user_id)
            if not current_user:
                 return jsonify({'message': 'User not found'}), 401

        except Exception as e:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated
