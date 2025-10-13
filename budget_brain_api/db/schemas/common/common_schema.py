from pydantic import BaseModel
from typing import Any, Optional

class APIResponse(BaseModel):
    issuccess: bool
    message: str
    data: Optional[Any] = None
    error: Optional[str] = None