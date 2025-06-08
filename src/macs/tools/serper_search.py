from typing import Type
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.tools import StructuredTool

from macs.config.tools import SerperSearchInput
from macs.tools.registry import TOOL_REGISTRY


class SerperSearchTool(StructuredTool):
    name: str = "serper_search"
    description: str = (
        "Uses Google via Serper.dev to find and summarize relevant information ",
        "from Google for a query.",
    )
    args_schema: Type[SerperSearchInput] = SerperSearchInput

    def __init__(self) -> None:
        super().__init__()
        self._serper = GoogleSerperAPIWrapper()

    def _run(self, query: str) -> str:
        try:
            res = self._serper.run(query)
            return res
        except Exception as exc:
            return f"[Tavily error] {exc}."

    async def _arun(self, query: str) -> str:
        try:
            res = await self._serper.arun(query)
            return res
        except Exception as exc:
            return f"[Tavily error] {exc}."


@TOOL_REGISTRY.register("serper_search")
def build_serper_search() -> StructuredTool:
    return SerperSearchTool()
