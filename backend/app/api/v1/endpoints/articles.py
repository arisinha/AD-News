from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from app.crud.article import article as article_crud
from app.schemas.article import ArticleResponse
from app.db.mongodb import get_database

router = APIRouter()

@router.get("/{article_id}", response_model=ArticleResponse)
async def read_article(
    article_id: str,
    db=Depends(get_database),
) -> Any:
    article = await article_crud.get(db, id=article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article
