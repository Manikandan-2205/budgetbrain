from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class Account(Base):
    __tablename__ = "tb_bb_accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("tb_bb_users.id"))
    name = Column(String, index=True)
    type = Column(String)  # checking, savings, credit_card, etc.
    balance = Column(Float, default=0.0)
    currency = Column(String, default="USD")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account")
    account_master = relationship("AccountMaster", back_populates="user")
    money_name_master = relationship("MoneyNameMaster", back_populates="user")
    transaction_master = relationship("TransactionMaster", back_populates="user")
    online_payment_name_master = relationship("OnlinePaymentNameMaster", back_populates="user")
    statement_details_extract = relationship("StatementDetailsExtract", back_populates="user")
    refresh_tokens = relationship("RefreshToken", back_populates="user")