from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from app.crud.article import article as article_crud
from app.db.mongodb import get_database
from app.services.summary_service import summary_service

router = APIRouter()

@router.post("/articles/{article_id}")
async def enrich_article(
    article_id: str,
    db=Depends(get_database),
) -> Any:
    """Generate AI summary, key points, and sentiment analysis for a specific article"""
    
    # Get the article
    article = await article_crud.get(db, id=article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    # Generate enrichment data
    text = f"{article.title}. {article.description or ''}. {article.content or ''}"
    enrichment = await summary_service.enrich_article(text)
    
    # Update the article
    collection = db["articles"]
    await collection.update_one(
        {"_id": article.id},
        {"$set": {
            "ai_summary": enrichment["summary"],
            "key_points": enrichment["key_points"],
            "sentiment_score": enrichment["sentiment_score"],
            "sentiment_label": enrichment["sentiment_label"]
        }}
    )
    
    return {
        "article_id": str(article.id),
        "title": article.title,
        "enrichment": enrichment
    }

@router.post("/articles")
async def enrich_all_articles(
    db=Depends(get_database),
) -> Any:
    """Generate AI summaries, key points, and sentiment analysis for all articles"""
    
    # Get all articles
    articles = await article_crud.get_multi(db, skip=0, limit=100)
    
    enriched_count = 0
    errors = []
    
    for article in articles:
        try:
            # Generate enrichment data
            text = f"{article.title}. {article.description or ''}. {article.content or ''}"
            enrichment = await summary_service.enrich_article(text)
            
            # Update the article
            collection = db["articles"]
            await collection.update_one(
                {"_id": article.id},
                {"$set": {
                    "ai_summary": enrichment["summary"],
                    "key_points": enrichment["key_points"],
                    "sentiment_score": enrichment["sentiment_score"],
                    "sentiment_label": enrichment["sentiment_label"]
                }}
            )
            enriched_count += 1
        except Exception as e:
            errors.append({
                "article_id": str(article.id),
                "title": article.title,
                "error": str(e)
            })
    
    return {
        "message": f"Successfully enriched {enriched_count} articles",
        "enriched_count": enriched_count,
        "total_articles": len(articles),
        "errors": errors
    }
