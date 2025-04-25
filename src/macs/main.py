from typing import TypedDict, Optional
from langchain_ollama.chat_models import ChatOllama
from langchain_ollama import OllamaEmbeddings
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

from macs.tools.serper_search_tool import get_serper_search_tool
from macs.tools.travily_search_tool import get_travily_search_tool
from macs.tools.scrape_website_tool import get_scrape_website_tool
from macs.tools.website_qa_tool import get_website_qa_tool
from macs.agents.vulnerability_research_agent import get_vulnerability_research_agent
from macs.agents.impact_analyzer_agent import get_impact_analyzer_agent
from macs.agents.recommendation_expert_agent import get_recommendation_expert_agent

load_dotenv()


manager_llm = ChatOllama(
    model="gemma3:4b",
    base_url="http://localhost:11434",
    temperature=0.1,
)
embeddings_model = OllamaEmbeddings(model="nomic-embed-text")

serper_search_tool = get_serper_search_tool()
tavily_search_tool = get_travily_search_tool()
scrape_website_tool = get_scrape_website_tool()
website_qa_tool = get_website_qa_tool(
    llm=manager_llm, embeddings_model=embeddings_model
)

vulnerability_research_agent = get_vulnerability_research_agent(
    llm=manager_llm,
    tools=[
        serper_search_tool,
        tavily_search_tool,
        # scrape_website_tool,
        website_qa_tool,
    ],
)

impact_analyzer_agent = get_impact_analyzer_agent(
    llm=manager_llm,
    tools=[
        serper_search_tool,
        tavily_search_tool,
        website_qa_tool,
    ],
)

recommendation_expert_agent = get_recommendation_expert_agent(
    llm=manager_llm,
    tools=[
        serper_search_tool,
        tavily_search_tool,
        website_qa_tool,
    ],
)


class VulnSystemState(TypedDict):
    input: str
    query: Optional[str]
    vulnerabilities_report: Optional[str]
    impact_analysis: Optional[str]
    recommendation: Optional[str]


def vulnerability_research_agent_node(state: dict) -> dict:
    input_text = state["input"]
    result = vulnerability_research_agent.invoke({"input": input_text})
    return {**state, "vulnerabilities_report": result["output"]}


def impact_analyzer_agent_node(state: dict) -> dict:
    vulnerabilities_report = state.get("vulnerabilities_report", "")
    result = impact_analyzer_agent.invoke({"input": vulnerabilities_report})
    return {**state, "impact_analysis": result["output"]}


def recommendation_expert_agent_node(state: dict) -> dict:
    vulnerabilities_report = state.get("vulnerabilities_report", "")
    impact_analysis = state.get("impact_analysis", "")

    combined_input = (
        f"Based on the vulnerabilities report:\n{vulnerabilities_report}\n\n"
        f"And the impact analysis:\n{impact_analysis}\n\n"
        "Generate detailed risk mitigation recommendations."
    )

    result = recommendation_expert_agent.invoke({"input": combined_input})
    return {**state, "recommendation": result["output"]}


graph_builder = StateGraph(VulnSystemState)

graph_builder.add_node(
    "vulnerability_research_agent_node", vulnerability_research_agent_node
)
graph_builder.add_node("impact_analyzer_agent_node", impact_analyzer_agent_node)
graph_builder.add_node(
    "recommendation_expert_agent_node", recommendation_expert_agent_node
)

graph_builder.add_edge(START, "vulnerability_research_agent_node")
graph_builder.add_edge(
    "vulnerability_research_agent_node", "impact_analyzer_agent_node"
)
graph_builder.add_edge("impact_analyzer_agent_node", "recommendation_expert_agent_node")
graph_builder.add_edge("recommendation_expert_agent_node", END)

graph = graph_builder.compile()
graph

input_msg = {
    "input": "Research and identify new critical vulnerabilities with the following parameters:"
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

result = graph.invoke(input_msg, config={"verbose": True})

print(result["vulnerabilities_report"])
