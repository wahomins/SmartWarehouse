from flask import request, jsonify


def validate_request(schema):
    def decorator(func):
        def wrapper(*args, **kwargs):
            data = request.get_json()

            try:
                schema.validate(data)
            except Exception as e:
                return jsonify({'error': str(e)}), 400

            return func(*args, **kwargs)

        return wrapper

    return decorator
