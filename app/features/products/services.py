from fastapi import UploadFile

from .schemas import ProductIn, ProductOut, ProductUpdate
from .dao import ProductDao
from .models import ProductDoc


from app.common.schemas import MongoObjectID
from app.common.exceptions import NotFoundException

from app.core.db import UserDoc

from app.features.upload.services import UploadService


class ProductService:

    @staticmethod
    async def get_products(user: UserDoc, sold_by_me: bool = True) -> list[ProductOut]:
        return [
            ProductOut.model_validate(product)
            for product in await ProductDao.get_all(
                filters=(
                    {"user._id": user.id}
                    if sold_by_me
                    else {"user._id": {"$ne": user.id}}
                ),
                fetch_links=True,
            )
        ]

    @staticmethod
    async def create_product(
        *, product_data: ProductIn, user: UserDoc, images: list[UploadFile]
    ) -> ProductOut:

        _product = await ProductDao.create(
            **product_data.model_dump(),
            user=user,
            images=await UploadService.upload_images(images)
        )

        return ProductOut.model_validate(_product)

    @staticmethod
    async def get_product_by_id(product_id: MongoObjectID) -> ProductOut:
        _product = await ProductDao.get_by_id(product_id)
        if not _product:
            raise NotFoundException("Product not found")

        return ProductOut.model_validate(_product)

    @staticmethod
    async def delete_product_by_id(product_id: MongoObjectID) -> None:
        _deleted_product = await ProductDao.delete_by_id(product_id)
        if not _deleted_product:
            raise NotFoundException("Product not found")

    @staticmethod
    async def update_product(
        product_id: MongoObjectID,
        *,
        update_data: ProductUpdate,
        user_id: MongoObjectID | None = None
    ) -> ProductOut:
        _product = await ProductDao.get_one(
            {"_id": product_id, "user._id": user_id},
            fetch_links=True,
        )

        if not _product:
            raise NotFoundException("Product not found")

        _updated_product = await ProductDao.update(_product, **update_data.model_dump())
        return ProductOut.model_validate(_updated_product)
