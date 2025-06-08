from langgraph.prebuilt import create_react_agent
from langgraph.graph.graph import CompiledGraph

from macs.agents.base import BaseAgent, AGENT_REGISTRY
from macs.config.agent import AgentConfig


class VulnResearcherAgent(BaseAgent):
    DEFAULT_LLM = "ollama"
    DEFAULT_PROMPT_NAME = "vuln_researcher"

    def __init__(self, cfg: AgentConfig):
        super().__init__(cfg)

    def build(self) -> CompiledGraph:
        return create_react_agent(
            llm=self._load_llm(),
            tools=self._cfg.tools,
            prompt=self._load_prompt(),
            checkpointer=self._cfg.checkpointer,
            debug=self._cfg.debug,
            **self._cfg.extras,
        )


@AGENT_REGISTRY.register("vuln_researcher")
def build_vuln_researcher(cfg: AgentConfig) -> CompiledGraph:
    return VulnResearcherAgent(cfg).build()
