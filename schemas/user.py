from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    full_name: str
    email: str
    profile_picture: Optional[str] = None  # Optional field for profile picture

class UserCreate(UserBase):
    password: str
    is_driver: bool
    nic_number: Optional[str] = None
    license_number: Optional[str] = None

class UserOut(BaseModel):
    id: int
    full_name: str
    nic_number: str
    license_number: str
    profile_picture: Optional[str] = None
    email: str

    class Config:
        from_attributes = True  # Pydantic v2 for ORM
        # or "orm_mode = True" if using Pydantic v1