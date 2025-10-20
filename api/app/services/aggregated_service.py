from sqlalchemy.orm import Session
from app.models.aggregated import AggregatedModel
from typing import List, Optional


def get_aggregated_data(db: Session, user_id: int) -> Optional[AggregatedModel]:
    return db.query(AggregatedModel).filter(AggregatedModel.user_id == user_id).first()


def get_all_aggregated_data(db: Session) -> List[AggregatedModel]:
    return db.query(AggregatedModel).all()


def create_aggregated_data(db: Session, aggregated_data: dict) -> AggregatedModel:
    db_aggregated = AggregatedModel(**aggregated_data)
    db.add(db_aggregated)
    db.commit()
    db.refresh(db_aggregated)
    return db_aggregated


def update_aggregated_data(db: Session, user_id: int, aggregated_data: dict) -> Optional[AggregatedModel]:
    db_aggregated = get_aggregated_data(db, user_id)
    if db_aggregated:
        for key, value in aggregated_data.items():
            setattr(db_aggregated, key, value)
        db.commit()
        db.refresh(db_aggregated)
    return db_aggregated


def delete_aggregated_data(db: Session, user_id: int) -> Optional[AggregatedModel]:
    db_aggregated = get_aggregated_data(db, user_id)
    if db_aggregated:
        db.delete(db_aggregated)
        db.commit()
    return db_aggregated