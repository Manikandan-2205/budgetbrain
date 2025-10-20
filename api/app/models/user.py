from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class User(Base):
    __tablename__ = "tb_bb_users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String(350))
    role = Column(String, default="user")  # user, admin, developer
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    accounts = relationship("Account", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")
    user_details = relationship("UserDetails", back_populates="user", uselist=False)
    account_master = relationship("AccountMaster", back_populates="user")
    money_name_master = relationship("MoneyNameMaster", back_populates="user")
    transaction_master = relationship("TransactionMaster", back_populates="user")
    online_payment_name_master = relationship("OnlinePaymentNameMaster", back_populates="user")
    statement_details_extract = relationship("StatementDetailsExtract", back_populates="user")
    refresh_tokens = relationship("RefreshToken", back_populates="user")
    activity_logs = relationship("ActivityLog", back_populates="user")