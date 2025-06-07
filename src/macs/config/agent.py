from typing import Any, Sequence, Optional
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool
from langgraph.checkpoint.base import BaseCheckpointSaver
from langchain_core.language_models.chat_models import BaseChatModel


class AgentConfig(BaseModel):
    model: BaseChatModel
    tools: Sequence[BaseTool]
    checkpointer: Optional[BaseCheckpointSaver] = None
    debug: bool = False
    extras: dict[str, Any] = Field(default_factory=dict)

    class Config:
        arbitrary_types_allowed = True
