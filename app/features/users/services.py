from .models import UserDoc

from app.common.schemas import MongoObjectID
from app.common.exceptions import NotFoundException


class UserService:

    @staticmethod
    async def get_all() -> list[UserDoc]:
        return await UserDoc.find().to_list()

    @staticmethod
    async def get_user_by_id(user_id: MongoObjectID) -> UserDoc:
        _user = await UserDoc.find_one({"_id": user_id})
        if not _user:
            raise NotFoundException("User not found")
        return _user

    @staticmethod
    async def get_one(query: dict) -> UserDoc | None:
        _user = await UserDoc.find_one(query)
        return _user if _user else None
