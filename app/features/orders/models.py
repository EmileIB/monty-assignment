from beanie import Document, Link
from app.common.schemas import DBTable
from app.features.users.models import UserDoc
from .schemas import OrderStatus, OrderItem, CustomerDetails, ShippingDetails

from datetime import datetime


class OrderDoc(Document):
    user: Link[UserDoc]
    products: list[OrderItem]
    stripe_checkout_session_id: str
    status: OrderStatus = OrderStatus.Checkout
    customer_details: CustomerDetails | None = None
    shipping_details: ShippingDetails | None = None
    created_at: datetime = datetime.now()

    class Settings:
        name = DBTable.Orders
        indexes = ["user_id", "stripe_checkout_session_id"]
