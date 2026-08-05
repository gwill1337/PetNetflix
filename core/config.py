from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://myuser:1234@localhost:5432/mydb"


settings = Settings()
