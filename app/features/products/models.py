from beanie import Document, Link
from app.common.schemas import DBTable


from app.features.users.models import UserDoc
from app.features.upload.schemas import FileIn


class ProductDoc(Document):
    name: str
    description: str
    price: float

    images: list[FileIn] = []

    user: Link[UserDoc]

    class Settings:
        name = DBTable.Products
