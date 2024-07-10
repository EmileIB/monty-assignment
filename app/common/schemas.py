from enum import Enum

from beanie import PydanticObjectId as DefaultPydanticObjectId

from pydantic import (
    GetJsonSchemaHandler,
)
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema


class DBTable(str, Enum):
    Dummy = "dummy"
    Users = "users"
    Products = "products"
    Files = "files"
    CartItems = "cart_items"
    Carts = "carts"


class PydanticObjectId(DefaultPydanticObjectId):
    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler  # type: ignore
    ) -> JsonSchemaValue:
        return handler(schema)


MongoObjectID = PydanticObjectId
