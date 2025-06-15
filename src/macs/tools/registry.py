from typing import Callable
from langchain.tools import Tool
from macs.core.registry import Registry

TOOL_REGISTRY = Registry[Callable[[], Tool]]()


def get_tool(name: str) -> Tool:
    return TOOL_REGISTRY.get(name)()
