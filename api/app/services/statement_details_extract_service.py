from sqlalchemy.orm import Session
from typing import List
from app.models.statement_details_extract import StatementDetailsExtract
from app.schemas.statement_details_extract import StatementDetailsExtractCreate, StatementDetailsExtractUpdate


def get_statement_details_extract(db: Session, extract_id: int):
    return db.query(StatementDetailsExtract).filter(StatementDetailsExtract.id == extract_id).first()


def get_extracts_by_user(db: Session, user_id: int) -> List[StatementDetailsExtract]:
    return db.query(StatementDetailsExtract).filter(StatementDetailsExtract.user_id == user_id).all()


def get_extracts_by_account(db: Session, account_id: int) -> List[StatementDetailsExtract]:
    return db.query(StatementDetailsExtract).filter(StatementDetailsExtract.account_id == account_id).all()


def get_unprocessed_extracts(db: Session, user_id: int) -> List[StatementDetailsExtract]:
    return db.query(StatementDetailsExtract).filter(
        StatementDetailsExtract.user_id == user_id,
        StatementDetailsExtract.is_processed == False
    ).all()


def create_statement_details_extract(db: Session, extract: StatementDetailsExtractCreate, user_id: int):
    db_extract = StatementDetailsExtract(**extract.dict(), user_id=user_id)
    db.add(db_extract)
    db.commit()
    db.refresh(db_extract)
    return db_extract


def update_statement_details_extract(db: Session, extract_id: int, extract: StatementDetailsExtractUpdate):
    db_extract = get_statement_details_extract(db, extract_id)
    if db_extract:
        for key, value in extract.dict(exclude_unset=True).items():
            setattr(db_extract, key, value)
        db.commit()
        db.refresh(db_extract)
    return db_extract


def delete_statement_details_extract(db: Session, extract_id: int):
    db_extract = get_statement_details_extract(db, extract_id)
    if db_extract:
        db.delete(db_extract)
        db.commit()
    return db_extract


def mark_extract_as_processed(db: Session, extract_id: int):
    db_extract = get_statement_details_extract(db, extract_id)
    if db_extract:
        db_extract.is_processed = True
        db.commit()
        db.refresh(db_extract)
    return db_extract