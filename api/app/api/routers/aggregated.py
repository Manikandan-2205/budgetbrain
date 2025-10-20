from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.aggregated import Aggregated, AggregatedCreate, AggregatedUpdate
from app.services.aggregated_service import (
    get_aggregated_data,
    get_all_aggregated_data,
    create_aggregated_data,
    update_aggregated_data,
    delete_aggregated_data
)
from app.api.deps import get_current_user
from app.models.user import User


router = APIRouter()


@router.get("/aggregated/{user_id}", response_model=Aggregated)
def read_aggregated_data(user_id: int, db: Session = Depends(get_db)):
    aggregated_data = get_aggregated_data(db, user_id)
    if not aggregated_data:
        raise HTTPException(status_code=404, detail="Aggregated data not found")
    return aggregated_data


@router.get("/aggregated", response_model=list[Aggregated])
def read_all_aggregated_data(db: Session = Depends(get_db)):
    return get_all_aggregated_data(db)


@router.post("/aggregated", response_model=Aggregated)
def create_aggregated_data_endpoint(
    aggregated_data: AggregatedCreate,
    db: Session = Depends(get_db)
):
    return create_aggregated_data(db, aggregated_data.dict())


@router.put("/aggregated/{user_id}", response_model=Aggregated)
def update_aggregated_data_endpoint(
    user_id: int,
    aggregated_data: AggregatedUpdate,
    db: Session = Depends(get_db)
):
    updated_data = update_aggregated_data(db, user_id, aggregated_data.dict(exclude_unset=True))
    if not updated_data:
        raise HTTPException(status_code=404, detail="Aggregated data not found")
    return updated_data


@router.delete("/aggregated/{user_id}")
def delete_aggregated_data_endpoint(
    user_id: int,
    db: Session = Depends(get_db)
):
    deleted_data = delete_aggregated_data(db, user_id)
    if not deleted_data:
        raise HTTPException(status_code=404, detail="Aggregated data not found")
    return {"message": "Aggregated data deleted successfully"}