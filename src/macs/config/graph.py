from typing import TypedDict, Optional


class VulnResearchSystemState(TypedDict, total=False):
    input: str
    query: Optional[str]
    vulnerabilities_report: Optional[str]
    impact_analysis: Optional[str]
    recommendation: Optional[str]
