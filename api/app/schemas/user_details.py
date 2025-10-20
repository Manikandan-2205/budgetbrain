from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserDetailsBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    profile_picture: Optional[str] = None


class UserDetailsCreate(UserDetailsBase):
    pass


class UserDetailsUpdate(UserDetailsBase):
    pass


class UserDetails(UserDetailsBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True