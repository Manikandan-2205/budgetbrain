from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.api.deps import get_current_user
from app.schemas.transactions import Account, AccountCreate
from app.models.account import Account as AccountModel
from app.models.user import User


router = APIRouter()


@router.get("/", response_model=List[Account])
def read_accounts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    accounts = db.query(AccountModel).filter(AccountModel.user_id == current_user.id).offset(skip).limit(limit).all()
    return accounts


@router.post("/", response_model=Account)
def create_account(
    account: AccountCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_account = AccountModel(**account.dict(), user_id=current_user.id)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account


@router.get("/{account_id}", response_model=Account)
def read_account(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    account = db.query(AccountModel).filter(
        AccountModel.id == account_id,
        AccountModel.user_id == current_user.id
    ).first()
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@router.put("/{account_id}", response_model=Account)
def update_account(
    account_id: int,
    account_update: AccountCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    account = db.query(AccountModel).filter(
        AccountModel.id == account_id,
        AccountModel.user_id == current_user.id
    ).first()
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    for key, value in account_update.dict().items():
        setattr(account, key, value)
    db.commit()
    db.refresh(account)
    return account


@router.delete("/{account_id}")
def delete_account(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    account = db.query(AccountModel).filter(
        AccountModel.id == account_id,
        AccountModel.user_id == current_user.id
    ).first()
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    db.delete(account)
    db.commit()
    return {"message": "Account deleted successfully"}
