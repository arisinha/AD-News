from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.crud.user import user as user_crud
from app.schemas.user import Token, UserCreate, UserResponse, LoginRequest
from app.core.security import create_access_token
from app.core.config import settings
from app.db.mongodb import get_database

router = APIRouter()

@router.post("/login", response_model=Token)
async def login_json(
    login_data: LoginRequest,
    db=Depends(get_database)
) -> Any:
    """Login endpoint that accepts JSON body with username and password"""
    user = await user_crud.authenticate_by_username(
        db, username=login_data.username, password=login_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }



@router.post("/register", response_model=UserResponse)
async def register_user(
    *,
    db=Depends(get_database),
    user_in: UserCreate,
) -> Any:
    user = await user_crud.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    user = await user_crud.create(db, obj_in=user_in)
    
    # Convert User model to UserResponse
    return UserResponse(
        id=str(user.id),
        email=user.email,
        username=user.username,
        is_active=user.is_active,
        preferences={
            "categories": user.preferences.categories,
            "regions": user.preferences.regions,
            "language": user.preferences.language,
            "notifications_enabled": user.preferences.notifications_enabled,
            "dark_mode": user.preferences.dark_mode,
        }
    )
