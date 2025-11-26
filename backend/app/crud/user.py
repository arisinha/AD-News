from typing import Optional
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_by_email(self, db, *, email: str) -> Optional[User]:
        collection = db[self.collection_name]
        doc = await collection.find_one({"email": email})
        if doc:
            return User(**doc)
        return None

    async def create(self, db, *, obj_in: UserCreate) -> User:
        from app.models.user import UserPreferences
        
        obj_in_data = obj_in.model_dump()
        password = obj_in_data.pop("password")
        obj_in_data["hashed_password"] = get_password_hash(password)
        
        # Initialize preferences with default values if not provided
        if "preferences" not in obj_in_data or obj_in_data["preferences"] is None:
            obj_in_data["preferences"] = UserPreferences().model_dump()
        
        collection = db[self.collection_name]
        result = await collection.insert_one(obj_in_data)
        created_doc = await collection.find_one({"_id": result.inserted_id})
        return User(**created_doc)

    async def get_by_username(self, db, *, username: str) -> Optional[User]:
        collection = db[self.collection_name]
        doc = await collection.find_one({"username": username})
        if doc:
            return User(**doc)
        return None

    async def authenticate(self, db, *, email: str, password: str) -> Optional[User]:
        user = await self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    async def authenticate_by_username(self, db, *, username: str, password: str) -> Optional[User]:
        user = await self.get_by_username(db, username=username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

user = CRUDUser(User, "users")
