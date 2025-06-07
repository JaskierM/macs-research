from typing import Callable
from macs.llm.base import BaseLLM
from macs.core.registry import Registry

LLM_REGISTRY = Registry[Callable[[], BaseLLM]]()
