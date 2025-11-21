from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from app.crud.topic import topic as topic_crud
from app.crud.article import article as article_crud
from app.schemas.topic import TopicResponse
from app.schemas.article import ArticleResponse
from app.db.mongodb import get_database
from bson import ObjectId

router = APIRouter()

@router.get("/", response_model=List[TopicResponse])
async def read_topics(
    db=Depends(get_database),
    skip: int = 0,
    limit: int = 10,
) -> Any:
    return await topic_crud.get_trending(db, limit=limit)

@router.get("/{topic_id}", response_model=TopicResponse)
async def read_topic(
    topic_id: str,
    db=Depends(get_database),
) -> Any:
    topic = await topic_crud.get(db, id=topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic

@router.get("/{topic_id}/articles", response_model=List[ArticleResponse])
async def read_topic_articles(
    topic_id: str,
    db=Depends(get_database),
) -> Any:
    topic = await topic_crud.get(db, id=topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    # Fetch articles by IDs
    # This is a bit inefficient, N+1 problem. Better to have a get_multi_by_ids in CRUD
    articles = []
    for art_id in topic.article_ids:
        art = await article_crud.get(db, id=art_id)
        if art:
            articles.append(art)
    return articles
