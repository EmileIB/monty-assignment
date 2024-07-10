from fastapi import APIRouter

from .endpoints import dummy, auth, users

router = APIRouter(prefix="/v1")

router.include_router(dummy.router)
router.include_router(auth.router)
router.include_router(users.router)
