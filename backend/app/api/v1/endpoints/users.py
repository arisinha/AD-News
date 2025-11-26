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
    return UserResponse(
        id=str(current_user.id),
        email=current_user.email,
        username=current_user.username,
        is_active=current_user.is_active,
        preferences=UserPreferencesBase(
            categories=current_user.preferences.categories,
            regions=current_user.preferences.regions,
            language=current_user.preferences.language,
            notifications_enabled=current_user.preferences.notifications_enabled,
            dark_mode=current_user.preferences.dark_mode,
        )
    )

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
    return UserResponse(
        id=str(user.id),
        email=user.email,
        username=user.username,
        is_active=user.is_active,
        preferences=UserPreferencesBase(
            categories=user.preferences.categories,
            regions=user.preferences.regions,
            language=user.preferences.language,
            notifications_enabled=user.preferences.notifications_enabled,
            dark_mode=user.preferences.dark_mode,
        )
    )
