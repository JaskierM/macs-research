from typing import Callable
from langchain.tools import StructuredTool
from macs.core.registry import Registry

TOOL_REGISTRY = Registry[Callable[[], StructuredTool]]()
