from typing import (
    Optional,
    Dict,
    Any,
)

import dj_database_url
from pydantic import (
    BaseSettings,
    Field,
    validator,
)


class DatabaseSettings(BaseSettings):
    default: str = Field(..., env="DEFAULT_DATABASE_URL")

    class Config:
        env_file = ".env"

    @validator("*")
    def format_config_from_dsn(cls, value: Optional[str]):
        if value is None:
            return {}

        return dj_database_url.parse(value)


class GeneralSettings(BaseSettings):
    SECRET_KEY: str
    DEBUG: bool
    DATABASES: Dict[str, Any] = DatabaseSettings().dict()


class ProjectSettings(GeneralSettings):
    pass


settings: ProjectSettings = ProjectSettings(_env_file=".env")
