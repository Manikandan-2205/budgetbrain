from datetime import datetime
from fastapi import APIRouter, HTTPException, status,Depends
from sqlalchemy.orm import Session

from db.models.user.user_details_model import UserDetails
from db.schemas.user_schema import UserCreate, UserDetailsCreate
from db.models.user.user_model import User
from db.schemas.common.common_schema import APIResponse
from db.session import get_db

# router = APIRouter(prefix="/v1/user", tags=["Authentication"])
router = APIRouter(prefix="/v1/user")


@router.get(
    "/get-all-user",
    response_model=APIResponse,
    status_code=status.HTTP_200_OK
)
def get_all_user_details(db: Session = Depends(get_db)):
    try:
        user_details = (
            db.query(User)
            .filter(User.is_active == 1, User.is_deleted == 0)
            .all()
        )

        if not user_details:
            return APIResponse(
                issuccess=False,
                message="No active users found.",
                data=[],
                error=None,
            )

        return APIResponse(
            issuccess=True,
            message="User details fetched successfully.",
            data=user_details,
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
    
@router.get("/get-user-by-id", response_model=APIResponse, status_code=status.HTTP_200_OK)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id, User.is_active == 1, User.is_deleted == 0).first()
        if not user:
            return APIResponse(
                issuccess=False,
                message="User not found.",
                data=None,
                error=None,
            )

        return APIResponse(
            issuccess=True,
            message="User details fetched successfully.",
            data=user,
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
    
@router.post("/create-user", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
def create_user_with_details(
    user_data: UserCreate,
    user_details_data: UserDetailsCreate,
    db: Session = Depends(get_db)
):
    try:
        new_user = User(**user_data.dict(), created_at=datetime.now(), created_by=1)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        new_details = UserDetails(**user_details_data.dict(), user_id=new_user.id, created_at=datetime.utcnow(), created_by=1)
        db.add(new_details)
        db.commit()

        return APIResponse(
            issuccess=True,
            message="User and details created successfully.",
            data={"user_id": new_user.id},
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
