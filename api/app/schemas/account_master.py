from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AccountMasterBase(BaseModel):
    account_name: str
    account_type: str
    bank_name: Optional[str] = None
    account_number: Optional[str] = None
    balance: float = 0.0
    currency: str = "USD"
    is_active: bool = True


class AccountMasterCreate(AccountMasterBase):
    pass


class AccountMasterUpdate(AccountMasterBase):
    pass


class AccountMaster(AccountMasterBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True