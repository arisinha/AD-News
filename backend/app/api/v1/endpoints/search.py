from typing import Any, List
from fastapi import APIRouter, Depends
from app.crud.article import article as article_crud
from app.schemas.article import ArticleResponse
from app.db.mongodb import get_database

router = APIRouter()

@router.get("/", response_model=List[ArticleResponse])
async def search_articles(
    q: str,
    db=Depends(get_database),
    skip: int = 0,
    limit: int = 20,
) -> Any:
    return await article_crud.search(db, query=q, skip=skip, limit=limit)
