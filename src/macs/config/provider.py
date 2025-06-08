from typing import Literal, Optional
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

_PROJECT_ROOT = Path(__file__).resolve().parents[3]
_ENV_PATH = _PROJECT_ROOT / ".env"


class BaseProviderConfig(BaseSettings):
    provider_key: Literal["ollama"] = Field(..., alias="PROVIDER")
    llm_key: str = Field(..., alias="LLM")
    embed_model_key: Optional[str] = Field(None, alias="EMBED_MODEL")
    temperature: Optional[float] = Field(0.2, alias="LLM_TEMPERATURE")

    model_config = SettingsConfigDict(env_file=str(_ENV_PATH), extra="ignore")


class OllamaConfig(BaseProviderConfig):
    base_url: Optional[str] = Field("http://localhost:11434", alias="OLLAMA_BASE_URL")
