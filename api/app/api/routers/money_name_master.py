from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.money_name_master import MoneyNameMaster, MoneyNameMasterCreate, MoneyNameMasterUpdate
from app.services.money_name_master_service import (
    get_money_name_master,
    get_money_names_by_user,
    get_money_names_by_type,
    create_money_name_master,
    update_money_name_master,
    delete_money_name_master
)
from app.api.deps import get_current_user
from app.models.user import User


router = APIRouter()


@router.get("/money-names", response_model=List[MoneyNameMaster])
def read_money_names(
    type_filter: str = Query(None, alias="type"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if type_filter:
        return get_money_names_by_type(db, current_user.id, type_filter)
    return get_money_names_by_user(db, current_user.id)


@router.get("/money-names/{money_name_id}", response_model=MoneyNameMaster)
def read_money_name(
    money_name_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    money_name = get_money_name_master(db, money_name_id)
    if not money_name or money_name.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Money name not found")
    return money_name


@router.post("/money-names", response_model=MoneyNameMaster)
def create_money_name(
    money_name: MoneyNameMasterCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_money_name_master(db, money_name, current_user.id)


@router.put("/money-names/{money_name_id}", response_model=MoneyNameMaster)
def update_money_name(
    money_name_id: int,
    money_name: MoneyNameMasterUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_money_name = get_money_name_master(db, money_name_id)
    if not db_money_name or db_money_name.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Money name not found")
    return update_money_name_master(db, money_name_id, money_name)


@router.delete("/money-names/{money_name_id}")
def delete_money_name(
    money_name_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_money_name = get_money_name_master(db, money_name_id)
    if not db_money_name or db_money_name.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Money name not found")
    delete_money_name_master(db, money_name_id)
    return {"message": "Money name deleted successfully"}