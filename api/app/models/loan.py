from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from app.db.base import Base


class Loan(Base):
    __tablename__ = "tb_bb_loans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    principal_amount = Column(Float)
    interest_rate = Column(Float)
    term_months = Column(Integer)
    monthly_payment = Column(Float)
    remaining_balance = Column(Float)
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True), nullable=True)
    lender = Column(String)
    loan_type = Column(String)  # personal, mortgage, auto, etc.
    status = Column(String, default="active")  # active, paid_off, defaulted
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())