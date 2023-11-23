from enum import Enum
from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings


class DatabaseConnectionType(Enum):
    DEFAULT: str = "default"
    TEMPORARY: str = "temporary"


class Settings(BaseSettings):
    database_url: PostgresDsn
    db_connection_type: DatabaseConnectionType = Field(alias='DATABASE_CONNECTION_TYPE')
    # TODO: uncomment after auth realization
    # secret_key: str
    # algorithm: str
    # access_token_expire_minutes: int

    class Config:
        env_file = ".env"
        
settings = Settings()
