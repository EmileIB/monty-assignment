from .models import DummyDoc
from .schemas import DummyIn

from app.common.schemas import MongoObjectID
from app.common.exceptions import NotFoundException


class DummyService:

    @staticmethod
    async def get_dummies() -> list[DummyDoc]:
        return await DummyDoc.find().to_list()

    @staticmethod
    async def create_dummy(dummy: DummyIn) -> DummyDoc:
        _dummy = DummyDoc(**dummy.model_dump())
        return await DummyDoc.insert_one(_dummy)

    @staticmethod
    async def get_dummy_by_id(dummy_id: MongoObjectID) -> DummyDoc:
        _dummy = await DummyDoc.find_one({"_id": dummy_id})
        if not _dummy:
            raise NotFoundException("Dummy not found")
        return _dummy

    @staticmethod
    async def delete_dummy_by_id(dummy_id: MongoObjectID) -> None:
        _dummy = await DummyService.get_dummy_by_id(dummy_id)
        await _dummy.delete()
