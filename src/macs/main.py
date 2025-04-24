import os

from langchain_ollama.chat_models import ChatOllama
from langchain_ollama import OllamaEmbeddings

from macs.tools.serper_search_tool import get_serper_search_tool
from macs.tools.scrape_website_tool import get_scrape_website_tool
from macs.tools.website_qa_tool import get_website_qa_tool
from macs.agents.vulnerability_research_agent import get_vulnerability_research_agent
from macs.agents.impact_analyzer_agent import get_impact_analyzer_agent
from macs.agents.recommendation_expert_agent import get_recommendation_expert_agent
from typing_extensions import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, START, END


os.environ["SERPER_API_KEY"] = "c503b47583ccd2816fe20daf79737eff2461b40e"


manager_llm = ChatOllama(
    model="llama3.1",
    base_url="http://localhost:11434",
    temperature=0.1,
)
embeddings_model = OllamaEmbeddings(model="nomic-embed-text")

serper_search_tool = get_serper_search_tool()
scrape_website_tool = get_scrape_website_tool()
website_qa_tool = get_website_qa_tool(
    llm=manager_llm,
    embeddings_model=embeddings_model,
)

vulnerability_research_agent = get_vulnerability_research_agent(
    llm=manager_llm,
    tools=[serper_search_tool, scrape_website_tool],
)

impact_analyzer_agent = get_impact_analyzer_agent(
    llm=manager_llm,
    tools=[serper_search_tool, scrape_website_tool],
)

recommendation_expert_agent = get_recommendation_expert_agent(
    llm=manager_llm,
    tools=[serper_search_tool, scrape_website_tool],
)


class GraphState(TypedDict):
    query: str
    vulns: str
    impact: str
    recommendations: str
    history: Annotated[list[str], add]


def vulnerability_research_node(state: GraphState) -> dict:
    out = vulnerability_research_agent.invoke({"input": state["query"]})
    return {
        "vulns": out["output"],
        "history": [f"🔍 research → {out['output'][:120]}…"],
    }


def impact_analyzer_node(state: GraphState) -> dict:
    out = impact_analyzer_agent.invoke({"input": state["vulns"]})
    return {"impact": out["output"], "history": [f"⚖️  impact → {out['output'][:120]}…"]}


def recommendation_node(state: GraphState) -> dict:
    out = recommendation_expert_agent.invoke({"input": state["impact"]})
    return {
        "recommendations": out["output"],
        "history": [f"💡 recommend → {out['output'][:120]}…"],
    }


query = {
    "query": "Research and identify new critical vulnerabilities with the following parameters:"
    "- Vendor: Cisco"
    "- Timeframe: 2025"
    "- Severity: critical"
    "Focus on:"
    "1. Technical details of each vulnerability"
    "2. Affected systems and versions"
    "3. Exploitation methods"
    "4. Current patch status"
    "Format the output as a structured list with clear headers for each vulnerability."
}

builder = StateGraph(GraphState)
builder.add_node("vulnerability_research", vulnerability_research_node)
builder.add_node("impact_analyzer", impact_analyzer_node)
builder.add_node("recommendation", recommendation_node)

builder.add_edge(START, "vulnerability_research")
builder.add_edge("vulnerability_research", "impact_analyzer")
builder.add_edge("impact_analyzer", "recommendation")
builder.add_edge("recommendation", END)

graph = builder.compile()

result = graph.invoke(query)
print(result["recommendations"])
print("\n--- History step by step ---")
for line in result["history"]:
    print(line)
