from pydantic import BaseModel, ConfigDict
from app.common.schemas import MongoObjectID

from app.features.auth.schemas import Token


class UserBase(BaseModel):
    username: str
    full_name: str | None = None

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class UserInDB(UserBase):
    id: MongoObjectID
    hashed_password: str


class UserOut(UserBase):
    id: MongoObjectID


class UserOutWithToken(UserOut):
    token: Token
