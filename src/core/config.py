from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./minicms.db"
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "MiniCMS"

    class Config:
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
