from typing import Sequence, List
from langchain_ollama.chat_models import ChatOllama
from langchain_ollama.embeddings import OllamaEmbeddings

from macs.llm_clients.base import BaseLLMClient
from macs.config.provider import OllamaConfig
from macs.llm_clients.registry import LLM_CLIENT_REGISTRY


class OllamaLLMClient(BaseLLMClient):

    def __init__(self, cfg: OllamaConfig) -> None:
        self._llm = ChatOllama(
            model=cfg.llm_key,
            base_url=cfg.base_url,
            temperature=cfg.temperature,
        )
        self._embed_model = (
            OllamaEmbeddings(model=cfg.embed_model_key, base_url=cfg.base_url)
            if cfg.embed_model_key
            else None
        )

    @property
    def llm(self) -> ChatOllama:
        return self._llm

    @property
    def embed_model(self) -> OllamaEmbeddings:
        return self._embed_model

    async def chat(self, messages: Sequence[str], **kwargs) -> str:
        resp = await self._llm.ainvoke(list(messages), **kwargs)
        return resp.content

    async def embed(self, texts: Sequence[str]) -> List[List[float]]:
        return await self._embed_model.aembed_documents(list(texts))


@LLM_CLIENT_REGISTRY.register("ollama")
def build_ollama_llm_client() -> OllamaLLMClient:
    return OllamaLLMClient(OllamaConfig())
