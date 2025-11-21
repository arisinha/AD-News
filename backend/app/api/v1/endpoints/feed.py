from typing import Any, List, Union
from fastapi import APIRouter, Depends
from app.api.v1.dependencies import get_current_user
from app.models.user import User
from app.crud.article import article as article_crud
from app.schemas.article import ArticleResponse
from app.db.mongodb import get_database

router = APIRouter()

@router.get("/", response_model=List[ArticleResponse])
async def read_feed(
    db=Depends(get_database),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 20,
) -> Any:
    # Logic to personalize feed based on user preferences
    # For now, just return latest articles
    # In real app: filter by categories, regions, etc.
    
    # Example: if user likes "technology", fetch tech news
    # categories = current_user.preferences.categories
    
    return await article_crud.get_multi(db, skip=skip, limit=limit)

@router.get("/category/{category}", response_model=List[ArticleResponse])
async def read_feed_by_category(
    category: str,
    db=Depends(get_database),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 20,
) -> Any:
    return await article_crud.get_by_category(db, category=category, skip=skip, limit=limit)

@router.get("/region/{region}", response_model=List[ArticleResponse])
async def read_feed_by_region(
    region: str,
    db=Depends(get_database),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 20,
) -> Any:
    return await article_crud.get_by_region(db, region=region, skip=skip, limit=limit)
