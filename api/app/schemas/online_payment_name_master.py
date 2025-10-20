from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class OnlinePaymentNameMasterBase(BaseModel):
    payment_name: str
    provider: Optional[str] = None
    account_email: Optional[str] = None
    is_active: bool = True


class OnlinePaymentNameMasterCreate(OnlinePaymentNameMasterBase):
    pass


class OnlinePaymentNameMasterUpdate(OnlinePaymentNameMasterBase):
    pass


class OnlinePaymentNameMaster(OnlinePaymentNameMasterBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True