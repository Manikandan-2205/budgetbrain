from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from db.session import get_db
from db.models.user_model import User
from db.schemas.user_schema import UserCreate, UserResponse
from db.schemas.common.common_schema import APIResponse
from core.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/v1/register", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(User).filter(User.username == user_data.username).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")

        hashed_pwd = hash_password(user_data.password)
        new_user = User(
            username=user_data.username,
            password=hashed_pwd,
            display_name=user_data.display_name
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return APIResponse(
            isSuccess=True,
            message="User registered successfully",
            data=UserResponse.from_orm(new_user)
        )
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(ex))


@router.post("/login", response_model=APIResponse)
def login_user(user_data: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user_data.username).first()
    if not db_user or not verify_password(user_data.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token({"sub": db_user.username})
    return APIResponse(
        isSuccess=True,
        message="Login successful",
        data={"access_token": token, "token_type": "bearer"}
    )
