from fastapi import APIRouter, status, Response

from app.features.dummy.services import DummyService
from app.features.dummy.schemas import DummyIn, DummyOut

from app.common.schemas import MongoObjectID

router = APIRouter(tags=["Dummy"], prefix="/dummy")


@router.get("", status_code=status.HTTP_201_CREATED)
async def get_dummies() -> list[DummyOut]:
    return [
        DummyOut.model_validate(dummy) for dummy in await DummyService().get_dummies()
    ]


@router.get("/{dummy_id}", status_code=status.HTTP_200_OK)
async def get_dummy_by_id(dummy_id: MongoObjectID) -> DummyOut:
    return DummyOut.model_validate(await DummyService().get_dummy_by_id(dummy_id))


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_dummy(dummy: DummyIn) -> DummyOut:
    return DummyOut.model_validate(await DummyService().create_dummy(dummy))


@router.delete(
    "/{dummy_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response
)
async def delete_dummy_by_id(dummy_id: MongoObjectID) -> None:
    await DummyService().delete_dummy_by_id(dummy_id)
