from beanie import Document
from app.common.schemas import DBTable


class DummyDoc(Document):
    title: str
    description: str

    class Settings:
        name: DBTable.Dummy
