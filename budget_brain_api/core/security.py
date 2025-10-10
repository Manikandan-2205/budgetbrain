

from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt
from jwt import PyJWTError
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from core.config import settings
from db.models.user_model import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hashes a plain text password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    """Verifies a plain text password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    """Creates a JWT access token with an expiration time."""
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + \
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_user_from_token(token: str, db: Session):
    """
    Decodes the JWT, validates it, and fetches the User object from the database.

    Raises HTTPException if the token is invalid or expired.
    Returns the User object if valid.
    """
    try:

        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        username: str = payload.get("sub")

        if username is None:
            raise CREDENTIALS_EXCEPTION

    except PyJWTError:

        raise CREDENTIALS_EXCEPTION

    user = db.query(User).filter(User.username == username).first()

    if user is None:

        raise CREDENTIALS_EXCEPTION

    return user
