from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class TopicBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: Optional[str] = None

class TopicCreate(TopicBase):
    pass

class TopicUpdate(TopicBase):
    unified_summary: Optional[str] = None
    trending_score: Optional[float] = None

class TopicResponse(TopicBase):
    id: str
    unified_summary: Optional[str] = None
    article_ids: List[str] = []
    trending_score: float
    first_article_date: Optional[str] = None
    last_article_date: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
