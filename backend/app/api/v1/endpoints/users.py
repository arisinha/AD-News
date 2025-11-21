from typing import Any
from fastapi import APIRouter, Depends, Body
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate, UserPreferencesBase
from app.api.v1.dependencies import get_current_user
from app.crud.user import user as user_crud
from app.db.mongodb import get_database

router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def read_user_me(
    current_user: User = Depends(get_current_user),
) -> Any:
    return current_user

@router.get("/preferences", response_model=UserPreferencesBase)
async def read_user_preferences(
    current_user: User = Depends(get_current_user),
) -> Any:
    return current_user.preferences

@router.put("/preferences", response_model=UserResponse)
async def update_user_preferences(
    *,
    db=Depends(get_database),
    preferences: UserPreferencesBase,
    current_user: User = Depends(get_current_user),
) -> Any:
    user_update = UserUpdate(preferences=preferences)
    user = await user_crud.update(db, db_obj=current_user, obj_in=user_update)
    return user
