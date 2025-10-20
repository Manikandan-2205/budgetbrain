from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class MoneyNameMaster(Base):
    __tablename__ = "tb_bb_money_name_master"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("tb_bb_users.id"))
    name = Column(String, index=True)  # e.g., "Salary", "Rent", "Groceries"
    type = Column(String)  # income, expense
    category = Column(String, nullable=True)
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="money_name_master")
    transaction_master = relationship("TransactionMaster", back_populates="money_name")