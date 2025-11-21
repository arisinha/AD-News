from typing import List, Optional
from app.models.base import MongoBaseModel, PyObjectId
from pydantic import Field

class Topic(MongoBaseModel):
    title: str
    description: Optional[str] = None
    unified_summary: Optional[str] = None
    article_ids: List[PyObjectId] = []
    
    # Metadata
    category: Optional[str] = None
    trending_score: float = 0.0
    first_article_date: Optional[str] = None
    last_article_date: Optional[str] = None

    class Config:
        populate_by_name = True
