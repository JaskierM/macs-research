from typing import Type
from langchain.tools import StructuredTool
from langchain_community.tools.tavily_search import TavilySearchResults

from macs.config.tool import TavilySearchConfig, TavilySearchInput
from macs.tools.registry import TOOL_REGISTRY


class TavilySearchTool(StructuredTool):
    name: str = "tavily_search"
    description: str = (
        "Web-search via Tavily. Returns a list of urls & snippets for a query."
    )
    args_schema: Type[TavilySearchInput] = TavilySearchInput

    def __init__(self, settings: TavilySearchConfig | None = None) -> None:
        super().__init__()
        self._search = TavilySearchResults(**settings.model_dump())

    def _run(self, query: str) -> str:
        try:
            res = self._search.run(query)
            return "\n".join(str(r) for r in res)
        except Exception as exc:
            return f"[Tavily error] {exc}."

    async def _arun(self, query: str) -> str:
        try:
            res = await self._search.arun(query)
            return "\n".join(str(r) for r in res)
        except Exception as exc:
            return f"[Tavily error] {exc}."


@TOOL_REGISTRY.register("tavily_search")
def build_tavily_search() -> StructuredTool:
    return TavilySearchTool(TavilySearchConfig())
