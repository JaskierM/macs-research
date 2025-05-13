from langchain_core.messages import AnyMessage
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt.chat_agent_executor import AgentState


SYSTEM_PROMPT = (
    "You are a security advisor with extensive experience in\n"
    "vulnerability remediation. You provide practical, actionable recommendations\n"
    "for addressing security vulnerabilities, including specific steps, patches,\n"
    "and best practices.\n"
    "Your main goal: provide detailed mitigation strategies and recommendations.\n"
)


def prompt(state: AgentState, config: RunnableConfig) -> list[AnyMessage]:
    return [{"role": "system", "content": SYSTEM_PROMPT}] + state["messages"]


def get_recommendation_expert_agent(model, tools):
    agent = create_react_agent(model=model, tools=tools, prompt=prompt, debug=True)
    return agent
