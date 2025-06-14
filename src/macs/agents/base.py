from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Sequence
from jinja2 import Environment, FileSystemLoader
from langchain.chat_models.base import BaseChatModel
from langgraph.graph.graph import CompiledGraph
from langchain_core.tools import BaseTool

from macs.config.agent import AgentConfig
from macs.llm_clients.registry import LLM_CLIENT_REGISTRY
from macs.tools.registry import TOOL_REGISTRY


_PROMPTS_DIR = Path(__file__).resolve().parents[1] / "prompts"


class BaseAgent(ABC):

    def __init__(self, cfg: AgentConfig) -> None:
        self._cfg = cfg

    @abstractmethod
    def build(self) -> CompiledGraph: ...

    def _load_llm(self) -> BaseChatModel:
        return LLM_CLIENT_REGISTRY.get(self._cfg.provider_key)().get_llm()

    def _load_tools(self) -> Sequence[BaseTool]:
        return [TOOL_REGISTRY.get(key)() for key in self._cfg.tool_keys or []]

    def _load_prompt(self) -> str:
        path = _PROMPTS_DIR / f"{self._cfg.prompt_name}.j2"
        return (
            Environment(loader=FileSystemLoader(_PROMPTS_DIR))
            .get_template(path.name)
            .render()
        )
