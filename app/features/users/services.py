from .models import UserDoc
from .dao import UserDao
from .schemas import UserOut

from app.common.schemas import MongoObjectID
from app.common.exceptions import NotFoundException


class UserService:

    @staticmethod
    async def get_all_users() -> list[UserOut]:
        return [UserOut.model_validate(user) for user in await UserDao.get_all()]

    @staticmethod
    async def get_user_by_id(user_id: MongoObjectID) -> UserOut:
        _user = await UserDao.get_by_id(user_id)
        if not _user:
            raise NotFoundException("User not found")
        return _user

    @staticmethod
    async def get_one(query: dict) -> UserDoc | None:
        _user = await UserDoc.find_one(query)
        return _user if _user else None

    @staticmethod
    async def get_by_username(username: str) -> UserOut | None:
        _user = await UserDao.get_one(username=username)
        return UserOut.model_validate(_user)
