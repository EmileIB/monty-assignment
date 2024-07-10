from pydantic import BaseModel, ConfigDict, Field, EmailStr
from app.common.schemas import MongoObjectID


class UserBase(BaseModel):
    username: str
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(UserBase):
    id: MongoObjectID
    hashed_password: str


class UserOut(UserBase):
    id: MongoObjectID
