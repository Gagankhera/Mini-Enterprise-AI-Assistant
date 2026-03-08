"""Application configuration using pydantic-settings."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # OpenAI Configuration
    openai_api_key: str

    # Langsmith configuration
    langsmith_tracing_v2: bool = True
    langsmith_api_key: str
    langsmith_project: str = "Mini Enterprise AI Assistant"
    langsmith_endpoint: str = "https://api.smith.langchain.com"

    # Document Processing Settings
    chunk_size: int = 1000
    chunk_overlap: int = 200

    # Model Configuration
    embedding_model: str = "text-embedding-3-small"
    llm_model: str = "gpt-4o-mini"
    llm_temperature: float = 0.0

    # Retrieval Settings
    retrieval_k: int = 4

    # Logging
    log_level: str = "INFO"

    # API Settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # Application Info
    app_name: str = "Mini Enterprise AI Assistant"
    app_version: str = "0.1.0"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
