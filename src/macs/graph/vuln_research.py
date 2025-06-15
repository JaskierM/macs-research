from typing import List, Dict
from langchain_core.messages import BaseMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.graph import CompiledGraph
from langgraph.checkpoint.memory import MemorySaver

from macs.graph.registry import GRAPH_REGISTRY
from macs.graph.base import BaseGraph
from macs.agents.registry import get_agent
from macs.config.graph import VulnResearchConfig, VulnResearchState


class VulnResearchGraph(BaseGraph):

    def __init__(self, cfg: VulnResearchConfig) -> None:
        super().__init__(cfg)
        self._vuln_researcher = get_agent("vuln_researcher")
        self._impact_analyzer = get_agent("impact_analyzer")
        self._recommendation_expert = get_agent("recommendation_expert")

    async def vuln_researcher_node(
        self, state: VulnResearchState
    ) -> Dict[str, List[BaseMessage]]:
        state["query"] = state["messages"][0].content
        print(f"vuln_researcher: я установил query: {state["query"]}")

        response = await self._vuln_researcher.ainvoke(
            {"messages": state["messages"]},
            config={"configurable": {"thread_id": state["session_id"]}},
        )

        print(
            f"vuln_researcher: я установил vulnerabilities_report: {response["messages"][-1].content}"
        )
        return {
            "messages": state["messages"] + response["messages"],
            "vulnerabilities_report": response["messages"][-1].content,
            "query": state["messages"][0].content,
        }

    async def impact_analyzer_node(
        self, state: VulnResearchState
    ) -> Dict[str, List[BaseMessage]]:
        print("impact_analyzer: приступаю к работе")
        response = await self._impact_analyzer.ainvoke(
            {"messages": [state["vulnerabilities_report"]]},
            config={"configurable": {"thread_id": state["session_id"]}},
        )

        state["impact_analysis"] = response["messages"][-1].content
        print(
            f"impact_analyzer: я установил анализ влияний: {state["impact_analysis"]}"
        )
        return {
            "messages": state["messages"] + response["messages"],
            "impact_analysis": response["messages"][-1].content,
        }

    async def recommendation_expert_node(
        self, state: VulnResearchState
    ) -> Dict[str, List[BaseMessage]]:
        print("recommendation_expert: приступаю к работе")

        response = await self._recommendation_expert.ainvoke(
            {
                "messages": [
                    state["vulnerabilities_report"],
                    state["impact_analysis"],
                ]
            },
            config={"configurable": {"thread_id": state["session_id"]}},
        )

        print(
            f"recommendation_expert: я установил рекомендации: {response["messages"][-1].content}"
        )

        return {
            "messages": state["messages"] + response["messages"],
            "recommendation": response["messages"][-1].content,
        }

    def build(self) -> CompiledGraph:
        graph = StateGraph(VulnResearchState)

        graph.add_node("vuln_researcher", self.vuln_researcher_node)
        graph.add_node("impact_analyzer", self.impact_analyzer_node)
        graph.add_node("recommendation_expert", self.recommendation_expert_node)

        graph.add_edge(START, "vuln_researcher")
        graph.add_edge("vuln_researcher", "impact_analyzer")
        graph.add_edge("impact_analyzer", "recommendation_expert")
        graph.add_edge("recommendation_expert", END)

        return graph.compile(
            checkpointer=MemorySaver(),
            debug=self._cfg.debug,
        )


@GRAPH_REGISTRY.register("vuln_research")
def build_vuln_research() -> CompiledGraph:
    return VulnResearchGraph(VulnResearchConfig()).build()
