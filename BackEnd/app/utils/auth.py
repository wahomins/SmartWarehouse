import jwt
from functools import wraps
from flask import request, jsonify, current_app
from werkzeug.local import LocalProxy
from datetime import datetime, timedelta

logger = LocalProxy(lambda: current_app.logger)
# Secret key for JWT
SECRET_KEY = "your_secret_key"


def generate_token(user_id, email, full_name):
    """
    Generate a JSON Web Token (JWT) for authentication.
    """
    payload = {
        'user_id': str(user_id),
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
            logger.debug(f'{token_}')
            # Decode and verify the token
            decoded_token = decode_token(token_)
            logger.debug(f'{decoded_token}')
            if not decoded_token:
                return jsonify({'error': 'Invalid token'}), 401

            # Pass the decoded token to the route function
            return f(decoded_token, *args, **kwargs)
        else:
            return jsonify({'error': 'Missing token'}), 401

    return decorated_function
