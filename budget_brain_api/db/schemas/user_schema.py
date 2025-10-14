from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str
    display_name: str
    role: Optional[int] = 1  # Default to 'User'

class UserDetailsCreate(BaseModel):
    email: EmailStr
    phone_number: constr(min_length=10, max_length=15)
    aadhar_number: constr(min_length=12, max_length=12)
    pan_number: constr(min_length=10, max_length=10)
    address_line1: Optional[str]
    address_line2: Optional[str]
    city: int
    state: int
    pincode: int
