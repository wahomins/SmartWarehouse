def validate_create_device_data(data):
    required_fields = ['name', 'deviceId', 'description']
    
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
    
    return True, None


def validate_update_device_data(data):
    if not data:
        return False, "No data provided for update"
    
    return True, None
