from fastapi import APIRouter, Depends
from typing import Annotated

from app.features.auth.services import AuthService, UserDoc
from app.features.users.schemas import UserOut

router = APIRouter(tags=["Users"], prefix="/users")


@router.get("/me", response_model=UserOut)
async def get_users_me(
    current_user: Annotated[UserDoc, Depends(AuthService.get_current_user)],
):
    return current_user
