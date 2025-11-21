from typing import Optional, List
from app.models.base import MongoBaseModel, PyObjectId
from pydantic import Field

class Article(MongoBaseModel):
    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None
    url: str
    image_url: Optional[str] = None
    source_name: str
    published_at: str  # ISO format string from source
    
    # Categorization
    category: str
    region: Optional[str] = None
    
    # Analysis
    sentiment_score: float = 0.0  # -1.0 to 1.0
    sentiment_label: str = "neutral" # positive, negative, neutral
    relevance_score: float = 0.0
    
    # AI Generated
    ai_summary: Optional[str] = None
    key_points: List[str] = []
    
    # Relations
    topic_id: Optional[PyObjectId] = None

    class Config:
        populate_by_name = True
