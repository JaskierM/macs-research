from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings
from langgraph.graph import MessagesState


class BaseGraphConfig(BaseSettings):
    debug: Optional[bool] = Field(False)


class VulnResearchConfig(BaseGraphConfig): ...


class VulnResearchState(MessagesState):
    session_id: str
    query: Optional[str]
    vulnerabilities_report: Optional[str]
    impact_analysis: Optional[str]
    recommendation: Optional[str]
