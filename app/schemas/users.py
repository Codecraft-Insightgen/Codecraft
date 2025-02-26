from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserCreate(UserBase):
    password: str

    class Config:
        from_attributes = True

class Login(BaseModel):
    email: EmailStr
    password: str
