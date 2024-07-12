from pydantic import BaseModel, ConfigDict, Field
from enum import Enum

from app.features.upload.schemas import FileBase
from app.common.schemas import MongoObjectID
from app.features.users.schemas import UserOut

from datetime import datetime


class OrderProduct(BaseModel):
    product_id: MongoObjectID | None = None
    name: str
    description: str
    price: float
    images: list[FileBase] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class OrderItem(BaseModel):
    product: OrderProduct
    quantity: int = Field(..., gt=0)

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class Address(BaseModel):
    country: str
    city: str | None = None
    line1: str | None = None
    line2: str | None = None
    postal_code: str | None = None
    state: str | None = None

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class ShippingDetails(BaseModel):
    name: str
    address: Address | None = None

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class CustomerDetails(BaseModel):
    name: str
    email: str
    phone: str
    address: Address | None = None

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class OrderStatus(str, Enum):
    Checkout = "checkout"  # Created checkout session
    Pending = "pending"  # Payment successful and order is pending
    InTransit = "in_transit"  # Order is in transit
    Complete = "complete"  # Order is delivered
    Expired = "expired"  # Order is expired (checkout expired, or new checkout created)


class OrderStatusUpdateAdmin(str, Enum):
    InTransit = "in_transit"
    Complete = "complete"


class OrderBase(BaseModel):
    products: list[OrderItem]
    stripe_checkout_session_id: str
    status: OrderStatus = OrderStatus.Checkout
    customer_details: CustomerDetails | None = None
    shipping_details: ShippingDetails | None = None
    created_at: datetime = datetime.now()


class OrderIn(OrderBase):
    pass


class OrderOut(OrderBase):
    id: MongoObjectID
    user: UserOut

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)
