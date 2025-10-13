from pydantic import BaseModel


class UserCreate(BaseModel):     
    username: str
    password: str
    display_name: str
    role : int = 1  # Default role as 'User'


class UserResponse(BaseModel):
    username: str
    display_name: str
    id: int

    class Config:
        from_attributes = True
