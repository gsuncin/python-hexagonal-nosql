import uuid
from src.core import settings

from pymongo import MongoClient, ASCENDING


def get_db() -> MongoClient:
    """
    Return mongo database
    """
    client = MongoClient(settings.DATABASE_URL, tz_aware=True)
    return client[settings.DATABASE_NAME]


def generate_uuid():
    return str(uuid.uuid4())
