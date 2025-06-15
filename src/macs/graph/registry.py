from typing import Callable
from langgraph.graph.graph import CompiledGraph

from macs.core.registry import Registry
from macs.config.graph import BaseGraphConfig

GRAPH_REGISTRY = Registry[Callable[[BaseGraphConfig | None], CompiledGraph]]()


def get_graph(name: str) -> CompiledGraph:
    return GRAPH_REGISTRY.get(name)()
