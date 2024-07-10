from fastapi import APIRouter, status, Depends

from app.features.auth.services import AuthService

from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from app.features.auth.schemas import Token, RegisterData
from app.features.users.schemas import UserOutWithToken

router = APIRouter(tags=["Auth"], prefix="/auth")


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_data: RegisterData = Depends()) -> UserOutWithToken:
    return await AuthService.register(user_data)


@router.post("/token", status_code=status.HTTP_200_OK)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    return await AuthService.login_for_access_token(form_data)
