from typing import List
from app.crud.base import CRUDBase
from app.models.topic import Topic
from app.schemas.topic import TopicCreate, TopicUpdate

class CRUDTopic(CRUDBase[Topic, TopicCreate, TopicUpdate]):
    async def get_trending(self, db, *, limit: int = 10) -> List[Topic]:
        collection = db[self.collection_name]
        cursor = collection.find().sort("trending_score", -1).limit(limit)
        docs = await cursor.to_list(length=limit)
        return [Topic(**doc) for doc in docs]

topic = CRUDTopic(Topic, "topics")
