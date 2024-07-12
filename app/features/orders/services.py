from .schemas import OrderIn, OrderOut, OrderStatus, MongoObjectID
from .dao import OrderDao

from app.features.users.models import UserDoc
from app.features.users.schemas import UserOut

from .schemas import ShippingDetails, CustomerDetails, OrderStatusUpdateAdmin
from app.common.exceptions import NotFoundException


from app.integrations.stripe.services import expire_session


class OrderService:
    @staticmethod
    async def create_order(order_data: OrderIn, user: UserDoc) -> OrderOut:
        await OrderService.expire_checkout_orders(user.id)
        order = await OrderDao.create(**order_data.model_dump(), user=user)
        return OrderOut(
            **order_data.model_dump(), id=order.id, user=UserOut.model_validate(user)
        )

    @staticmethod
    async def expire_checkout_orders(user_id: MongoObjectID):
        checkout_orders = await OrderDao.get_all(
            filters={"user._id": user_id, "status": OrderStatus.Checkout},
            fetch_links=True,
        )

        for order in checkout_orders:
            await expire_session(order.stripe_checkout_session_id)
            order.status = OrderStatus.Expired
            await OrderDao.update(order)

    @staticmethod
    async def process_order_paid(
        checkout_session_id: str,
        shipping_details: ShippingDetails,
        customer_details: CustomerDetails,
    ):
        from app.features.carts.services import CartItemService

        order = await OrderDao.get_one(
            filters={"stripe_checkout_session_id": checkout_session_id},
        )

        order.status = OrderStatus.Pending
        order.shipping_details = shipping_details
        order.customer_details = customer_details
        await OrderDao.update(order)
        await CartItemService.empty_cart(order.user.to_dict()["id"])

    @staticmethod
    async def get_orders(user: UserDoc) -> list[OrderOut]:

        filters = {"status": {"$nin": [OrderStatus.Expired, OrderStatus.Checkout]}}
        if not user.is_admin:
            filters["user._id"] = user.id

        return [
            OrderOut.model_validate(order)
            for order in await OrderDao.get_all(
                filters=filters,
                fetch_links=True,
            )
        ]

    @staticmethod
    async def update_order_status(
        order_id: MongoObjectID, new_status: OrderStatusUpdateAdmin
    ) -> OrderOut:
        order = await OrderDao.get_by_id(order_id)
        if not order:
            raise NotFoundException("Order not found")
        order.status = new_status
        await OrderDao.update(order)

        return await OrderService.get_order_by_id(order_id)

    @staticmethod
    async def get_order_by_id(
        order_id: MongoObjectID, user: UserDoc | None = None
    ) -> OrderOut:

        filters = {"_id": order_id}
        if user and not user.is_admin:
            filters["user._id"] = user.id

        order = await OrderDao.get_one(filters=filters, fetch_links=True)
        if not order:
            raise NotFoundException("Order not found")
        return OrderOut.model_validate(order)
