from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class AccountMaster(Base):
    __tablename__ = "tb_bb_account_master"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("tb_bb_users.id"))
    account_name = Column(String, index=True)
    account_type = Column(String)  # checking, savings, credit_card, etc.
    bank_name = Column(String, nullable=True)
    account_number = Column(String, nullable=True)
    balance = Column(Float, default=0.0)
    currency = Column(String, default="USD")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="account_master")
    transaction_master = relationship("TransactionMaster", back_populates="account")
    statement_details_extract = relationship("StatementDetailsExtract", back_populates="account")