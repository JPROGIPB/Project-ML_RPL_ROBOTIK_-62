import bcrypt
from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models.user import User


def hash_password(password: str) -> str:
    """Hash password menggunakan bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(password: str, hashed: str) -> bool:
    """Verify password dengan hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


def role_required(*roles):
    """Decorator untuk check role"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            
            if not user or not user.role:
                return jsonify({'error': 'Unauthorized'}), 403
            
            if user.role.role_name not in roles:
                return jsonify({'error': 'Insufficient permissions'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


