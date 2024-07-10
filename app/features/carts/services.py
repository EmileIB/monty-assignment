from .schemas import CartItemOut, CartItemUpdate, CartItemIn
from .dao import CartItemDao
from app.core.db import UserDoc

from app.common.schemas import MongoObjectID
from app.common.exceptions import NotFoundException

from app.features.products.services import ProductService


class CartItemService:

    @staticmethod
    async def get_cart_items(user: UserDoc) -> list[CartItemOut]:
        return [
            CartItemOut.model_validate(cart_item)
            for cart_item in await CartItemDao.get_all(
                filters={"user.id": user.id},
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

        product = await ProductService.get_product_by_id(item_data.product_id)
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
