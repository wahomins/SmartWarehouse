from pydantic import BaseModel, EmailStr, validator, ValidationError
from typing import Optional


class CreateDeviceModel(BaseModel):
    name: str
    description: str
    mac_address: Optional[str]
    local_ip: Optional[str]


class UpdateDeviceModel(BaseModel):
    name: Optional[str]
    description: Optional[str]
    mac_address: Optional[str]
    local_ip: Optional[str]


class AuthModel(BaseModel):
    device_id: str
    secret: str
