from typing import Optional
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

_PROJECT_ROOT = Path(__file__).resolve().parents[3]
_ENV_PATH = _PROJECT_ROOT / ".env"


class BaseLLMClientConfig(BaseSettings):
    model: str = Field(...)
    embed_model: Optional[str | None] = Field(None)
    temperature: Optional[float] = Field(0.2)

    model_config = SettingsConfigDict(
        env_prefix="LLM_CLIENT_", env_file=str(_ENV_PATH), extra="ignore"
    )


class OllamaConfig(BaseLLMClientConfig):
    base_url: Optional[str] = Field("http://localhost:11434")

    model_config = SettingsConfigDict(
        env_prefix="OLLAMA_", env_file=str(_ENV_PATH), extra="ignore"
    )
