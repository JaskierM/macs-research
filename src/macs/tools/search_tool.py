from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field


class GoogleSearchInput(BaseModel):
    query: str = Field(..., description="Search query for Google")


def search_google(query: str) -> str:
    try:
        serper = GoogleSerperAPIWrapper()
        return serper.run(query)
    except Exception as e:
        return f"Error: {e}"


def get_search_tool() -> StructuredTool:
    return StructuredTool.from_function(
        func=search_google,
        name="SearchTool",
        description="Uses Google via Serper.dev to search the web for relevant information",
        args_schema=GoogleSearchInput,
    )
