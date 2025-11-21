from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from pydantic import BaseModel
from app.models.base import MongoBaseModel
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId

ModelType = TypeVar("ModelType", bound=MongoBaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], collection_name: str):
        self.model = model
        self.collection_name = collection_name

    async def get(self, db, id: Any) -> Optional[ModelType]:
        collection: AsyncIOMotorCollection = db[self.collection_name]
        doc = await collection.find_one({"_id": ObjectId(id)})
        if doc:
            return self.model(**doc)
        return None

    async def get_multi(
        self, db, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        collection: AsyncIOMotorCollection = db[self.collection_name]
        cursor = collection.find().skip(skip).limit(limit)
        docs = await cursor.to_list(length=limit)
        return [self.model(**doc) for doc in docs]

    async def create(self, db, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = obj_in.model_dump()
        collection: AsyncIOMotorCollection = db[self.collection_name]
        result = await collection.insert_one(obj_in_data)
        created_doc = await collection.find_one({"_id": result.inserted_id})
        return self.model(**created_doc)

    async def update(
        self,
        db,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = db_obj.model_dump()
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        for field in obj_data:
            if field in update_data:
                obj_data[field] = update_data[field]
                
        collection: AsyncIOMotorCollection = db[self.collection_name]
        await collection.update_one(
            {"_id": db_obj.id}, {"$set": update_data}
        )
        updated_doc = await collection.find_one({"_id": db_obj.id})
        return self.model(**updated_doc)

    async def remove(self, db, *, id: Any) -> Optional[ModelType]:
        collection: AsyncIOMotorCollection = db[self.collection_name]
        doc = await collection.find_one({"_id": ObjectId(id)})
        if doc:
            await collection.delete_one({"_id": ObjectId(id)})
            return self.model(**doc)
        return None
