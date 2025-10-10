from pydantic import BaseModel


class UserCreate(BaseModel):     
    username: str
    password: str
    display_name: str


class UserResponse(BaseModel):
    username: str
    display_name: str
    id: int

    class Config:
        from_attributes = True
