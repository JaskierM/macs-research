from typing import Callable
from macs.llm_clients.base import BaseLLMClient
from macs.core.registry import Registry

LLM_CLIENT_REGISTRY = Registry[Callable[[], BaseLLMClient]]()


def get_llm_client(name: str) -> BaseLLMClient:
    return LLM_CLIENT_REGISTRY.get(name)()
