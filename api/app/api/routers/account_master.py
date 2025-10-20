from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.account_master import AccountMaster, AccountMasterCreate, AccountMasterUpdate
from app.services.account_master_service import (
    get_account_master,
    get_accounts_by_user,
    create_account_master,
    update_account_master,
    delete_account_master
)
from app.api.deps import get_current_user
from app.db.models import User


router = APIRouter()


@router.get("/accounts", response_model=List[AccountMaster])
def read_accounts(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_accounts_by_user(db, current_user.id)


@router.get("/accounts/{account_id}", response_model=AccountMaster)
def read_account(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    account = get_account_master(db, account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@router.post("/accounts", response_model=AccountMaster)
def create_account(
    account: AccountMasterCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_account_master(db, account, current_user.id)


@router.put("/accounts/{account_id}", response_model=AccountMaster)
def update_account(
    account_id: int,
    account: AccountMasterUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_account = get_account_master(db, account_id)
    if not db_account or db_account.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Account not found")
    return update_account_master(db, account_id, account)


@router.delete("/accounts/{account_id}")
def delete_account(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_account = get_account_master(db, account_id)
    if not db_account or db_account.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Account not found")
    delete_account_master(db, account_id)
    return {"message": "Account deleted successfully"}