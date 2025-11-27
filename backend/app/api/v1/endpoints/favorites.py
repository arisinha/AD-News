from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from app.api.v1.dependencies import get_current_user
from app.models.user import User
from app.crud.favorite import favorite as favorite_crud
from app.schemas.favorite import FavoriteResponse, FavoriteCreate
from app.db.mongodb import get_database

router = APIRouter()

@router.get("/", response_model=List[FavoriteResponse])
async def read_favorites(
    db=Depends(get_database),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 20,
) -> Any:
    return await favorite_crud.get_by_user(db, user_id=str(current_user.id), skip=skip, limit=limit)

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
