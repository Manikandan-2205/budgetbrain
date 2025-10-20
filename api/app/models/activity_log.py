from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class ActivityLog(Base):
    __tablename__ = "tb_bb_activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("tb_bb_users.id"), nullable=True, index=True)
    action = Column(String(100), nullable=False, index=True)  # login, logout, transaction_create, etc.
    resource_type = Column(String(50), nullable=True)  # user, transaction, account, etc.
    resource_id = Column(Integer, nullable=True)  # ID of the affected resource
    description = Column(Text, nullable=True)  # Human-readable description
    log_data = Column(JSON, nullable=True)  # Additional structured data
    ip_address = Column(String(45), nullable=True)  # IPv4/IPv6 address
    user_agent = Column(Text, nullable=True)  # Browser/client info
    status = Column(String(20), default="success")  # success, failed, warning
    error_message = Column(Text, nullable=True)  # Error details if applicable
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Relationships
    user = relationship("User", back_populates="activity_logs")

    def __repr__(self):
        return f"<ActivityLog(id={self.id}, user_id={self.user_id}, action='{self.action}', status='{self.status}')>"