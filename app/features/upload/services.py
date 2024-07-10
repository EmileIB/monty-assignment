import aiofiles
import os
import asyncio

from fastapi import FastAPI, UploadFile
from pathlib import Path

from uuid import uuid4

from app.common.exceptions import BadRequestException

from .schemas import FileOut

app = FastAPI()

# Ensure the 'uploads' directory exists
root_path = Path(__file__).parent.parent.parent.parent.absolute()
uploads_path = root_path / "static" / "uploads"
os.makedirs(uploads_path, exist_ok=True)


class UploadService:
    @staticmethod
    async def upload_file(file: UploadFile) -> FileOut:
        new_file_name = UploadService.format_new_file_name(file.filename)

        async with aiofiles.open(uploads_path / new_file_name, "wb") as f:
            await f.write(await file.read())

        return FileOut(original_name=file.filename, file_name=new_file_name)

    @staticmethod
    async def upload_files(files: list[UploadFile]) -> list[FileOut]:
        tasks = [UploadService.upload_file(file) for file in files]
        return list(await asyncio.gather(*tasks))

    @staticmethod
    async def upload_image(file: UploadFile) -> FileOut:
        if not file.filename.endswith((".png", ".jpg", ".jpeg")):
            raise BadRequestException(
                "Invalid image file. Please upload a valid image file (png, jpg, jpeg)"
            )

        return await UploadService.upload_file(file)

    @staticmethod
    async def upload_images(files: list[UploadFile]) -> list[FileOut]:
        tasks = [UploadService.upload_image(file) for file in files]
        return list(await asyncio.gather(*tasks))

    @staticmethod
    def format_new_file_name(file_name: str) -> str:
        return f"{uuid4()}_{Path(file_name).suffix}"
