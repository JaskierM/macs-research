from __future__ import annotations

from abc import ABC, abstractmethod

from pathlib import Path
from typing import Callable
from jinja2 import Environment, FileSystemLoader
from langchain.tools import BaseTool
from langchain.chat_models.base import BaseChatModel
from langgraph.graph.graph import CompiledGraph

from macs.core.registry import Registry
from macs.tools.registry import TOOL_REGISTRY
from macs.provider.registry import PROVIDER_REGISTRY
from macs.config.agent import AgentConfig


AGENT_REGISTRY: Registry[Callable[[], CompiledGraph]] = Registry()
_PROMPTS_DIR = Path(__file__).resolve().parents[1] / "prompts"


class BaseAgent(ABC):

    def __init__(self, cfg: AgentConfig) -> None:
        self._cfg = cfg

    @abstractmethod
    def build(self) -> CompiledGraph: ...

    def _load_llm(self) -> BaseChatModel:
        return PROVIDER_REGISTRY.get(self._cfg.provider_key)()

    def _load_prompt(self) -> str:
        path = _PROMPTS_DIR / f"{self._cfg.prompt_name}.j2"
        return (
            Environment(loader=FileSystemLoader(_PROMPTS_DIR))
            .get_template(path.name)
            .render()
        )
