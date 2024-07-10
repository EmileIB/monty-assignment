from fastapi import APIRouter, status, Depends, Body

from typing import Annotated
from app.features.auth.services import AuthService, UserDoc

from app.features.carts.services import CartItemService
from app.features.carts.schemas import CartItemOut, CartItemUpdate, CartItemIn

from app.common.schemas import MongoObjectID


router = APIRouter(tags=["Cart"], prefix="/cart")


@router.get("/items", status_code=status.HTTP_201_CREATED)
async def get_cart_items(
    current_user: Annotated[UserDoc, Depends(AuthService.get_current_user)]
) -> list[CartItemOut]:
    return await CartItemService.get_cart_items(current_user)


@router.put("/items/{cart_item_id}", status_code=status.HTTP_201_CREATED)
async def update_cart_item_quantity(
    cart_item_id: MongoObjectID,
    update_data: CartItemUpdate,
    current_user: Annotated[UserDoc, Depends(AuthService.get_current_user)],
) -> CartItemOut:
    return await CartItemService.update_cart_item(
        cart_item_id, user=current_user, update_data=update_data
    )


@router.post(
    "/items",
    status_code=status.HTTP_201_CREATED,
    description="Add item to cart. If it already exists, increase the quantity by the given amount.",
)
async def add_cart_item(
    item_data: Annotated[CartItemIn, Body(...)],
    current_user: Annotated[UserDoc, Depends(AuthService.get_current_user)],
) -> CartItemOut:
    return await CartItemService.add_cart_item(item_data=item_data, user=current_user)
