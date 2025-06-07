from typing import Sequence, List
from langchain_ollama.chat_models import ChatOllama
from langchain_ollama.embeddings import OllamaEmbeddings

from macs.llm.base import BaseLLM
from macs.config.llm import OllamaSettings
from macs.llm.registry import LLM_REGISTRY


class OllamaLLM(BaseLLM):

    def __init__(self, settings: OllamaSettings) -> None:
        self._chat = ChatOllama(
            model=settings.model,
            base_url=settings.base_url,
            temperature=settings.temperature,
        )
        self._embed = OllamaEmbeddings(model=settings.embed_model)

    async def chat(self, messages: Sequence[str], **kwargs) -> str:
        resp = await self._chat.ainvoke(list(messages), **kwargs)
        return resp.content

    async def embed(self, texts: Sequence[str]) -> List[List[float]]:
        return await self._embed.aembed_documents(list(texts))


@LLM_REGISTRY.register("ollama")
def build_ollama_llm() -> BaseLLM:
    return OllamaLLM(OllamaSettings())
