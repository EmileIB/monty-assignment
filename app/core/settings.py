from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MONGO_URL: str
    DB_NAME: str

    API_VERSION: str = "v1"

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    STRIPE_SECRET_KEY: str
    WEBHOOK_SECRET: str

    UPLOADS_URL: str

    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
