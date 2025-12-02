from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from app.crud.article import article as article_crud
from app.schemas.article import ArticleResponse
from app.db.mongodb import get_database

router = APIRouter()

@router.get("/", response_model=List[ArticleResponse])
async def read_articles(
    page: int = 1,
    size: int = 10,
    db=Depends(get_database),
) -> Any:
    skip = (page - 1) * size
    limit = size
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

@router.get("/search", response_model=List[ArticleResponse])
async def search_articles(
    q: str,
    page: int = 1,
    size: int = 20,
    db=Depends(get_database),
) -> Any:
    skip = (page - 1) * size
    limit = size
    articles = await article_crud.search(db, query=q, skip=skip, limit=limit)
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

@router.get("/{article_id}/unified-summary")
async def get_article_with_unified_summary(
    article_id: str,
    db=Depends(get_database),
) -> Any:
    """Get article with a comprehensive unified summary from multiple related sources"""
    from app.services.summary_service import summary_service
    
    # Get the main article
    article = await article_crud.get(db, id=article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    # Find related articles by category (same topic)
    related_articles = await article_crud.get_by_category(
        db, 
        category=article.category, 
        skip=0, 
        limit=5
    )
    
    # Filter to get different sources (exclude the current article)
    related_articles = [a for a in related_articles if str(a.id) != article_id][:4]
    
    # Prepare articles data for unified summary
    all_articles = [article] + related_articles
    articles_data = [
        {
            "title": a.title,
            "description": a.description,
            "content": a.content,
            "source_name": a.source_name,
        }
        for a in all_articles
    ]
    
    # Generate unified summary
    unified_data = await summary_service.generate_unified_summary(articles_data)
    
    # Return article with unified summary
    return {
        "article": ArticleResponse(
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
        ),
        "unified_summary": unified_data["unified_summary"],
        "key_insights": unified_data["key_insights"],
        "overall_sentiment": unified_data["overall_sentiment"],
        "sources_analyzed": unified_data["sources_count"],
        "related_articles": [
            {
                "id": str(a.id),
                "title": a.title,
                "source_name": a.source_name,
                "published_at": a.published_at,
            }
            for a in related_articles
        ]
    }

