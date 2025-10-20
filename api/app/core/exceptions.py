"""
Custom exceptions for BudgetBrain API
"""

from typing import Dict, Any, Optional
from fastapi import HTTPException, status


class BudgetBrainException(Exception):
    """Base exception for BudgetBrain application"""

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class AuthenticationError(BudgetBrainException):
    """Authentication related errors"""

    def __init__(self, message: str = "Authentication failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED, details)


class AuthorizationError(BudgetBrainException):
    """Authorization related errors"""

    def __init__(self, message: str = "Insufficient permissions", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status.HTTP_403_FORBIDDEN, details)


class ValidationError(BudgetBrainException):
    """Data validation errors"""

    def __init__(self, message: str = "Validation failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status.HTTP_422_UNPROCESSABLE_ENTITY, details)


class ResourceNotFoundError(BudgetBrainException):
    """Resource not found errors"""

    def __init__(self, resource: str, resource_id: Any = None, details: Optional[Dict[str, Any]] = None):
        message = f"{resource} not found"
        if resource_id:
            message += f" with id {resource_id}"
        super().__init__(message, status.HTTP_404_NOT_FOUND, details)


class DatabaseError(BudgetBrainException):
    """Database operation errors"""

    def __init__(self, message: str = "Database operation failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status.HTTP_500_INTERNAL_SERVER_ERROR, details)


class ExternalServiceError(BudgetBrainException):
    """External service/API errors"""

    def __init__(self, service: str, message: str = "External service error", details: Optional[Dict[str, Any]] = None):
        super().__init__(f"{service}: {message}", status.HTTP_502_BAD_GATEWAY, details)


class RateLimitError(BudgetBrainException):
    """Rate limiting errors"""

    def __init__(self, message: str = "Rate limit exceeded", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status.HTTP_429_TOO_MANY_REQUESTS, details)


class FileProcessingError(BudgetBrainException):
    """File processing errors"""

    def __init__(self, message: str = "File processing failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status.HTTP_400_BAD_REQUEST, details)


class ConfigurationError(BudgetBrainException):
    """Configuration errors"""

    def __init__(self, message: str = "Configuration error", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status.HTTP_500_INTERNAL_SERVER_ERROR, details)


def handle_budgetbrain_exception(exc: BudgetBrainException) -> HTTPException:
    """Convert BudgetBrain exceptions to FastAPI HTTPException"""
    return HTTPException(
        status_code=exc.status_code,
        detail={
            "message": exc.message,
            "type": exc.__class__.__name__,
            "details": exc.details
        }
    )


def create_error_response(
    message: str,
    error_type: str = "UnknownError",
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    details: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Create standardized error response"""
    return {
        "success": False,
        "message": message,
        "error_type": error_type,
        "status_code": status_code,
        "details": details or {}
    }


def create_success_response(
    message: str,
    data: Optional[Any] = None,
    details: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Create standardized success response"""
    response = {
        "success": True,
        "message": message,
        "data": data
    }
    if details:
        response["details"] = details
    return response