from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    jwt_secret: str = "change-this-to-a-long-random-string"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440

    database_url: str = "sqlite:///./app.db"

    openai_api_key: str = ""
    embedding_model: str = "text-embedding-3-small"
    chat_model: str = "gpt-4o-mini"

    upload_dir: str = "./uploads"
    chroma_path: str = "./chroma_store"

    frontend_origin: str = "http://localhost:5173"


settings = Settings()
