from datetime import datetime, timezone
from passlib.context import CryptContext
from src.adapters.driven.database.base import generate_uuid, get_db


class GenericORM:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    db_client = get_db()
    collections = {
        "user": db_client["user"],
        "video": db_client["video"],
    }
    __collection__ = ""  # abstract, should be defined in subclasses

    @classmethod
    def find_all(cls, instance_class):
        collection = cls.collections[cls.__collection__]
        results = list(collection.find({}))
        return [instance_class(**result) for result in results]

    @classmethod
    def create(cls, data, instance_class):
        entity = cls.save(data, instance_class)
        return entity

    @classmethod
    def save(cls, entity, instance_class):
        collection = cls.collections[cls.__collection__]
        entity_dict = entity.__dict__.copy()
        if not entity_dict.get("id"):
            entity_dict["id"] = generate_uuid()
            entity_dict["created_at"] = datetime.now(timezone.utc)
        entity_dict["updated_at"] = datetime.now(timezone.utc)
        collection.update_one(
            {"id": entity_dict["id"]}, {"$set": entity_dict}, upsert=True
        )
        return instance_class(**entity_dict)

    @classmethod
    def find_by_id(cls, id, instance_class):
        collection = cls.collections[cls.__collection__]
        result = collection.find_one({"id": id})
        if result:
            return instance_class(**result)
        return None

    @classmethod
    def exists_by_id(cls, id):
        collection = cls.collections[cls.__collection__]
        return collection.find_one({"id": id}) is not None

    @classmethod
    def delete_by_id(cls, id):
        collection = cls.collections[cls.__collection__]
        collection.delete_one({"id": id})

    @classmethod
    def filter(cls, syntax, instance_class):
        collection = cls.collections[cls.__collection__]
        results = list(collection.find(syntax))
        return [instance_class(**result) for result in results]
