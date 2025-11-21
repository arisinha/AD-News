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
    # Create favorite with user_id
    # Note: In a real app, we should check if it already exists
    fav_data = favorite_in.model_dump()
    fav_data["user_id"] = current_user.id
    
    # We need to adapt the CRUD create to handle this or create a specific method
    # For simplicity, let's assume we can pass the dict with user_id
    # But our CRUD expects Pydantic model.
    # Let's do it manually here or update CRUD.
    # Updating CRUD is better but for now let's hack it slightly by creating a new model instance
    
    # Actually, let's just use the CRUD create but we need to inject user_id.
    # The schema FavoriteCreate doesn't have user_id.
    # We can create a new dict and pass it to the model directly if we bypass CRUD or update CRUD.
    
    # Let's use the collection directly for this specific case to be quick, or better:
    # Create a Favorite internal model
    from app.models.favorite import Favorite
    
    fav = Favorite(**fav_data)
    collection = db["favorites"]
    result = await collection.insert_one(fav.model_dump(by_alias=True))
    created_doc = await collection.find_one({"_id": result.inserted_id})
    return Favorite(**created_doc)

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
