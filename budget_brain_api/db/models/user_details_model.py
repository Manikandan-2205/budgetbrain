from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from db.session import Base

class UserDetails(Base):
    __tablename__ = "tb_bb_user_details"
    __table_args__ = {"schema": "bb"}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    email = Column(String(50), unique = True, index = True, nullable = False)
    phone_number = Column(String(15), unique = True, index = True, nullable = False)
    aadhar_number = Column(String(12), unique = True, index = True, nullable = False)
    pan_number = Column(String(10), unique = True, index = True, nullable = False)
    
    address_line1 = Column(String(100), nullable = True)
    address_line2 = Column(String(100), nullable = True)  
    city = Column(Integer, nullable = False)
    state = Column(Integer, nullable = False)
    pincode = Column(Integer, nullable = False)

    user_id = Column(Integer, ForeignKey("bb.tb_bb_users.id"), nullable = False)

    created_at = Column(DateTime, nullable=False)
    created_by = Column(Integer, nullable=False)
    updated_at = Column(DateTime, nullable=True)
    updated_by = Column(Integer, nullable=True)
    is_active = Column(Integer, default=1, nullable=False)
    is_deleted = Column(Integer, default=0, nullable=False)

   