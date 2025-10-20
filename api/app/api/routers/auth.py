from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import authenticate_user, create_access_token, get_password_hash
from app.schemas.auth import UserCreate, Token, TokenRefresh, User
from app.schemas.refresh_token import TokenResponse, RefreshTokenRequest
from app.services.refresh_token_service import (
    create_refresh_token,
    revoke_refresh_token,
    revoke_all_user_tokens,
    is_token_valid
)
from app.models.user import User as UserModel
from app.core.config import settings


router = APIRouter()


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


@router.post("/register", response_model=User)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    db_user = UserModel(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(db, user.id)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token.token,
        "token_type": "bearer"
    }


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(refresh_data: RefreshTokenRequest, db: Session = Depends(get_db)):
    if not is_token_valid(db, refresh_data.refresh_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )

    refresh_db = db.query(RefreshToken).filter(
        RefreshToken.token == refresh_data.refresh_token
    ).first()

    user = refresh_db.user
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    # Revoke old refresh token and create new one
    revoke_refresh_token(db, refresh_data.refresh_token)
    new_refresh_token = create_refresh_token(db, user.id)

    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token.token,
        "token_type": "bearer"
    }


@router.post("/logout")
def logout(refresh_data: TokenRefresh, db: Session = Depends(get_db)):
    revoke_refresh_token(db, refresh_data.refresh_token)
    return {"message": "Successfully logged out"}
