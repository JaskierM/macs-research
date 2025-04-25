from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

from macs.tools.args_wrappers import structured_tool_wrapper


MAX_RESULTS = 10


class SerperSearchInput(BaseModel):
    query: str = Field(..., description="Search query")


def _travily_search(**kwargs) -> str:
    try:
        travily_search = TavilySearchResults(max_results=MAX_RESULTS)
        result = travily_search.run(kwargs.get("query", ""))
        return "\n".join([str(elem) for elem in result])
    except Exception as e:
        return f"Error: {e}"


def get_travily_search_tool(
    name: str = "TravilySearchTool",
    description: str = (
        "A search engine. Useful for when you need to answer questions about current events\n"
        f"and get some URLs that you can then explore. Return {MAX_RESULTS} urls and related information\n"
        "Input should be a one search query"
    ),
) -> StructuredTool:
    return StructuredTool.from_function(
        func=structured_tool_wrapper(_travily_search),
        name=name,
        description=description,
        args_schema=SerperSearchInput,
    )
