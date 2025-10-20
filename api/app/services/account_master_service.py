from sqlalchemy.orm import Session
from typing import List
from app.models.account_master import AccountMaster
from app.schemas.account_master import AccountMasterCreate, AccountMasterUpdate


def get_account_master(db: Session, account_id: int):
    return db.query(AccountMaster).filter(AccountMaster.id == account_id).first()


def get_accounts_by_user(db: Session, user_id: int) -> List[AccountMaster]:
    return db.query(AccountMaster).filter(AccountMaster.user_id == user_id).all()


def create_account_master(db: Session, account: AccountMasterCreate, user_id: int):
    db_account = AccountMaster(**account.dict(), user_id=user_id)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account


def update_account_master(db: Session, account_id: int, account: AccountMasterUpdate):
    db_account = get_account_master(db, account_id)
    if db_account:
        for key, value in account.dict(exclude_unset=True).items():
            setattr(db_account, key, value)
        db.commit()
        db.refresh(db_account)
    return db_account


def delete_account_master(db: Session, account_id: int):
    db_account = get_account_master(db, account_id)
    if db_account:
        db.delete(db_account)
        db.commit()
    return db_account