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

    async def delete_by_id(self, doc_id: MongoObjectID) -> T | None:
        _doc = await self.document_class.get_by_id(doc_id)
        if not _doc:
            return None
        await _doc.delete()
        return _doc

    async def delete_one(
        self, filters: dict[str, any], fetch_links: bool = False
    ) -> T | None:
        _doc = await self.get_one(filters, fetch_links=fetch_links)
        if not _doc:
            return None
        await _doc.delete()
        return _doc

    async def delete_many(
        self, filters: dict[str, any], fetch_links: bool = False
    ) -> list[T]:
        _docs = await self.get_all(filters=filters, fetch_links=fetch_links)
        for _doc in _docs:
            await _doc.delete()
        return _docs

    async def get_one(self, filters: dict[str, any], fetch_links: bool = False) -> T:
        _doc = await self.document_class.find_one(filters, fetch_links=fetch_links)
        return _doc

    @staticmethod
    async def update(doc: T, **kwargs) -> T:
        """
        Can either send the updated doc directly to save it.
        Or, send the original document with the updated fields as kwargs.
        :param doc: Updated Document or Original Document
        :param kwargs: Updated Fields
        :return: Updated Document
        """
        for key, value in kwargs.items():
            setattr(doc, key, value)
        await doc.save()
        return doc
