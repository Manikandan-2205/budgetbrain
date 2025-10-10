from sqlalchemy import Column, Integer, DateTime

class PrimarykeyMixin:
    """
    Mixin for primary key column.
    This class is abstract and will not create a table.
    """
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

class AuditMixin:
    """
    Mixin for common audit columns: created_at, updated_at, etc.
    This class is abstract and will not create a table.
    """
    __abstract__ = True

    created_at = Column(DateTime, nullable=False)
    created_by = Column(Integer, nullable=False)
    updated_at = Column(DateTime, nullable=True)
    updated_by = Column(Integer, nullable=True)
    is_active = Column(Integer, default=1, nullable=False)
    is_deleted = Column(Integer, default=0, nullable=False)