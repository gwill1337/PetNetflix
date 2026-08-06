from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://myuser:1234@localhost:5432/mydb"

    jwt_key: str = "7ca122f85929901e408265204aa46d4bbb62f362e9f49afa6ce492e51fa82655"
    jwt_algorithm: str = "HS256"


settings = Settings()
