import redis.asyncio as redis
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class RedisClient:
    client: redis.Redis = None

redis_client = RedisClient()

async def get_redis():
    return redis_client.client

async def connect_to_redis():
    try:
        redis_client.client = redis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)
        # Test connection
        await redis_client.client.ping()
        logger.info("Successfully connected to Redis")
    except Exception as e:
        logger.warning(f"Redis connection failed: {e}. Continuing without Redis cache.")
        redis_client.client = None

async def close_redis_connection():
    if redis_client.client:
        try:
            await redis_client.client.close()
            logger.info("Redis connection closed")
        except Exception as e:
            logger.warning(f"Error closing Redis connection: {e}")
