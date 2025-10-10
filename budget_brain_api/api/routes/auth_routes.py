from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.session import get_db
from core.security import hash_password, verify_password, create_access_token

# ----------------------------------------------------------------------
# CRITICAL IMPORTS: 
# 1. Pydantic Schemas (Fixes the FastAPIError)
from db.schemas.user_schema import UserCreate, UserResponse 

# 2. SQLAlchemy Model
# Ensure your User model class is defined in this file path
from db.models.user_model import User 
# ----------------------------------------------------------------------

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post(
    "/register", 
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user"
)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Creates a new user account in the database.
    
    - **username**: Must be unique.
    - **password**: Will be hashed before storage.
    - **display_name**: User's visible name.
    """
    
    # 1. Check if username already exists
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Username already exists"
        )

    # 2. Hash the password
    hashed_pwd = hash_password(user_data.password)
    
    # 3. Create the new SQLAlchemy model instance
    new_user = User(
        username=user_data.username, 
        password=hashed_pwd, 
        display_name=user_data.display_name
    )
    
    # 4. Add to database and commit
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # 5. Return the UserResponse schema
    return new_user

@router.post("/login", summary="Authenticate and receive JWT token")
def login_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Authenticates a user and returns a JWT access token.
    """
    
    # 1. Retrieve the user by username
    db_user = db.query(User).filter(User.username == user_data.username).first()
    
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid credentials"
        )
        
    # 2. Verify the password
    if not verify_password(user_data.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid credentials"
        )
        
    # 3. Create the access token
    access_token = create_access_token(data={"sub": db_user.username})
    
    # 4. Return the token
    return {"access_token": access_token, "token_type": "bearer"}