from typing import List, Optional
from app.crud.base import CRUDBase
from app.models.article import Article
from app.schemas.article import ArticleCreate, ArticleUpdate

class CRUDArticle(CRUDBase[Article, ArticleCreate, ArticleUpdate]):
    async def get_by_category(self, db, *, category: str, skip: int = 0, limit: int = 100) -> List[Article]:
        collection = db[self.collection_name]
        cursor = collection.find({"category": category}).sort("published_at", -1).skip(skip).limit(limit)
        docs = await cursor.to_list(length=limit)
        # Convert ObjectId to string for proper serialization
        for doc in docs:
            if '_id' in doc:
                doc['_id'] = str(doc['_id'])
            if 'topic_id' in doc and doc['topic_id']:
                doc['topic_id'] = str(doc['topic_id'])
        return [Article(**doc) for doc in docs]

    async def get_by_region(self, db, *, region: str, skip: int = 0, limit: int = 100) -> List[Article]:
        collection = db[self.collection_name]
        cursor = collection.find({"region": region}).sort("published_at", -1).skip(skip).limit(limit)
        docs = await cursor.to_list(length=limit)
        # Convert ObjectId to string for proper serialization
        for doc in docs:
            if '_id' in doc:
                doc['_id'] = str(doc['_id'])
            if 'topic_id' in doc and doc['topic_id']:
                doc['topic_id'] = str(doc['topic_id'])
        return [Article(**doc) for doc in docs]
    
    async def search(self, db, *, query: str, skip: int = 0, limit: int = 100) -> List[Article]:
        collection = db[self.collection_name]
        # Use regex search instead of text index for better compatibility
        regex_pattern = {"$regex": query, "$options": "i"}
        cursor = collection.find({
            "$or": [
                {"title": regex_pattern},
                {"description": regex_pattern},
                {"content": regex_pattern}
            ]
        }).skip(skip).limit(limit)
        docs = await cursor.to_list(length=limit)
        # Convert ObjectId to string for proper serialization
        for doc in docs:
            if '_id' in doc:
                doc['_id'] = str(doc['_id'])
            if 'topic_id' in doc and doc['topic_id']:
                doc['topic_id'] = str(doc['topic_id'])
        return [Article(**doc) for doc in docs]

article = CRUDArticle(Article, "articles")
