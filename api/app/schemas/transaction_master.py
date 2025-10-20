from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class TransactionMasterBase(BaseModel):
    account_id: int
    money_name_id: Optional[int] = None
    amount: float
    description: Optional[str] = None
    transaction_date: datetime
    transaction_type: str  # income, expense, transfer
    payment_method: Optional[str] = None
    tags: Optional[List[str]] = None
    is_recurring: bool = False
    recurring_frequency: Optional[str] = None


class TransactionMasterCreate(TransactionMasterBase):
    pass


class TransactionMasterUpdate(TransactionMasterBase):
    pass


class TransactionMaster(TransactionMasterBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True