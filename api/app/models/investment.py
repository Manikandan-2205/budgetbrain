from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from app.db.base import Base


class Investment(Base):
    __tablename__ = "tb_bb_investments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    type = Column(String)  # stock, bond, mutual_fund, crypto, etc.
    symbol = Column(String, nullable=True)
    quantity = Column(Float)
    purchase_price = Column(Float)
    current_price = Column(Float, nullable=True)
    purchase_date = Column(DateTime(timezone=True))
    brokerage = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())