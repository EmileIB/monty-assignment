from beanie import Document, Link
from app.common.schemas import DBTable

from app.features.products.models import ProductDoc
from app.features.users.models import UserDoc


class CartItemDoc(Document):
    user: Link[UserDoc]
    product: Link[ProductDoc]
    quantity: int

    class Settings:
        name = DBTable.CartItems
        indexes = ["product"]
