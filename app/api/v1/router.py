from fastapi import APIRouter

from .endpoints import auth, users, products, upload, carts, stripe, orders

router = APIRouter(prefix="/v1")

router.include_router(auth.router)
router.include_router(users.router)
router.include_router(products.router)
router.include_router(upload.router)
router.include_router(carts.router)
router.include_router(stripe.router)
router.include_router(orders.router)
