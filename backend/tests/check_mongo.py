import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

async def check_mongo():
    url = os.getenv("MONGODB_URL")
    print(f"Connecting to {url}...")
    client = AsyncIOMotorClient(url)
    try:
        await client.admin.command('ping')
        print("MongoDB connection successful!")
    except Exception as e:
        print(f"MongoDB connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(check_mongo())
