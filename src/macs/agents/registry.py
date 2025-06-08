from typing import Callable
from langgraph.graph.graph import CompiledGraph

from macs.core.registry import Registry
from macs.config.agent import AgentConfig

AGENT_REGISTRY = Registry[Callable[[AgentConfig | None], CompiledGraph]]()
