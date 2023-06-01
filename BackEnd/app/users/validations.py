from pydantic import BaseModel, EmailStr, validator, ValidationError
from typing import Optional


class CreateUserModel(BaseModel):
    username: Optional[str]
    password: str
    full_name: str
    role: str
    email: EmailStr


class UpdateUserModel(BaseModel):
    username: Optional[str]
    full_name: Optional[str]
    role: Optional[str]


class LoginModel(BaseModel):
    username: str
    password: str
