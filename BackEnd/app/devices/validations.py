from pydantic import BaseModel, EmailStr, validator, ValidationError
from typing import Optional


class CreateDeviceModel(BaseModel):
    name: str
    description: str
    mac_address: Optional[str]
    local_ip: Optional[str]
    warehouse_id: Optional[str]
    output_device_id: Optional[str]
    device_group: Optional[str]
    device_sub_group: Optional[str]
    active: Optional[str]

    class Config:
        validate_assignment = True

    @validator('active')
    def set_param_active(cls):
        return "False"
    
    @validator('device_group')
    def set_param_group(cls, device_group):
        return device_group or 'unknown'
    
    @validator('device_sub_group')
    def set_param_sub_group(cls, device_group):
        return device_group or 'unknown'


class UpdateDeviceModel(BaseModel):
    name: Optional[str]
    description: Optional[str]
    mac_address: Optional[str]
    local_ip: Optional[str]
    device_group: Optional[str]
    warehouse_id: Optional[str]


class AuthModel(BaseModel):
    device_id: str
    secret: str
