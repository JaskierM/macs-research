from typing import Optional, Sequence, Any
from pathlib import Path
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from langgraph.checkpoint.base import BaseCheckpointSaver

_PROJECT_ROOT = Path(__file__).resolve().parents[3]
_ENV_PATH = _PROJECT_ROOT / ".env"


class AgentConfig(BaseSettings):
    provider_key: str = Field(...)
    prompt_name: str = Field(...)
    tool_keys: Optional[Sequence[str]] = Field(default_factory=list)
    checkpointer: Optional[BaseCheckpointSaver | None] = Field(None)
    debug: Optional[bool] = Field(False)
    extras: dict[str, Any] = Field(default_factory=dict)

    model_config = {"arbitrary_types_allowed": True}


class VulnResearcherConfig(AgentConfig):
    model_config = SettingsConfigDict(
        env_prefix="VULN_RESEARCHER_",
        env_file=_ENV_PATH,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @field_validator("tool_keys", mode="before")
    @classmethod
    def _split_tools(cls, v):
        if isinstance(v, str):
            return [s.strip() for s in v.split(",") if s.strip()]
        return v
