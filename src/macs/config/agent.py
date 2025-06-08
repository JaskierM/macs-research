from typing import Optional, Sequence, Any
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool
from langgraph.checkpoint.base import BaseCheckpointSaver


class AgentConfig(BaseModel):
    provider_key: str = Field(...)
    tools: Sequence[BaseTool] = Field(default_factory=list)
    prompt_name: str = Field(...)
    checkpointer: Optional[BaseCheckpointSaver] = Field(None)
    debug: Optional[bool] = Field(False)
    extras: dict[str, Any] = Field(default_factory=dict)

    model_config = {"arbitrary_types_allowed": True}
