from pydantic import BaseModel, ConfigDict


class FileBase(BaseModel):
    original_name: str
    file_name: str

    model_config = ConfigDict(from_attributes=True)


class FileIn(FileBase):
    pass


class FileOut(FileBase):
    pass
