from fastapi import APIRouter

from .endpoints import dummy

router = APIRouter(prefix="/v1")

router.include_router(dummy.router)
