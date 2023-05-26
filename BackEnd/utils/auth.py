import jwt
from functools import wraps
from flask import request, jsonify
from datetime import datetime, timedelta

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
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def decode_token(token):
    """
    Decode and verify a JSON Web Token (JWT).
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
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

        # Decode and verify the token
        decoded_token = decode_token(token)

        if not decoded_token:
            return jsonify({'error': 'Invalid token'}), 401

        # Pass the decoded token to the route function
        return f(decoded_token, *args, **kwargs)

    return decorated_function
