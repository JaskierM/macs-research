from importlib.resources import files

from macs.agents.base import BaseAgent
from macs.core.registry import register_agent

PROMPT_FILE = files("macs.prompts").joinpath("recommendation_expert.md")


@register_agent("recommendation_expert")
class RecommendationExpertAgent(BaseAgent):
    def system_prompt(self) -> str:
        return PROMPT_FILE.read_text(encoding="utf-8")
