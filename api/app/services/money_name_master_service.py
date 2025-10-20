from sqlalchemy.orm import Session
from typing import List
from app.models.money_name_master import MoneyNameMaster
from app.schemas.money_name_master import MoneyNameMasterCreate, MoneyNameMasterUpdate


def get_money_name_master(db: Session, money_name_id: int):
    return db.query(MoneyNameMaster).filter(MoneyNameMaster.id == money_name_id).first()


def get_money_names_by_user(db: Session, user_id: int) -> List[MoneyNameMaster]:
    return db.query(MoneyNameMaster).filter(MoneyNameMaster.user_id == user_id).all()


def get_money_names_by_type(db: Session, user_id: int, type: str) -> List[MoneyNameMaster]:
    return db.query(MoneyNameMaster).filter(
        MoneyNameMaster.user_id == user_id,
        MoneyNameMaster.type == type
    ).all()


def create_money_name_master(db: Session, money_name: MoneyNameMasterCreate, user_id: int):
    db_money_name = MoneyNameMaster(**money_name.dict(), user_id=user_id)
    db.add(db_money_name)
    db.commit()
    db.refresh(db_money_name)
    return db_money_name


def update_money_name_master(db: Session, money_name_id: int, money_name: MoneyNameMasterUpdate):
    db_money_name = get_money_name_master(db, money_name_id)
    if db_money_name:
        for key, value in money_name.dict(exclude_unset=True).items():
            setattr(db_money_name, key, value)
        db.commit()
        db.refresh(db_money_name)
    return db_money_name


def delete_money_name_master(db: Session, money_name_id: int):
    db_money_name = get_money_name_master(db, money_name_id)
    if db_money_name:
        db.delete(db_money_name)
        db.commit()
    return db_money_name