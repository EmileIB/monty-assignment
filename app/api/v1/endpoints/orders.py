from fastapi import APIRouter, status, Depends

from typing import Annotated
from app.features.auth.services import AuthService, UserDoc

from app.features.orders.services import OrderService
from app.features.orders.schemas import OrderOut, OrderStatusUpdateAdmin

from app.common.schemas import MongoObjectID


router = APIRouter(tags=["Order"], prefix="/orders")


@router.get("/orders", status_code=status.HTTP_200_OK)
async def get_orders(
    current_user: Annotated[UserDoc, Depends(AuthService.get_current_user)]
) -> list[OrderOut]:
    return await OrderService.get_orders(current_user)


@router.put(
    "/orders/{order_id}",
    status_code=status.HTTP_201_CREATED,
    summary="Update order status - Admin only",
)
async def update_order_status(
    order_id: MongoObjectID,
    new_status: OrderStatusUpdateAdmin,
    _current_user: Annotated[UserDoc, Depends(AuthService.get_current_admin_user)],
) -> OrderOut:
    return await OrderService.update_order_status(order_id, new_status)


@router.get("/orders/{order_id}", status_code=status.HTTP_200_OK)
async def get_order_by_id(
    order_id: MongoObjectID,
    current_user: Annotated[UserDoc, Depends(AuthService.get_current_user)],
) -> OrderOut:
    return await OrderService.get_order_by_id(order_id, current_user)
