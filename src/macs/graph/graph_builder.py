from macs.graph.vuln_system_state import VulnSystemState
from langgraph.graph import StateGraph, START, END


class GraphBuilder:

    def __init__(
        self,
        vulnerability_research_agent,
        impact_analyzer_agent,
        recommendation_expert_agent,
    ):
        self.vulnerability_research_agent = vulnerability_research_agent
        self.impact_analyzer_agent = impact_analyzer_agent
        self.recommendation_expert_agent = recommendation_expert_agent

    def vulnerability_research_agent_node(self, state: dict) -> dict:
        input_text = state["input"]
        result = self.vulnerability_research_agent.invoke(
            {"messages": [{"role": "user", "content": input_text}]}
        )
        return {**state, "vulnerabilities_report": result["messages"][-1].content}

    def impact_analyzer_agent_node(self, state: dict) -> dict:
        vulnerabilities_report = state["vulnerabilities_report"]
        result = self.impact_analyzer_agent.invoke(
            {"messages": [{"role": "user", "content": vulnerabilities_report}]}
        )
        return {**state, "impact_analysis": result["messages"][-1].content}

    def recommendation_expert_agent_node(self, state: dict) -> dict:
        vulnerabilities_report = state.get("vulnerabilities_report", "")
        impact_analysis = state.get("impact_analysis", "")

        combined_input = (
            f"Based on the vulnerabilities report:\n{vulnerabilities_report}\n\n"
            f"And the impact analysis:\n{impact_analysis}\n\n"
            "Generate detailed risk mitigation recommendations."
        )

        result = self.recommendation_expert_agent.invoke(
            {"messages": [{"role": "user", "content": combined_input}]}
        )
        return {**state, "recommendation": result["messages"][-1].content}

    def build(self):
        graph_builder = StateGraph(VulnSystemState)

        graph_builder.add_node(
            "vulnerability_research_agent_node", self.vulnerability_research_agent_node
        )
        graph_builder.add_node(
            "impact_analyzer_agent_node", self.impact_analyzer_agent_node
        )
        graph_builder.add_node(
            "recommendation_expert_agent_node", self.recommendation_expert_agent_node
        )

        graph_builder.add_edge(START, "vulnerability_research_agent_node")
        graph_builder.add_edge(
            "vulnerability_research_agent_node", "impact_analyzer_agent_node"
        )
        graph_builder.add_edge(
            "impact_analyzer_agent_node", "recommendation_expert_agent_node"
        )
        graph_builder.add_edge("recommendation_expert_agent_node", END)

        graph = graph_builder.compile()
        return graph
