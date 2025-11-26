from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, articles, topics, feed, search, favorites, seed

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/user", tags=["users"])
api_router.include_router(articles.router, prefix="/articles", tags=["articles"])
api_router.include_router(topics.router, prefix="/topics", tags=["topics"])
api_router.include_router(feed.router, prefix="/feed", tags=["feed"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(favorites.router, prefix="/user/favorites", tags=["favorites"])
api_router.include_router(seed.router, prefix="/seed", tags=["seed"])

