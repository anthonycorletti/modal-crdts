import os
from enum import Enum

from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    test = "test"
    local = "local"
    preview = "preview"
    production = "production"


environment = Environment(os.getenv("APP_ENV", Environment.local.value))
environment_file = f".env.{environment.value}"


class Settings(BaseSettings):
    ENV: Environment = Environment.local
    LOG_LEVEL: str = "DEBUG"
    DB_PATH: str = "ystore.db"

    model_config = SettingsConfigDict(
        env_prefix="app_",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_file=environment_file,
        extra="allow",
    )

    def is_environment(self, environment: Environment) -> bool:
        return self.ENV == environment

    def is_production(self) -> bool:
        return self.is_environment(Environment.production)


settings = Settings()
