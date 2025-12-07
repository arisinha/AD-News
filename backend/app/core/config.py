from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "AD News API"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "changethis"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    MONGODB_URL: str
    MONGODB_DB_NAME: str = "adnews"
    
    REDIS_URL: str = "redis://localhost:6379"
    
    NEWS_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    YOUTUBE_API_KEY: Optional[str] = None
    
    SENTRY_DSN: Optional[str] = None

    class Config:
        env_file = ".env"

settings = Settings()
