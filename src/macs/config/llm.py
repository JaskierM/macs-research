from typing import Literal, Optional
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[3]
ENV_PATH = PROJECT_ROOT / ".env"


class BaseLLMSettings(BaseSettings):
    provider: Literal["ollama"] = Field(..., alias="LLM_PROVIDER")
    model: str = Field(..., alias="LLM_MODEL")
    embed_model: str = Field(..., alias="EMBED_MODEL")
    temperature: Optional[float] = Field(0.2, alias="LLM_TEMPERATURE")
    max_tokens: Optional[int] = Field(None, ealiasnv="LLM_MAX_TOKENS")

    model_config = SettingsConfigDict(env_file=str(ENV_PATH), extra="ignore")


class OllamaSettings(BaseLLMSettings):
    base_url: Optional[str] = Field("http://localhost:11434", alias="OLLAMA_BASE_URL")
