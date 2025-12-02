from typing import Any, List, Union
from fastapi import APIRouter, Depends
from app.api.v1.dependencies import get_current_user
from app.models.user import User
from app.crud.article import article as article_crud
from app.schemas.article import ArticleResponse
from app.db.mongodb import get_database

router = APIRouter()

@router.get("/personalized", response_model=List[ArticleResponse])
async def read_personalized_feed(
    db=Depends(get_database),
    current_user: User = Depends(get_current_user),
    page: int = 1,
    size: int = 20,
) -> Any:
    """Get personalized feed based on user preferences"""
    skip = (page - 1) * size
    limit = size
    
    # Logic to personalize feed based on user preferences
    # For now, just return latest articles
    # In real app: filter by categories, regions, etc.
    
    # Example: if user likes "technology", fetch tech news
    # categories = current_user.preferences.categories
    
    return await article_crud.get_multi(db, skip=skip, limit=limit)

@router.get("/trending", response_model=List[ArticleResponse])
async def read_trending_feed(
    db=Depends(get_database),
    page: int = 1,
    size: int = 20,
) -> Any:
    """Get trending articles (most recent for now, can be enhanced with popularity metrics)"""
    skip = (page - 1) * size
    limit = size
    
    # For now, return latest articles
    # In production: sort by engagement metrics, views, shares, etc.
    return await article_crud.get_multi(db, skip=skip, limit=limit)

@router.get("/", response_model=List[ArticleResponse])
async def read_feed(
    db=Depends(get_database),
    current_user: User = Depends(get_current_user),
    page: int = 1,
    size: int = 20,
) -> Any:
    """General feed endpoint"""
    skip = (page - 1) * size
    limit = size
    return await article_crud.get_multi(db, skip=skip, limit=limit)

@router.get("/category/{category}", response_model=List[ArticleResponse])
async def read_feed_by_category(
    category: str,
    db=Depends(get_database),
    current_user: User = Depends(get_current_user),
    page: int = 1,
    size: int = 20,
) -> Any:
    skip = (page - 1) * size
    limit = size
    return await article_crud.get_by_category(db, category=category, skip=skip, limit=limit)

@router.get("/region/{region}", response_model=List[ArticleResponse])
async def read_feed_by_region(
    region: str,
    db=Depends(get_database),
    current_user: User = Depends(get_current_user),
    page: int = 1,
    size: int = 20,
) -> Any:
    skip = (page - 1) * size
    limit = size
    return await article_crud.get_by_region(db, region=region, skip=skip, limit=limit)
