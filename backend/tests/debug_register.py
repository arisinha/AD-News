import asyncio
from app.crud.user import user as user_crud
from app.schemas.user import UserCreate
from app.db.mongodb import connect_to_mongo, close_mongo_connection, get_database
from app.core.config import settings
import traceback

async def debug_register():
    print(f"Connecting to MongoDB: {settings.MONGODB_URL.split('@')[-1] if '@' in settings.MONGODB_URL else '...'}")
    await connect_to_mongo()
    db = await get_database()
    
    email = "debug_user@example.com"
    username = "debug_user"
    password = "password123"
    
    user_in = UserCreate(email=email, username=username, password=password)
    
    try:
        from app.core.security import get_password_hash
        print("Testing password hash...")
        hashed = get_password_hash(password)
        print(f"Password hashed: {hashed[:10]}...")

        print("Attempting to create user...")
        user = await user_crud.create(db, obj_in=user_in)
        print(f"User created: {user.id}")
    except Exception as e:
        print("Error creating user:")
        traceback.print_exc()
    finally:
        await close_mongo_connection()

if __name__ == "__main__":
    asyncio.run(debug_register())
