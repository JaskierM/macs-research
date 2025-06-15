from langgraph.prebuilt import create_react_agent
from langgraph.graph.graph import CompiledGraph
from langgraph.checkpoint.memory import MemorySaver

from macs.agents.base import BaseAgent
from macs.config.agent import RecommendationExpertConfig
from macs.agents.registry import AGENT_REGISTRY


class RecommendationExpertAgent(BaseAgent):

    def __init__(self, cfg: RecommendationExpertConfig) -> None:
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


@AGENT_REGISTRY.register("recommendation_expert")
def build_recommendation_expert() -> CompiledGraph:
    return RecommendationExpertAgent(RecommendationExpertConfig()).build()
