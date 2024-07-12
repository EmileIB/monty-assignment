from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorDatabase,
)

from beanie import init_beanie, Link  # type: ignore

from app.features.users.models import UserDoc
from app.features.products.models import ProductDoc
from app.features.carts.models import CartItemDoc
from app.features.orders.models import OrderDoc

from app.core.settings import settings

db_client: AsyncIOMotorClient | None = None


async def connect_and_init_db():
    global db_client
    db_client = AsyncIOMotorClient(settings.MONGO_URL)
    await init_beanie(
        db_client[settings.DB_NAME],
        document_models=[UserDoc, ProductDoc, CartItemDoc, OrderDoc],
    )


async def get_db() -> AsyncIOMotorDatabase:
    return db_client.get_database(settings.DB_NAME)


async def close_db_connection():
    global db_client
    if db_client is not None:
        db_client.close()
        db_client = None
