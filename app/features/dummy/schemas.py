from pydantic import BaseModel, ConfigDict, Field
from app.common.schemas import MongoObjectID


class DummyBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=100)

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class DummyIn(DummyBase):
    pass


class DummyOut(DummyBase):
    id: MongoObjectID
