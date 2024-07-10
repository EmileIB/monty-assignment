from beanie import Document
from app.common.schemas import DBTable


class UserDoc(Document):
    username: str
    full_name: str
    hashed_password: str

    class Settings:
        name = DBTable.Users
        indexes = ["username"]
