from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class RefreshTokenBase(BaseModel):
    token: str
    expires_at: datetime
    is_revoked: bool = False


class RefreshTokenCreate(RefreshTokenBase):
    pass


class RefreshTokenUpdate(RefreshTokenBase):
    pass


class RefreshToken(RefreshTokenBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    refresh_token: str