from pydantic import BaseModel, ConfigDict, Field, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class RegisterData(BaseModel):
    username: str
    password: str = Field(..., min_length=8)
    full_name: str

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)
