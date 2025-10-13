from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from requests import Session
from streamlit import status

from db.models.user_model import User
from db.schemas.common.common_schema import APIResponse
from db.session import get_db

router = APIRouter(prefix="v1/user", tags=["Authentication"])


@router.get("/get-all-user",)
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
            ), status.HTTP_404_NOT_FOUND

        return APIResponse(
            issuccess=True,
            message="User details fetched successfully.",
            data=user_details,
        )

    except Exception as e:
        # You can log this error internally if needed
        return APIResponse(
            issuccess=False,
            message="Internal server error.",
            error=str(e),
        ), status.HTTP_500_INTERNAL_SERVER_ERROR
