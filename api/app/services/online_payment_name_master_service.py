from sqlalchemy.orm import Session
from typing import List
from app.db.models import OnlinePaymentNameMaster
from app.schemas.online_payment_name_master import OnlinePaymentNameMasterCreate, OnlinePaymentNameMasterUpdate


def get_online_payment_name_master(db: Session, payment_id: int):
    return db.query(OnlinePaymentNameMaster).filter(OnlinePaymentNameMaster.id == payment_id).first()


def get_online_payments_by_user(db: Session, user_id: int) -> List[OnlinePaymentNameMaster]:
    return db.query(OnlinePaymentNameMaster).filter(OnlinePaymentNameMaster.user_id == user_id).all()


def create_online_payment_name_master(db: Session, payment: OnlinePaymentNameMasterCreate, user_id: int):
    db_payment = OnlinePaymentNameMaster(**payment.dict(), user_id=user_id)
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment


def update_online_payment_name_master(db: Session, payment_id: int, payment: OnlinePaymentNameMasterUpdate):
    db_payment = get_online_payment_name_master(db, payment_id)
    if db_payment:
        for key, value in payment.dict(exclude_unset=True).items():
            setattr(db_payment, key, value)
        db.commit()
        db.refresh(db_payment)
    return db_payment


def delete_online_payment_name_master(db: Session, payment_id: int):
    db_payment = get_online_payment_name_master(db, payment_id)
    if db_payment:
        db.delete(db_payment)
        db.commit()
    return db_payment