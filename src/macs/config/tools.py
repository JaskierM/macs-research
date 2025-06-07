from typing import Optional
from pathlib import Path
from pydantic import BaseModel, Field, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

_PROJECT_ROOT = Path(__file__).resolve().parents[3]
_ENV_PATH = _PROJECT_ROOT / ".env"


class TavilySearchSettings(BaseSettings):
    max_results: Optional[int] = Field(10, alias="TAVILY_SEARCH_MAX_RESULTS")

    model_config = SettingsConfigDict(env_file=str(_ENV_PATH), extra="ignore")


class TavilySearchInput(BaseModel):
    query: str = Field(..., description="Search query string (natural language).")


class SerperSearchInput(BaseModel):
    query: str = Field(..., description="Search query string (natural language).")


class ScrapeWebsiteInput(BaseModel):
    url: str = Field(..., description="Web-page URL to scrape.")


class WebsiteQASettings(BaseSettings):
    max_chunk_size: int = Field(500, alias="WEBSITE_QA_MAX_CHUNK_SIZE")
    chunk_overlap: int = Field(50, alias="WEBSITE_QA_MAX_CHUNK_OVERLAP")

    model_config = SettingsConfigDict(env_file=str(_ENV_PATH), extra="ignore")


class WebsiteQAInput(BaseModel):
    url: str = Field(..., description="Web‑page URL.")
    question: str = Field(
        ..., description="Any question about the content of the page."
    )
