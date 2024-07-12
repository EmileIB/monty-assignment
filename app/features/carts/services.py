from .schemas import CartItemOut, CartItemUpdate, CartItemIn, CheckoutCartOut
from .dao import CartItemDao
from app.core.db import UserDoc

from app.common.schemas import MongoObjectID
from app.common.exceptions import NotFoundException, BadRequestException

from app.features.products.dao import ProductDao

from app.integrations.stripe.services import create_checkout_session
from app.integrations.stripe.schemas import (
    LineItem,
    PriceData,
    ProductData,
    ProductDataRequiredMetadata,
    CheckoutMetadata,
)

from app.core.settings import settings

from app.features.orders.schemas import OrderProduct, OrderItem, OrderIn
from app.features.orders.services import OrderService


class CartItemService:

    @staticmethod
    async def get_cart_items(user: UserDoc) -> list[CartItemOut]:
        return [
            CartItemOut.model_validate(cart_item)
            for cart_item in await CartItemDao.get_all(
                filters={"user._id": user.id},
                fetch_links=True,
            )
        ]

    @staticmethod
    async def get_cart_item_by_id(cart_item_id: MongoObjectID) -> CartItemOut:
        cart_item = await CartItemDao.get_by_id(cart_item_id, fetch_links=True)
        if not cart_item:
            raise NotFoundException("Cart item not found")
        return CartItemOut.model_validate(cart_item)

    @staticmethod
    async def update_cart_item(
        cart_item_id: MongoObjectID,
        *,
        user: UserDoc,
        update_data: CartItemUpdate,
    ) -> CartItemOut:
        cart_item = await CartItemDao.get_one(
            filters={"user._id": user.id, "_id": cart_item_id},
            fetch_links=True,
        )
        if not cart_item:
            raise NotFoundException("Cart item not found")

        cart_item.quantity = update_data.quantity
        _updated_item = await CartItemDao.update(cart_item)
        return CartItemOut.model_validate(_updated_item)

    @staticmethod
    async def add_cart_item(item_data: CartItemIn, *, user: UserDoc) -> CartItemOut:

        product = await ProductDao.get_by_id(item_data.product_id)
        if not product:
            raise NotFoundException("Product not found")

        cart_item = await CartItemDao.get_one(
            filters={"user._id": user.id, "product._id": item_data.product_id},
            fetch_links=True,
        )

        if cart_item:
            cart_item.quantity += item_data.quantity
            _updated_item = await CartItemDao.update(cart_item)
            return CartItemOut.model_validate(_updated_item)

        _item = await CartItemDao.create(
            user=user, product=product, quantity=item_data.quantity
        )

        return await CartItemService.get_cart_item_by_id(_item.id)

    @staticmethod
    async def delete_cart_item(cart_item_id: MongoObjectID, *, user: UserDoc) -> None:
        deleted_cart_item = await CartItemDao.delete_one(
            filters={"user._id": user.id, "_id": cart_item_id},
            fetch_links=True,
        )

        if not deleted_cart_item:
            raise NotFoundException("Cart item not found")

    @staticmethod
    async def checkout_cart(user: UserDoc) -> CheckoutCartOut:
        cart_items = await CartItemDao.get_all(
            filters={"user._id": user.id},
            fetch_links=True,
        )

        if not cart_items:
            raise BadRequestException("Cart is empty")

        line_items = [
            LineItem(
                price_data=PriceData(
                    product_data=ProductData(
                        name=cart_item.product.name,
                        description=cart_item.product.description,
                        images=[
                            f"{settings.UPLOADS_URL}/{image.file_name}"
                            for image in cart_item.product.images
                        ],
                        metadata=ProductDataRequiredMetadata(
                            product_id=cart_item.product.id,
                            user_id=cart_item.product.user.id,
                        ),
                    ),
                    unit_amount=int(cart_item.product.price * 100),
                ),
                quantity=cart_item.quantity,
            )
            for cart_item in cart_items
        ]

        metadata = CheckoutMetadata(user_id=user.id)

        session = await create_checkout_session(line_items, metadata)

        order_items = [
            OrderItem(
                product=OrderProduct(
                    product_id=item.product.id,
                    name=item.product.name,
                    description=item.product.description,
                    price=item.product.price,
                    images=item.product.images,
                ),
                quantity=item.quantity,
            )
            for item in cart_items
        ]

        order = OrderIn(
            products=order_items,
            stripe_checkout_session_id=session.id,
        )

        await OrderService.create_order(order_data=order, user=user)

        return CheckoutCartOut(url=session.url)

    @staticmethod
    async def empty_cart(user: UserDoc | str | MongoObjectID) -> None:
        user_id = user.id if isinstance(user, UserDoc) else MongoObjectID(user)
        await CartItemDao.delete_many(filters={"user._id": user_id}, fetch_links=True)
