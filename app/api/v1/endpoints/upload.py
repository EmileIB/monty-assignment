from fastapi import UploadFile, File
from fastapi import APIRouter, Depends
from typing import Annotated

from app.features.auth.services import AuthService, UserDoc

from app.features.upload.services import UploadService
from app.features.upload.schemas import FileOut

router = APIRouter(tags=["Upload"], prefix="/upload")


@router.post("/image/single")
async def upload_single_image(
    _current_user: Annotated[UserDoc, Depends(AuthService.get_current_user)],
    image: UploadFile = File(...),
) -> FileOut:
    return await UploadService.upload_image(image)


@router.post("/images/multiple")
async def upload_multiple_images(
    _current_user: Annotated[UserDoc, Depends(AuthService.get_current_user)],
    images: list[UploadFile] = File(...),
) -> list[FileOut]:
    return await UploadService.upload_images(images)
