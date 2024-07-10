from pydantic import BaseModel, ConfigDict, Field
from app.common.schemas import MongoObjectID

from app.features.upload.schemas import FileOut, FileIn


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    description: str = Field(..., min_length=1, max_length=150)
    price: float = Field(..., gt=0)

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class ProductIn(ProductBase):
    pass


class ProductOut(ProductBase):
    id: MongoObjectID
    images: list[FileOut] = []


class ProductUpdate(ProductBase):
    images: list[FileIn] = []
