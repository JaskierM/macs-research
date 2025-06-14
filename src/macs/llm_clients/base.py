from abc import ABC, abstractmethod
from typing import Sequence
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.embeddings import Embeddings


class BaseLLMClient(ABC):

    @abstractmethod
    async def chat(self, messages: Sequence[str], **kwargs) -> str: ...

    @abstractmethod
    async def embed(self, texts: Sequence[str]) -> list[list[float]] | None:
        return None

    @abstractmethod
    def llm(self) -> BaseChatModel: ...

    @abstractmethod
    def embed_model(self) -> Embeddings | None:
        return None
