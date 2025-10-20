from sqlalchemy.orm import Session
from app.models.user_details import UserDetails
from app.schemas.user_details import UserDetailsCreate, UserDetailsUpdate


def get_user_details(db: Session, user_id: int):
    return db.query(UserDetails).filter(UserDetails.user_id == user_id).first()


def create_user_details(db: Session, user_details: UserDetailsCreate, user_id: int):
    db_user_details = UserDetails(**user_details.dict(), user_id=user_id)
    db.add(db_user_details)
    db.commit()
    db.refresh(db_user_details)
    return db_user_details


def update_user_details(db: Session, user_id: int, user_details: UserDetailsUpdate):
    db_user_details = get_user_details(db, user_id)
    if db_user_details:
        for key, value in user_details.dict(exclude_unset=True).items():
            setattr(db_user_details, key, value)
        db.commit()
        db.refresh(db_user_details)
    return db_user_details


def delete_user_details(db: Session, user_id: int):
    db_user_details = get_user_details(db, user_id)
    if db_user_details:
        db.delete(db_user_details)
        db.commit()
    return db_user_details