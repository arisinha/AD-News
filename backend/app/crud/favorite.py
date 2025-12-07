from typing import List, Optional, Any
from app.crud.base import CRUDBase
from app.models.favorite import Favorite
from app.schemas.favorite import FavoriteCreate, FavoriteBase
from bson import ObjectId

class CRUDFavorite(CRUDBase[Favorite, FavoriteCreate, FavoriteBase]):
    async def get_by_user(self, db, *, user_id: str, skip: int = 0, limit: int = 100) -> List[Favorite]:
        collection = db[self.collection_name]
        cursor = collection.find({"user_id": ObjectId(user_id)}).sort("created_at", -1).skip(skip).limit(limit)
        docs = await cursor.to_list(length=limit)
        # Convert ObjectId to string for proper serialization
        for doc in docs:
            if '_id' in doc:
                doc['_id'] = str(doc['_id'])
            if 'user_id' in doc and doc['user_id']:
                doc['user_id'] = str(doc['user_id'])
            if 'article_id' in doc and doc['article_id']:
                doc['article_id'] = str(doc['article_id'])
        return [Favorite(**doc) for doc in docs]

    async def create(self, db, *, obj_in: FavoriteCreate, user_id: str) -> Favorite:
        obj_in_data = obj_in.model_dump()
        obj_in_data["user_id"] = ObjectId(user_id)
        collection = db[self.collection_name]
        result = await collection.insert_one(obj_in_data)
        created_doc = await collection.find_one({"_id": result.inserted_id})
        # Convert ObjectId to string for proper serialization
        if created_doc and '_id' in created_doc:
            created_doc['_id'] = str(created_doc['_id'])
            if 'user_id' in created_doc and created_doc['user_id']:
                created_doc['user_id'] = str(created_doc['user_id'])
            if 'article_id' in created_doc and created_doc['article_id']:
                created_doc['article_id'] = str(created_doc['article_id'])
        return Favorite(**created_doc)

    async def get(self, db, *, id: Any) -> Optional[Favorite]:
        """Override get to properly convert user_id to string"""
        collection = db[self.collection_name]
        doc = await collection.find_one({"_id": ObjectId(id)})
        if doc:
            if '_id' in doc:
                doc['_id'] = str(doc['_id'])
            if 'user_id' in doc and doc['user_id']:
                doc['user_id'] = str(doc['user_id'])
            if 'article_id' in doc and doc['article_id']:
                doc['article_id'] = str(doc['article_id'])
            return Favorite(**doc)
        return None

    async def remove(self, db, *, id: Any) -> Optional[Favorite]:
        """Override remove to properly convert user_id to string"""
        collection = db[self.collection_name]
        doc = await collection.find_one({"_id": ObjectId(id)})
        if doc:
            await collection.delete_one({"_id": ObjectId(id)})
            # Convert ObjectId to string for proper serialization
            if '_id' in doc:
                doc['_id'] = str(doc['_id'])
            if 'user_id' in doc and doc['user_id']:
                doc['user_id'] = str(doc['user_id'])
            if 'article_id' in doc and doc['article_id']:
                doc['article_id'] = str(doc['article_id'])
            return Favorite(**doc)
        return None

favorite = CRUDFavorite(Favorite, "favorites")

