from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.online_payment_name_master import (
    OnlinePaymentNameMaster,
    OnlinePaymentNameMasterCreate,
    OnlinePaymentNameMasterUpdate
)
from app.services.online_payment_name_master_service import (
    get_online_payment_name_master,
    get_online_payments_by_user,
    create_online_payment_name_master,
    update_online_payment_name_master,
    delete_online_payment_name_master
)
from app.api.deps import get_current_user
from app.db.models import User


router = APIRouter()


@router.get("/online-payments", response_model=List[OnlinePaymentNameMaster])
def read_online_payments(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_online_payments_by_user(db, current_user.id)


@router.get("/online-payments/{payment_id}", response_model=OnlinePaymentNameMaster)
def read_online_payment(
    payment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    payment = get_online_payment_name_master(db, payment_id)
    if not payment or payment.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Online payment not found")
    return payment


@router.post("/online-payments", response_model=OnlinePaymentNameMaster)
def create_online_payment(
    payment: OnlinePaymentNameMasterCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_online_payment_name_master(db, payment, current_user.id)


@router.put("/online-payments/{payment_id}", response_model=OnlinePaymentNameMaster)
def update_online_payment(
    payment_id: int,
    payment: OnlinePaymentNameMasterUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_payment = get_online_payment_name_master(db, payment_id)
    if not db_payment or db_payment.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Online payment not found")
    return update_online_payment_name_master(db, payment_id, payment)


@router.delete("/online-payments/{payment_id}")
def delete_online_payment(
    payment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_payment = get_online_payment_name_master(db, payment_id)
    if not db_payment or db_payment.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Online payment not found")
    delete_online_payment_name_master(db, payment_id)
    return {"message": "Online payment deleted successfully"}