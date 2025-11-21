from typing import List
from app.crud.base import CRUDBase
from app.models.favorite import Favorite
from app.schemas.favorite import FavoriteCreate, FavoriteBase
from bson import ObjectId

class CRUDFavorite(CRUDBase[Favorite, FavoriteCreate, FavoriteBase]):
    async def get_by_user(self, db, *, user_id: str, skip: int = 0, limit: int = 100) -> List[Favorite]:
        collection = db[self.collection_name]
        cursor = collection.find({"user_id": ObjectId(user_id)}).sort("created_at", -1).skip(skip).limit(limit)
        docs = await cursor.to_list(length=limit)
        return [Favorite(**doc) for doc in docs]

favorite = CRUDFavorite(Favorite, "favorites")
