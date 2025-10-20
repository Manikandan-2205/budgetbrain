from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class StatementDetailsExtractBase(BaseModel):
    account_id: Optional[int] = None
    statement_date: datetime
    transaction_date: datetime
    description: str
    amount: float
    balance: Optional[float] = None
    category: Optional[str] = None
    extracted_data: Optional[Dict[str, Any]] = None
    is_processed: bool = False


class StatementDetailsExtractCreate(StatementDetailsExtractBase):
    pass


class StatementDetailsExtractUpdate(StatementDetailsExtractBase):
    pass


class StatementDetailsExtract(StatementDetailsExtractBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True