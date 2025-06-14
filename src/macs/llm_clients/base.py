from abc import ABC, abstractmethod
from typing import Sequence
from langchain_core.language_models.chat_models import BaseChatModel


class BaseLLMClient(ABC):

    @abstractmethod
    async def chat(self, messages: Sequence[str], **kwargs) -> str: ...

    @abstractmethod
    def llm(self) -> BaseChatModel: ...
