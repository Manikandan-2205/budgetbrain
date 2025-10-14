from sqlalchemy import Column, String, Integer, DateTime, Enum as SQLEnum
from db.Enum.role_enum import RoleEnum
from db.session import Base


class User(Base):
    __tablename__ = "tb_bb_users"
    __table_args__ = {"schema": "bb"}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    username = Column(String(20), unique=True, index=True, nullable=False)
    # NOTE: Storing passwords this way is highly insecure. Use a strong hashing library like 'bcrypt'.
    password = Column(String(300), nullable=False)
    display_name = Column(String(20), nullable=False)
    role = Column(Integer, nullable=False, default=RoleEnum.User)

    created_at = Column(DateTime, nullable=False)
    created_by = Column(Integer, nullable=False)
    updated_at = Column(DateTime, nullable=True)
    updated_by = Column(Integer, nullable=True)
    is_active = Column(Integer, default=1, nullable=False)
    is_deleted = Column(Integer, default=0, nullable=False)