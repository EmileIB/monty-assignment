from typing import Type, TypeVar, Generic
from .schemas import MongoObjectID


T = TypeVar("T")


class BaseDao(Generic[T]):
    def __init__(self, document_class: Type[T]):
        self.document_class = document_class

    async def get_all(
        self, *, filters: dict[str, any] | None = None, fetch_links: bool = False
    ) -> list[T]:

        if filters is None:
            filters = {}
        return await self.document_class.find(
            filters, fetch_links=fetch_links
        ).to_list()

    async def create(self, **kwargs) -> T:
        _doc = self.document_class(**kwargs)
        return await self.document_class.insert_one(_doc)

    async def get_by_id(self, doc_id: MongoObjectID, fetch_links: bool = False) -> T:
        _doc = await self.document_class.get(doc_id, fetch_links=fetch_links)
        return _doc

    async def delete_by_id(self, doc_id: MongoObjectID) -> T:
        _doc = await self.document_class.get_by_id(doc_id)
        await _doc.delete()
        return _doc

    async def get_one(self, filters: dict[str, any], fetch_links: bool = False) -> T:
        _doc = await self.document_class.find_one(filters, fetch_links=fetch_links)
        return _doc

    @staticmethod
    async def update(doc: T, **kwargs) -> T:
        for key, value in kwargs.items():
            setattr(doc, key, value)
        await doc.save()
        return doc
