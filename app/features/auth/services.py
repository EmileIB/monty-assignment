import jwt

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from typing import Annotated, Coroutine

from passlib.context import CryptContext

from app.core.settings import settings
from app.common.exceptions import (
    UnauthorizedException,
    BadRequestException,
    ForbiddenException,
)

from app.features.users.dao import UserDao
from .schemas import TokenData, Token, RegisterData

from app.features.users.models import UserDoc
from app.features.users.schemas import UserOut, UserOutWithToken


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"/{settings.API_VERSION}/auth/token")


class AuthService:
    @staticmethod
    def verify_password(plain_password, hashed_password) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password) -> str:
        return pwd_context.hash(password)

    @staticmethod
    async def authenticate_user(username: str, password: str) -> UserDoc | None:
        user = await UserDao.get_one({"username": username})
        if not user or not AuthService.verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        return encoded_jwt

    @staticmethod
    async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)]
    ) -> UserDoc:
        credentials_exception = UnauthorizedException("Could not validate credentials.")
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except InvalidTokenError:
            raise credentials_exception
        user = await UserDao.get_one({"username": token_data.username})
        if user is None:
            raise credentials_exception
        return user

    @staticmethod
    async def get_current_admin_user(
        get_current_user_coroutine: Annotated[
            Coroutine[any, any, UserDoc], Depends(get_current_user)
        ],
    ):
        current_user = await get_current_user_coroutine
        if not current_user.is_admin:
            raise ForbiddenException("Forbidden")
        return current_user

    @staticmethod
    async def login_for_access_token(login_data: OAuth2PasswordRequestForm) -> Token:
        user = await AuthService.authenticate_user(
            login_data.username, login_data.password
        )
        if not user:
            raise UnauthorizedException("Incorrect username or password")
        return await AuthService.generate_token(user.username)

    @staticmethod
    async def generate_token(username: str) -> Token:
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = AuthService.create_access_token(
            data={"sub": username}, expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")

    @staticmethod
    async def register(user_data: RegisterData) -> UserOutWithToken:
        _user = await UserDao.get_one({"username": user_data.username})
        if _user:
            raise BadRequestException("Username already exists")

        _user = await UserDao.create(
            username=user_data.username,
            full_name=user_data.full_name,
            hashed_password=AuthService.get_password_hash(user_data.password),
            is_admin=False,
        )

        return UserOutWithToken(
            **UserOut.model_validate(_user).model_dump(),
            token=await AuthService.generate_token(_user.username),
        )

    @staticmethod
    async def create_default_admin():
        _user = await UserDao.get_one({"username": settings.ADMIN_USERNAME})
        if _user:
            return
        await UserDao.create(
            username=settings.ADMIN_USERNAME,
            full_name="Admin",
            hashed_password=AuthService.get_password_hash(settings.ADMIN_PASSWORD),
            is_admin=True,
        )
        return
