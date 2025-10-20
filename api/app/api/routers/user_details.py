from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user_details import UserDetails, UserDetailsCreate, UserDetailsUpdate
from app.services.user_details_service import (
    get_user_details,
    create_user_details,
    update_user_details,
    delete_user_details
)
from app.api.deps import get_current_user
from app.models.user import User


router = APIRouter()


@router.get("/me/details", response_model=UserDetails)
def read_user_details(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_details = get_user_details(db, current_user.id)
    if not user_details:
        raise HTTPException(status_code=404, detail="User details not found")
    return user_details


@router.post("/me/details", response_model=UserDetails)
def create_user_details_endpoint(
    user_details: UserDetailsCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    existing_details = get_user_details(db, current_user.id)
    if existing_details:
        raise HTTPException(status_code=400, detail="User details already exist")
    return create_user_details(db, user_details, current_user.id)


@router.put("/me/details", response_model=UserDetails)
def update_user_details_endpoint(
    user_details: UserDetailsUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    updated_details = update_user_details(db, current_user.id, user_details)
    if not updated_details:
        raise HTTPException(status_code=404, detail="User details not found")
    return updated_details


@router.delete("/me/details")
def delete_user_details_endpoint(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    deleted_details = delete_user_details(db, current_user.id)
    if not deleted_details:
        raise HTTPException(status_code=404, detail="User details not found")
    return {"message": "User details deleted successfully"}