from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class Transaction(Base):
    __tablename__ = "tb_bb_transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("tb_bb_users.id"))
    account_id = Column(Integer, ForeignKey("tb_bb_accounts.id"))
    category_id = Column(Integer, ForeignKey("tb_bb_categories.id"), nullable=True)
    amount = Column(Float)
    description = Column(String)
    date = Column(DateTime(timezone=True))
    type = Column(String)  # income, expense, transfer
    is_recurring = Column(Boolean, default=False)
    recurring_frequency = Column(String, nullable=True)  # daily, weekly, monthly, yearly
    tags = Column(Text, nullable=True)  # JSON string for tags
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="transactions")
    account = relationship("Account", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")