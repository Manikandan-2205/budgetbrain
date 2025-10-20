from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class CategoryBase(BaseModel):
    name: str
    type: str
    color: str = "#000000"
    icon: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int
    is_default: bool

    class Config:
        orm_mode = True


class AccountBase(BaseModel):
    name: str
    type: str
    balance: float = 0.0
    currency: str = "USD"


class AccountCreate(AccountBase):
    pass


class Account(AccountBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class TransactionBase(BaseModel):
    amount: float
    description: str
    date: datetime
    type: str
    category_id: Optional[int] = None
    tags: Optional[str] = None


class TransactionCreate(TransactionBase):
    account_id: int


class Transaction(TransactionBase):
    id: int
    user_id: int
    account_id: int
    is_recurring: bool = False
    recurring_frequency: Optional[str] = None

    class Config:
        orm_mode = True


class LoanBase(BaseModel):
    name: str
    principal_amount: float
    interest_rate: float
    term_months: int
    monthly_payment: float
    start_date: datetime
    lender: str
    loan_type: str


class LoanCreate(LoanBase):
    pass


class Loan(LoanBase):
    id: int
    user_id: int
    remaining_balance: float
    end_date: Optional[datetime] = None
    status: str = "active"

    class Config:
        orm_mode = True


class InvestmentBase(BaseModel):
    name: str
    type: str
    quantity: float
    purchase_price: float
    purchase_date: datetime
    symbol: Optional[str] = None
    brokerage: Optional[str] = None
    notes: Optional[str] = None


class InvestmentCreate(InvestmentBase):
    pass


class Investment(InvestmentBase):
    id: int
    user_id: int
    current_price: Optional[float] = None

    class Config:
        orm_mode = True
