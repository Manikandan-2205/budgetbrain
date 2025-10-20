from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class StatementDetailsExtract(Base):
    __tablename__ = "tb_bb_statement_details_extract"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("tb_bb_users.id"))
    account_id = Column(Integer, ForeignKey("tb_bb_account_master.id"), nullable=True)
    statement_date = Column(DateTime(timezone=True))
    transaction_date = Column(DateTime(timezone=True))
    description = Column(String)
    amount = Column(Float)
    balance = Column(Float, nullable=True)
    category = Column(String, nullable=True)
    extracted_data = Column(JSON, nullable=True)  # Additional extracted fields
    is_processed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="statement_details_extract")
    account = relationship("AccountMaster", back_populates="statement_details_extract")