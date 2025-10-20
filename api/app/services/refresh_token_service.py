from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.refresh_token import RefreshToken
from app.schemas.refresh_token import RefreshTokenCreate
from app.core.config import settings


def get_refresh_token(db: Session, token: str):
    return db.query(RefreshToken).filter(RefreshToken.token == token).first()


def create_refresh_token(db: Session, user_id: int):
    expires_at = datetime.utcnow() + timedelta(days=30)  # 30 days expiry
    token_data = RefreshTokenCreate(token=f"refresh_{user_id}_{datetime.utcnow().timestamp()}", expires_at=expires_at)
    db_token = RefreshToken(**token_data.dict(), user_id=user_id)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token


def revoke_refresh_token(db: Session, token: str):
    db_token = get_refresh_token(db, token)
    if db_token:
        db_token.is_revoked = True
        db.commit()
        db.refresh(db_token)
    return db_token


def revoke_all_user_tokens(db: Session, user_id: int):
    db.query(RefreshToken).filter(
        RefreshToken.user_id == user_id,
        RefreshToken.is_revoked == False
    ).update({"is_revoked": True})
    db.commit()


def is_token_valid(db: Session, token: str) -> bool:
    db_token = get_refresh_token(db, token)
    if not db_token:
        return False
    if db_token.is_revoked or db_token.expires_at < datetime.utcnow():
        return False
    return True