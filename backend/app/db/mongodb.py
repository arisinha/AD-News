from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None

db = MongoDB()

async def get_database():
    return db.db

async def connect_to_mongo():
    import certifi
    import ssl
    
    # Create SSL context with certifi certificates
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    db.client = AsyncIOMotorClient(
        settings.MONGODB_URL,
        tls=True,
        tlsCAFile=certifi.where(),
        tlsAllowInvalidCertificates=True,
        tlsAllowInvalidHostnames=True
    )
    db.db = db.client[settings.MONGODB_DB_NAME]

async def close_mongo_connection():
    db.client.close()
