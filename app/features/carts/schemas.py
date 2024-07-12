from pydantic import BaseModel, ConfigDict, Field
from app.common.schemas import MongoObjectID
from enum import Enum

from app.features.products.schemas import ProductOut


class CartItemBase(BaseModel):
    quantity: int = Field(..., gt=0)
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class CartItemIn(CartItemBase):
    product_id: MongoObjectID


class CartItemOut(CartItemBase):
    id: MongoObjectID
    product: ProductOut


class CartItemUpdate(CartItemBase):
    pass


class CheckoutCartOut(BaseModel):
    url: str
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)
