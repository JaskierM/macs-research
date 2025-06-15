from langgraph.prebuilt import create_react_agent
from langgraph.graph.graph import CompiledGraph
from langgraph.checkpoint.memory import MemorySaver

from macs.agents.base import BaseAgent
from macs.config.agent import ImpactAnalyzerConfig
from macs.agents.registry import AGENT_REGISTRY


class ImpactAnalyzerAgent(BaseAgent):

    def __init__(self, cfg: ImpactAnalyzerConfig) -> None:
        super().__init__(cfg)

    def build(self) -> CompiledGraph:
        return create_react_agent(
            model=self._load_llm(),
            tools=self._load_tools(),
            prompt=self._load_prompt(),
            checkpointer=MemorySaver(),
            debug=self._cfg.debug,
            **self._cfg.extras,
        )


@AGENT_REGISTRY.register("impact_analyzer")
def build_impact_analyzer() -> CompiledGraph:
    return ImpactAnalyzerAgent(ImpactAnalyzerConfig()).build()
