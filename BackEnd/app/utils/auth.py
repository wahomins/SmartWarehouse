import jwt
from functools import wraps
from flask import request, jsonify, current_app
from werkzeug.local import LocalProxy
from datetime import datetime, timedelta

logger = LocalProxy(lambda: current_app.logger)
# Secret key for JWT
SECRET_KEY = "your_secret_key"


def generate_token(user_id, email, full_name, role):
    """
    Generate a JSON Web Token (JWT) for authentication.
    """
    payload = {
        'user_id': str(user_id),
        'role': str(role),
        'email': email,
        'full_name': full_name,
        'exp': datetime.utcnow() + timedelta(hours=1)  # Token expiration time (1 hour)
    }
    token = jwt.encode(payload=payload, key=SECRET_KEY)
    return token

def generate_device_token(device_id, name):
    """
    Generate a JSON Web Token (JWT) for authentication.
    """
    payload = {
        'device_id': str(device_id),
        'name': name,
        'exp': datetime.utcnow() + timedelta(hours=1)  # Token expiration time (1 hour)
    }
    token = jwt.encode(payload=payload, key=SECRET_KEY)
    return token


def decode_token(token):
    """
    Decode and verify a JSON Web Token (JWT).
    """
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=['HS256', ])
        return payload
    except jwt.ExpiredSignatureError:
        # Token has expired
        return None
    except jwt.InvalidTokenError:
        # Token is invalid
        return None


def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Extract the token from the request headers
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Missing token'}), 401

        # Split the header value by whitespace
        parts = token.split()

        # Check if the header value has the expected format
        if len(parts) == 2 and parts[0].lower() == 'bearer':
            # Extract the token from the header
            token_ = parts[1]
            # Decode and verify the token
            decoded_token = decode_token(token_)
            if not decoded_token:
                return jsonify({'error': 'Invalid token'}), 401

            # Pass the decoded token to the route function
            return f(decoded_token, *args, **kwargs)
        else:
            return jsonify({'error': 'Missing token'}), 401

    return decorated_function

def authorize_role(roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            decoded_token = args[0]
            user_role = decoded_token.get('role')

            if user_role in roles:
                return func(*args, **kwargs)
            else:
                return jsonify({'message': 'Unauthorized. Insufficient role permissions.'}), 403

        return wrapper

    return decorator