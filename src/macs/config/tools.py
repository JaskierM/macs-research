from typing import Optional
from pathlib import Path
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

_PROJECT_ROOT = Path(__file__).resolve().parents[3]
_ENV_PATH = _PROJECT_ROOT / ".env"


class TavilySearchConfig(BaseSettings):
    max_results: Optional[int] = Field(10, alias="TAVILY_SEARCH_MAX_RESULTS")

    model_config = SettingsConfigDict(env_file=str(_ENV_PATH), extra="ignore")


class TavilySearchInput(BaseModel):
    query: str = Field(..., description="Search query string (natural language).")


class SerperSearchInput(BaseModel):
    query: str = Field(..., description="Search query string (natural language).")


class ScrapeWebsiteInput(BaseModel):
    url: str = Field(..., description="Web-page URL to scrape.")


class WebsiteQAConfig(BaseSettings):
    provider_key: str = Field(..., alias="WEBSITE_QA_PROVIDER")
    max_chunk_size: Optional[int] = Field(500, alias="WEBSITE_QA_MAX_CHUNK_SIZE")
    chunk_overlap: Optional[int] = Field(50, alias="WEBSITE_QA_MAX_CHUNK_OVERLAP")

    model_config = SettingsConfigDict(env_file=str(_ENV_PATH), extra="ignore")


class WebsiteQAInput(BaseModel):
    url: str = Field(..., description="Web‑page URL.")
    question: str = Field(
        ..., description="Any question about the content of the page."
    )
