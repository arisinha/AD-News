from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class FavoriteBase(BaseModel):
    article_id: str
    collection_name: Optional[str] = "default"

class FavoriteCreate(FavoriteBase):
    pass

class FavoriteResponse(FavoriteBase):
    id: str
    user_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True
