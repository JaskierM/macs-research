from typing import TypedDict, Optional


class VulnSystemState(TypedDict):
    input: str
    query: Optional[str]
    vulnerabilities_report: Optional[str]
    impact_analysis: Optional[str]
    recommendation: Optional[str]
