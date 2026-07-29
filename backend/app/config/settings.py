from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str
    app_version: str

    openai_api_key: str

    database_url: str

    qdrant_url: str

    jwt_secret: str
    jwt_algorithm: str
    jwt_expire_minutes: int

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )


settings = Settings()