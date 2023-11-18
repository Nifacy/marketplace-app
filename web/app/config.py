from pydantic import PostgresDsn, BaseSettings

class Settings(BaseSettings):
    database_url: PostgresDsn
    # TODO: uncomment after auth realization
    # secret_key: str
    # algorithm: str
    # access_token_expire_minutes: int

    class Config:
        env_file = ".env"
        
settings = Settings()
