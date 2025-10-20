from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.statement_details_extract import (
    StatementDetailsExtract,
    StatementDetailsExtractCreate,
    StatementDetailsExtractUpdate
)
from app.services.statement_details_extract_service import (
    get_statement_details_extract,
    get_extracts_by_user,
    get_extracts_by_account,
    get_unprocessed_extracts,
    create_statement_details_extract,
    update_statement_details_extract,
    delete_statement_details_extract,
    mark_extract_as_processed
)
from app.api.deps import get_current_user
from app.db.models import User


router = APIRouter()


@router.get("/statement-extracts", response_model=List[StatementDetailsExtract])
def read_statement_extracts(
    account_id: int = Query(None),
    unprocessed_only: bool = Query(False),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if unprocessed_only:
        return get_unprocessed_extracts(db, current_user.id)
    elif account_id:
        return get_extracts_by_account(db, account_id)
    return get_extracts_by_user(db, current_user.id)


@router.get("/statement-extracts/{extract_id}", response_model=StatementDetailsExtract)
def read_statement_extract(
    extract_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    extract = get_statement_details_extract(db, extract_id)
    if not extract or extract.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Statement extract not found")
    return extract


@router.post("/statement-extracts", response_model=StatementDetailsExtract)
def create_statement_extract(
    extract: StatementDetailsExtractCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_statement_details_extract(db, extract, current_user.id)


@router.put("/statement-extracts/{extract_id}", response_model=StatementDetailsExtract)
def update_statement_extract(
    extract_id: int,
    extract: StatementDetailsExtractUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_extract = get_statement_details_extract(db, extract_id)
    if not db_extract or db_extract.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Statement extract not found")
    return update_statement_details_extract(db, extract_id, extract)


@router.put("/statement-extracts/{extract_id}/process")
def mark_extract_processed(
    extract_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_extract = get_statement_details_extract(db, extract_id)
    if not db_extract or db_extract.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Statement extract not found")
    mark_extract_as_processed(db, extract_id)
    return {"message": "Extract marked as processed"}


@router.delete("/statement-extracts/{extract_id}")
def delete_statement_extract(
    extract_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_extract = get_statement_details_extract(db, extract_id)
    if not db_extract or db_extract.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Statement extract not found")
    delete_statement_details_extract(db, extract_id)
    return {"message": "Statement extract deleted successfully"}