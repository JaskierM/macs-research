from importlib.resources import files

from macs.agents.base import BaseAgent
from macs.core.registry import register_agent

PROMPT_FILE = files("macs.prompts").joinpath("impact_analyzer.md")


@register_agent("impact_analyzer")
class ImpactAnalyzerAgent(BaseAgent):
    def system_prompt(self) -> str:
        return PROMPT_FILE.read_text(encoding="utf-8")
