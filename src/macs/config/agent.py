from typing import Optional, Sequence, Any
from pathlib import Path
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

_PROJECT_ROOT = Path(__file__).resolve().parents[3]
_ENV_PATH = _PROJECT_ROOT / ".env"


class BaseAgentConfig(BaseSettings):
    llm_client_key: str = Field(...)
    prompt_name: str = Field(...)
    tool_keys: Optional[Sequence[str]] = Field(default_factory=list)
    debug: Optional[bool] = Field(False)
    extras: dict[str, Any] = Field(default_factory=dict)

    @field_validator("tool_keys", mode="before")
    @classmethod
    def _split_tools(cls, value):
        if isinstance(value, str):
            return [s.strip() for s in value.split(",") if s.strip()]
        return value

    model_config = {"arbitrary_types_allowed": True}


class VulnResearcherConfig(BaseAgentConfig):
    model_config = SettingsConfigDict(
        env_prefix="VULN_RESEARCHER_",
        env_file=_ENV_PATH,
        extra="ignore",
        arbitrary_types_allowed=True,
    )


class ImpactAnalyzerConfig(BaseAgentConfig):
    model_config = SettingsConfigDict(
        env_prefix="IMPACT_ANALYZER_",
        env_file=_ENV_PATH,
        extra="ignore",
        arbitrary_types_allowed=True,
    )


class RecommendationExpertConfig(BaseAgentConfig):
    model_config = SettingsConfigDict(
        env_prefix="RECOMMENDATION_EXPERT_",
        env_file=_ENV_PATH,
        extra="ignore",
        arbitrary_types_allowed=True,
    )
