from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field


class SerperSearchInput(BaseModel):
    query: str = Field(..., description="Search query for Google")


def _serper_search(query: str) -> str:
    try:
        serper = GoogleSerperAPIWrapper()
        return serper.run(query)
    except Exception as e:
        return f"Error: {e}"


def get_serper_search_tool(
    name: str = "SerperSearchTool",
    description: str = "Uses Google via Serper.dev to search the web for relevant information",
) -> StructuredTool:
    return StructuredTool.from_function(
        func=_serper_search,
        name=name,
        description=description,
        args_schema=SerperSearchInput,
    )
