import logging
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import authenticate_user, create_access_token, get_password_hash, verify_password
from app.schemas.auth import UserCreate, Token, TokenRefresh, User
from app.schemas.refresh_token import TokenResponse, RefreshTokenRequest
from app.schemas.response import APIResponse, _success_response, _error_response, _validation_error_response
from app.services.refresh_token_service import (
    create_refresh_token,
    revoke_refresh_token,
    revoke_all_user_tokens,
    is_token_valid
)
from app.services.log_manager import get_log_manager
from app.models.user import User as UserModel
from app.models.refresh_token import RefreshToken
from app.core.config import settings

_logger = logging.getLogger(__name__)


router = APIRouter()


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


@router.post(" ", response_model=User)
def register(user: UserCreate, db: Session = Depends(get_db)):
        _logger.info(f"Registration attempt for username: {user.username}, email: {user.email}")

        # Log registration attempt
        log_manager = get_log_manager()
        log_manager.log_activity(
            user_id=None,
            action="user_register_attempt",
            description=f"Registration attempt for username: {user.username}, email: {user.email}",
            status="pending"
        )

        db_user = db.query(UserModel).filter(UserModel.username == user.username).first()
        if db_user:
            _logger.warning(f"Registration failed: Username {user.username} already exists")
            log_manager.log_activity(
                user_id=None,
                action="user_register_failed",
                description=f"Registration failed: Username {user.username} already exists",
                status="failed",
                error_message="Username already registered"
            )
            raise HTTPException(status_code=400, detail="Username already registered")

        db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
        if db_user:
            _logger.warning(f"Registration failed: Email {user.email} already exists")
            log_manager.log_activity(
                user_id=None,
                action="user_register_failed",
                description=f"Registration failed: Email {user.email} already exists",
                status="failed",
                error_message="Email already registered"
            )
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
        _logger.info(f"User {user.username} registered successfully with ID: {db_user.id}")

        # Log successful registration
        log_manager.log_activity(
            user_id=db_user.id,
            action="user_register_success",
            description=f"User {user.username} registered successfully",
            status="success"
        )

        return _success_response("User registered successfully", db_user.dict())


@router.post("/login", response_model=APIResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    _logger.info(f"Login attempt for username: {form_data.username}")

    # Log login attempt
    log_manager = get_log_manager()
    log_manager.log_activity(
        user_id=None,
        action="user_login_attempt",
        description=f"Login attempt for username: {form_data.username}",
        status="pending"
    )

    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        _logger.warning(f"Login failed for username: {form_data.username} - Invalid credentials")
        log_manager.log_activity(
            user_id=None,
            action="user_login_failed",
            description=f"Login failed for username: {form_data.username} - Invalid credentials",
            status="failed",
            error_message="Incorrect username or password"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={
            "sub": user.username,
            "user_id": user.id,
            "role": user.role
        },
        expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(db, user.id)
    _logger.info(f"Login successful for user: {user.username} (ID: {user.id}, Role: {user.role})")

    # Log successful login
    log_manager.log_activity(
        user_id=user.id,
        action="user_login_success",
        description=f"User {user.username} logged in successfully",
        status="success"
    )

    return _success_response("Login successful", {
        "access_token": access_token,
        "refresh_token": refresh_token.token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
    })


@router.post("/refresh", response_model=APIResponse)
def refresh_token(refresh_data: RefreshTokenRequest, db: Session = Depends(get_db)):
    _logger.info(f"Token refresh attempt with token: {refresh_data.refresh_token[:10]}...")
    if not is_token_valid(db, refresh_data.refresh_token):
        _logger.warning(f"Token refresh failed: Invalid or expired refresh token")
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
        data={
            "sub": user.username,
            "user_id": user.id,
            "role": user.role
        },
        expires_delta=access_token_expires
    )

    # Revoke old refresh token and create new one
    revoke_refresh_token(db, refresh_data.refresh_token)
    new_refresh_token = create_refresh_token(db, user.id)

    _logger.info(f"Token refresh successful for user: {user.username} (ID: {user.id})")
    return _success_response("Token refreshed successfully", {
        "access_token": access_token,
        "refresh_token": new_refresh_token.token,
        "token_type": "bearer"
    })


@router.post("/logout", response_model=APIResponse)
def logout(refresh_data: TokenRefresh, db: Session = Depends(get_db)):
    _logger.info(f"Logout attempt with token: {refresh_data.refresh_token[:10]}...")

    # Get user from refresh token for logging
    refresh_db = db.query(RefreshToken).filter(
        RefreshToken.token == refresh_data.refresh_token
    ).first()

    user_id = refresh_db.user.id if refresh_db else None

    # Log logout attempt
    log_manager = get_log_manager()
    log_manager.log_activity(
        user_id=user_id,
        action="user_logout",
        description=f"User logged out",
        status="success"
    )

    revoke_refresh_token(db, refresh_data.refresh_token)
    _logger.info("Logout successful")
    return _success_response("Successfully logged out")
