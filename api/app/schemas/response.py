from typing import Any, Dict, Optional
from pydantic import BaseModel


class APIResponse(BaseModel):
    """Standardized API response format"""
    success: bool
    message: str
    data: Optional[Any] = None
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    status_code: int

    class Config:
        from_attributes = True


def _create_success_response(
    message: str,
    data: Any = None,
    status_code: int = 200
) -> APIResponse:
    """Create a success response"""
    return APIResponse(
        success=True,
        message=message,
        data=data,
        status_code=status_code
    )


def _create_error_response(
    message: str,
    error_code: str,
    error_message: str,
    status_code: int = 400
) -> APIResponse:
    """Create an error response"""
    return APIResponse(
        success=False,
        message=message,
        error_code=error_code,
        error_message=error_message,
        status_code=status_code
    )


# Common response functions
def _success_response(message: str = "Operation successful", data: Any = None) -> APIResponse:
    return _create_success_response(message, data)

def _error_response(
    message: str = "An error occurred",
    error_code: str = "INTERNAL_ERROR",
    error_message: str = "Internal server error",
    status_code: int = 500
) -> APIResponse:
    return _create_error_response(message, error_code, error_message, status_code)

def _validation_error_response(error_message: str) -> APIResponse:
    return _create_error_response(
        "Validation failed",
        "VALIDATION_ERROR",
        error_message,
        422
    )

def _not_found_response(resource: str = "Resource") -> APIResponse:
    return _create_error_response(
        f"{resource} not found",
        "NOT_FOUND",
        f"The requested {resource.lower()} was not found",
        404
    )

def _unauthorized_response() -> APIResponse:
    return _create_error_response(
        "Authentication required",
        "UNAUTHORIZED",
        "You must be authenticated to access this resource",
        401
    )

def _forbidden_response() -> APIResponse:
    return _create_error_response(
        "Access denied",
        "FORBIDDEN",
        "You don't have permission to access this resource",
        403
    )