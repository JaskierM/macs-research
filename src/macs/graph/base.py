from abc import ABC, abstractmethod
from langgraph.graph.graph import CompiledGraph

from macs.config.graph import BaseGraphConfig


class BaseGraph(ABC):

    def __init__(self, cfg: BaseGraphConfig) -> None:
        self._cfg = cfg

    @abstractmethod
    def build(self) -> CompiledGraph: ...
