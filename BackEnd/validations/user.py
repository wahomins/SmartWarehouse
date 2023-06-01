def validate_create_user_data(data):
    # Check if all required fields for creating a user are present in the data
    required_fields = ['username', 'password', 'full_name', 'role']
    for field in required_fields:
        if field not in data:
            return False, f"Missing field: {field}"
    
    return True, None

def validate_update_user_data(data):
    # Check if all required fields for updating a user are present in the data
    required_fields = ['full_name', 'role']
    for field in required_fields:
        if field not in data:
            return False, f"Missing field: {field}"
    
    return True, None

def validate_login_data(data):
    # Check if all required fields for updating a user are present in the data
    required_fields = ['username', 'password']
    for field in required_fields:
        if field not in data:
            return False, f"Missing field: {field}"
    
    return True, None