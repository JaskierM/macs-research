from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Iterable, Iterator

from langchain_core.messages import AnyMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import Graph
from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt.chat_agent_executor import AgentState

from macs.config.agents.agent import AgentConfig


class BaseAgent(ABC):

    def __init__(self, cfg: "AgentConfig"):
        self.cfg = cfg
        self._graph = self.build_graph()

    @abstractmethod
    def system_prompt(self) -> str: ...

    def extra_prompt(self, state: AgentState) -> list[AnyMessage]:
        return []

    def prompt(self, state: AgentState, config: RunnableConfig) -> list[AnyMessage]:
        return (
            [{"role": "system", "content": self.system_prompt()}]
            + self.extra_prompt(state)
            + list(state["messages"])
        )

    def build_graph(self) -> Graph:
        return create_react_agent(
            model=self.cfg.model,
            tools=self.cfg.tools,
            prompt=self.prompt,
            debug=self.cfg.debug,
            checkpointer=self.cfg.checkpointer,
        )

    def invoke(self, state: AgentState, *, config: RunnableConfig | None = None) -> Any:
        return self._graph.invoke(state, config=config or {})

    def stream(
        self,
        state: AgentState,
        *,
        config: RunnableConfig | None = None,
        stream_mode: str | Iterable[str] = "values",
    ) -> Iterator[Any]:
        return self._graph.stream(state, config=config or {}, stream_mode=stream_mode)
