from typing import Optional, List
from pydantic import BaseModel, EmailStr

# Shared properties
class UserPreferencesBase(BaseModel):
    categories: Optional[List[str]] = None
    regions: Optional[List[str]] = None
    language: Optional[str] = None
    notifications_enabled: Optional[bool] = None
    dark_mode: Optional[bool] = None

class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    is_active: Optional[bool] = True

# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    username: str
    password: str

# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None
    preferences: Optional[UserPreferencesBase] = None

# Properties to return to client
class UserResponse(UserBase):
    id: str
    preferences: UserPreferencesBase
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
