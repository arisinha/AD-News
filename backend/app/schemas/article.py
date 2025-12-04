from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class ArticleBase(BaseModel):
    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None
    url: str
    image_url: Optional[str] = None
    source_name: str
    published_at: str
    category: str
    region: Optional[str] = None

class ArticleCreate(ArticleBase):
    pass

class ArticleUpdate(ArticleBase):
    pass

class ArticleResponse(ArticleBase):
    id: str
    sentiment_score: float
    sentiment_label: str
    relevance_score: float
    ai_summary: Optional[str] = None
    key_points: List[str] = []
    topic_id: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class FeedResponse(BaseModel):
    items: List[ArticleResponse]
    total: int
    page: int
    size: int
    pages: int
