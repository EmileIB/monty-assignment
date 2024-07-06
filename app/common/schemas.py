from enum import Enum

from beanie import PydanticObjectId

from pydantic import (
    GetJsonSchemaHandler,
)
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema


class DBTable(str, Enum):
    Dummy = "dummy"


class MongoObjectID(PydanticObjectId):
    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler  # type: ignore
    ) -> JsonSchemaValue:
        return handler(schema)
