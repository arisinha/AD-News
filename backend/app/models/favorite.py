from typing import Optional
from app.models.base import MongoBaseModel, PyObjectId
from pydantic import Field

class Favorite(MongoBaseModel):
    user_id: PyObjectId
    article_id: PyObjectId
    collection_name: str = "default" # e.g., "Read Later", "Favorites"
    
    class Config:
        populate_by_name = True
