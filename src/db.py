from motor.motor_asyncio import AsyncIOMotorClient

from config import (
    MONGODB_URL, MAX_CONNECTIONS_COUNT, MIN_CONNECTIONS_COUNT,
    DB_NAME,
)


class DataBase:
    client: AsyncIOMotorClient = None


_db = DataBase()


async def get_database() -> AsyncIOMotorClient:
    return _db.client[DB_NAME]


async def connect_to_mongo():
    _db.client = AsyncIOMotorClient(
        str(MONGODB_URL),
        maxPoolSize=MAX_CONNECTIONS_COUNT,
        minPoolSize=MIN_CONNECTIONS_COUNT
    )


async def close_mongo_connection():
    await _db.client.close()
