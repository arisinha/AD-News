from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from app.crud.article import article as article_crud
from app.schemas.article import ArticleResponse
from app.db.mongodb import get_database

router = APIRouter()

@router.get("/", response_model=List[ArticleResponse])
async def read_articles(
    skip: int = 0,
    limit: int = 10,
    db=Depends(get_database),
) -> Any:
    articles = await article_crud.get_multi(db, skip=skip, limit=limit)
    return [
        ArticleResponse(
            id=str(article.id),
            title=article.title,
            description=article.description,
            content=article.content,
            author=article.author,
            url=article.url,
            image_url=article.image_url,
            source_name=article.source_name,
            published_at=article.published_at,
            category=article.category,
            region=article.region,
            sentiment_score=article.sentiment_score,
            sentiment_label=article.sentiment_label,
            relevance_score=article.relevance_score,
            ai_summary=article.ai_summary,
            key_points=article.key_points,
            topic_id=str(article.topic_id) if article.topic_id else None,
            created_at=article.created_at,
        )
        for article in articles
    ]

@router.get("/{article_id}", response_model=ArticleResponse)
async def read_article(
    article_id: str,
    db=Depends(get_database),
) -> Any:
    article = await article_crud.get(db, id=article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return ArticleResponse(
        id=str(article.id),
        title=article.title,
        description=article.description,
        content=article.content,
        author=article.author,
        url=article.url,
        image_url=article.image_url,
        source_name=article.source_name,
        published_at=article.published_at,
        category=article.category,
        region=article.region,
        sentiment_score=article.sentiment_score,
        sentiment_label=article.sentiment_label,
        relevance_score=article.relevance_score,
        ai_summary=article.ai_summary,
        key_points=article.key_points,
        topic_id=str(article.topic_id) if article.topic_id else None,
        created_at=article.created_at,
    )

