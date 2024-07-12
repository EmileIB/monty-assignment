from fastapi import APIRouter, status, Response, Depends, File, UploadFile, Form, Body

from typing import Annotated
from app.features.auth.services import AuthService, UserDoc

from app.features.products.services import ProductService
from app.features.products.schemas import ProductIn, ProductOut, ProductUpdate

from app.common.schemas import MongoObjectID

router = APIRouter(tags=["Product"], prefix="/products")


@router.get("", status_code=status.HTTP_201_CREATED)
async def get_products() -> list[ProductOut]:
    return await ProductService.get_products()


@router.get("/{product_id}", status_code=status.HTTP_200_OK)
async def get_product_by_id(product_id: MongoObjectID) -> ProductOut:
    return await ProductService.get_product_by_id(product_id)


@router.post(
    "", status_code=status.HTTP_201_CREATED, summary="Create Product - Admin Only"
)
async def create_product(
    current_user: Annotated[UserDoc, Depends(AuthService.get_current_admin_user)],
    name: Annotated[str, Form(...)],
    price: Annotated[float, Form(...)],
    description: Annotated[str, Form(...)],
    images: list[UploadFile] = File(...),
) -> ProductOut:
    product_data = ProductIn(name=name, price=price, description=description)
    return await ProductService.create_product(
        product_data=product_data, user=current_user, images=images
    )


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    summary="Delete Product By Id - Admin Only",
)
async def delete_product_by_id(
    _current_user: Annotated[UserDoc, Depends(AuthService.get_current_admin_user)],
    product_id: MongoObjectID,
) -> None:
    await ProductService.delete_product_by_id(product_id)


@router.put(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    summary="Update Product - Admin Only",
)
async def update_product(
    _current_user: Annotated[UserDoc, Depends(AuthService.get_current_admin_user)],
    product_data: Annotated[ProductUpdate, Body(...)],
    product_id: MongoObjectID,
) -> ProductOut:
    return await ProductService.update_product(
        product_id=product_id, update_data=product_data
    )
