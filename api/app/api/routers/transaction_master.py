from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.db.session import get_db
from app.schemas.transaction_master import TransactionMaster, TransactionMasterCreate, TransactionMasterUpdate
from app.services.transaction_master_service import (
    get_transaction_master,
    get_transactions_by_user,
    get_transactions_by_account,
    get_transactions_by_date_range,
    create_transaction_master,
    update_transaction_master,
    delete_transaction_master
)
from app.api.deps import get_current_user
from app.models.user import User


router = APIRouter()


@router.get("/transactions", response_model=List[TransactionMaster])
def read_transactions(
    account_id: int = Query(None),
    start_date: datetime = Query(None),
    end_date: datetime = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if account_id:
        return get_transactions_by_account(db, account_id)
    elif start_date and end_date:
        return get_transactions_by_date_range(db, current_user.id, start_date, end_date)
    return get_transactions_by_user(db, current_user.id)


@router.get("/transactions/{transaction_id}", response_model=TransactionMaster)
def read_transaction(
    transaction_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    transaction = get_transaction_master(db, transaction_id)
    if not transaction or transaction.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.post("/transactions", response_model=TransactionMaster)
def create_transaction(
    transaction: TransactionMasterCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_transaction_master(db, transaction, current_user.id)


@router.put("/transactions/{transaction_id}", response_model=TransactionMaster)
def update_transaction(
    transaction_id: int,
    transaction: TransactionMasterUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_transaction = get_transaction_master(db, transaction_id)
    if not db_transaction or db_transaction.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return update_transaction_master(db, transaction_id, transaction)


@router.delete("/transactions/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_transaction = get_transaction_master(db, transaction_id)
    if not db_transaction or db_transaction.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Transaction not found")
    delete_transaction_master(db, transaction_id)
    return {"message": "Transaction deleted successfully"}