from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class OnlinePaymentNameMaster(Base):
    __tablename__ = "tb_bb_online_payment_name_master"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("tb_bb_users.id"))
    payment_name = Column(String, index=True)  # e.g., "PayPal", "Venmo", "Zelle"
    provider = Column(String, nullable=True)
    account_email = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="online_payment_name_master")