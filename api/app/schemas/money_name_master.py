from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MoneyNameMasterBase(BaseModel):
    name: str
    type: str  # income, expense
    category: Optional[str] = None
    is_default: bool = False


class MoneyNameMasterCreate(MoneyNameMasterBase):
    pass


class MoneyNameMasterUpdate(MoneyNameMasterBase):
    pass


class MoneyNameMaster(MoneyNameMasterBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True