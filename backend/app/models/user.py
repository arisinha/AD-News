from typing import List, Optional
from pydantic import EmailStr, Field
from app.models.base import MongoBaseModel
from datetime import datetime

class UserPreferences(MongoBaseModel):
    categories: List[str] = []
    regions: List[str] = []
    language: str = "es"
    notifications_enabled: bool = True
    dark_mode: bool = False

class User(MongoBaseModel):
    email: EmailStr
    username: str
    hashed_password: str
    preferences: UserPreferences = Field(default_factory=UserPreferences)
    last_login: Optional[datetime] = None
    is_active: bool = True
    is_superuser: bool = False

    class Config:
        populate_by_name = True
