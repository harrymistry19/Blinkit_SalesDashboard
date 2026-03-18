from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    groq_api_key: str | None = None
    groq_model: str = "llama-3.3-70b-versatile"
    max_upload_mb: int = 10

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
