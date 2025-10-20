from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class TransactionMaster(Base):
    __tablename__ = "tb_bb_transaction_master"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("tb_bb_users.id"))
    account_id = Column(Integer, ForeignKey("tb_bb_account_master.id"))
    money_name_id = Column(Integer, ForeignKey("tb_bb_money_name_master.id"), nullable=True)
    amount = Column(Float)
    description = Column(String, nullable=True)
    transaction_date = Column(DateTime(timezone=True))
    transaction_type = Column(String)  # income, expense, transfer
    payment_method = Column(String, nullable=True)  # cash, card, online, etc.
    tags = Column(JSON, nullable=True)
    is_recurring = Column(Boolean, default=False)
    recurring_frequency = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="transaction_master")
    account = relationship("AccountMaster", back_populates="transaction_master")
    money_name = relationship("MoneyNameMaster", back_populates="transaction_master")