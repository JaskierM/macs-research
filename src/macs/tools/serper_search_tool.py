from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

# from macs.tools.args_wrappers import structured_tool_wrapper


class SerperSearchInput(BaseModel):
    query: str = Field(..., description="Search query")


def _serper_search(**kwargs) -> str:
    try:
        serper = GoogleSerperAPIWrapper()
        return serper.run(kwargs.get("query", ""))
    except Exception as e:
        return f"Error: {e}"


def get_serper_search_tool(
    name: str = "SerperSearchTool",
    description: str = "Uses Google via Serper.dev to find and summarize relevant information from Google for a query",
) -> StructuredTool:
    return StructuredTool.from_function(
        func=_serper_search,
        name=name,
        description=description,
        args_schema=SerperSearchInput,
    )
