from abc import ABC, abstractmethod
from typing import Sequence


class BaseLLM(ABC):

    @abstractmethod
    async def chat(self, messages: Sequence[str], **kwargs) -> str: ...

    @abstractmethod
    async def embed(self, texts: Sequence[str]) -> list[list[float]]: ...
