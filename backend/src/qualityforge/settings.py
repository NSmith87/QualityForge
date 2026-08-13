from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

LLMProvider = Literal["ollama", "openai", "anthropic", "azure_openai"]
VectorBackend = Literal["chroma", "qdrant", "pinecone", "weaviate"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "local"
    llm_provider: LLMProvider = "ollama"
    llm_model: str = "mistral"
    ollama_base_url: str = "http://127.0.0.1:11434"
    openai_api_key: str | None = None
    openai_model: str = "gpt-4.1"
    anthropic_api_key: str | None = None
    anthropic_model: str = "claude-sonnet-4-5"
    azure_openai_api_key: str | None = None
    azure_openai_endpoint: str | None = None
    azure_openai_deployment: str | None = None
    azure_openai_api_version: str = "2024-10-21"
    database_url: str = (
        "postgresql+psycopg://qualityforge:qualityforge@127.0.0.1:5432/qualityforge"
    )
    vector_backend: VectorBackend = "chroma"
    chroma_path: str = ".chroma"
    chroma_collection: str = "qualityforge"


@lru_cache
def get_settings() -> Settings:
    return Settings()
