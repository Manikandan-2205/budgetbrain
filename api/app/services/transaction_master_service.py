from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.models.transaction_master import TransactionMaster
from app.schemas.transaction_master import TransactionMasterCreate, TransactionMasterUpdate


def get_transaction_master(db: Session, transaction_id: int):
    return db.query(TransactionMaster).filter(TransactionMaster.id == transaction_id).first()


def get_transactions_by_user(db: Session, user_id: int) -> List[TransactionMaster]:
    return db.query(TransactionMaster).filter(TransactionMaster.user_id == user_id).all()


def get_transactions_by_account(db: Session, account_id: int) -> List[TransactionMaster]:
    return db.query(TransactionMaster).filter(TransactionMaster.account_id == account_id).all()


def get_transactions_by_date_range(
    db: Session, user_id: int, start_date: datetime, end_date: datetime
) -> List[TransactionMaster]:
    return db.query(TransactionMaster).filter(
        TransactionMaster.user_id == user_id,
        TransactionMaster.transaction_date >= start_date,
        TransactionMaster.transaction_date <= end_date
    ).all()


def create_transaction_master(db: Session, transaction: TransactionMasterCreate, user_id: int):
    db_transaction = TransactionMaster(**transaction.dict(), user_id=user_id)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def update_transaction_master(db: Session, transaction_id: int, transaction: TransactionMasterUpdate):
    db_transaction = get_transaction_master(db, transaction_id)
    if db_transaction:
        for key, value in transaction.dict(exclude_unset=True).items():
            setattr(db_transaction, key, value)
        db.commit()
        db.refresh(db_transaction)
    return db_transaction


def delete_transaction_master(db: Session, transaction_id: int):
    db_transaction = get_transaction_master(db, transaction_id)
    if db_transaction:
        db.delete(db_transaction)
        db.commit()
    return db_transaction