from langgraph.prebuilt import create_react_agent
from langgraph.graph.graph import CompiledGraph

from macs.agents.base import BaseAgent
from macs.config.agent import VulnResearcherConfig
from macs.agents.registry import AGENT_REGISTRY


class VulnResearcherAgent(BaseAgent):

    def __init__(self, cfg: VulnResearcherConfig) -> None:
        super().__init__(cfg)
        print(self._load_tools())

    def build(self) -> CompiledGraph:
        return create_react_agent(
            model=self._load_llm(),
            tools=self._load_tools(),
            prompt=self._load_prompt(),
            checkpointer=self._cfg.checkpointer,
            debug=self._cfg.debug,
            **self._cfg.extras,
        )


@AGENT_REGISTRY.register("vuln_researcher")
def build_vuln_researcher() -> CompiledGraph:
    return VulnResearcherAgent(VulnResearcherConfig()).build()
