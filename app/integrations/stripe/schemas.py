from pydantic import BaseModel, ConfigDict, Field
from enum import Enum

from app.common.schemas import MongoObjectID


class Currency(str, Enum):
    USD = "usd"


class ProductDataRequiredMetadata(BaseModel):
    product_id: MongoObjectID
    user_id: MongoObjectID

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class ProductData(BaseModel):
    name: str
    description: str | None = None
    images: list[str] = Field(default_factory=list, max_length=8)
    metadata: ProductDataRequiredMetadata

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class PriceData(BaseModel):
    currency: Currency = Currency.USD
    product_data: ProductData
    unit_amount: int = Field(..., gt=0)

    model_config = ConfigDict(
        from_attributes=True, arbitrary_types_allowed=True, use_enum_values=True
    )


class LineItem(BaseModel):
    price_data: PriceData
    quantity: int

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class CheckoutMetadata(BaseModel):
    user_id: MongoObjectID

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)
