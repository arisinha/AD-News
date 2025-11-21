import redis.asyncio as redis
from app.core.config import settings

class RedisClient:
    client: redis.Redis = None

redis_client = RedisClient()

async def get_redis():
    return redis_client.client

async def connect_to_redis():
    redis_client.client = redis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)

async def close_redis_connection():
    await redis_client.client.close()
