from typing import Any, List, Dict
from fastapi import APIRouter, Depends, HTTPException
from app.api.v1.dependencies import get_current_user
from app.models.user import User
from app.crud.favorite import favorite as favorite_crud
from app.crud.article import article as article_crud
from app.schemas.favorite import FavoriteResponse, FavoriteCreate
from app.schemas.article import ArticleResponse
from app.db.mongodb import get_database

router = APIRouter()

@router.get("/")
async def read_favorites(
    db=Depends(get_database),
    current_user: User = Depends(get_current_user),
    page: int = 1,
    size: int = 20,
) -> Any:
    """Get user's favorite articles with pagination"""
    skip = (page - 1) * size
    limit = size
    
    # Get favorites for the user
    favorites = await favorite_crud.get_by_user(db, user_id=str(current_user.id), skip=skip, limit=limit)
    
    # Get the actual articles
    articles = []
    for fav in favorites:
        article = await article_crud.get(db, id=fav.article_id)
        if article:
            articles.append(ArticleResponse(
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
            ))
    
    # Get total count
    collection = db["favorites"]
    from bson import ObjectId
    total = await collection.count_documents({"user_id": ObjectId(current_user.id)})
    
    return {
        "items": articles,
        "total": total,
        "page": page,
        "size": size,
    }

@router.post("/", response_model=FavoriteResponse)
async def create_favorite(
    *,
    db=Depends(get_database),
    favorite_in: FavoriteCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Create new favorite.
    """
    return await favorite_crud.create(db, obj_in=favorite_in, user_id=str(current_user.id))

@router.delete("/{favorite_id}", response_model=FavoriteResponse)
async def delete_favorite(
    favorite_id: str,
    db=Depends(get_database),
    current_user: User = Depends(get_current_user),
) -> Any:
    fav = await favorite_crud.get(db, id=favorite_id)
    if not fav:
        raise HTTPException(status_code=404, detail="Favorite not found")
    if str(fav.user_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return await favorite_crud.remove(db, id=favorite_id)
