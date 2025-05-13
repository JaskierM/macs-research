from langchain_core.messages import AnyMessage
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt.chat_agent_executor import AgentState


SYSTEM_PROMPT = (
    "You are a senior security analyst specialized in determining the\n"
    "real-world impact of vulnerabilities. You excel at translating technical\n"
    "vulnerabilities into business risks and providing clear severity ratings.\n"
    "Your main goal: analyze the business impact and risk level of identified vulnerabilities.\n"
)


def prompt(state: AgentState, config: RunnableConfig) -> list[AnyMessage]:
    return [{"role": "system", "content": SYSTEM_PROMPT}] + state["messages"]


def get_impact_analyzer_agent(model, tools):
    agent = create_react_agent(model=model, tools=tools, prompt=prompt, debug=True)
    return agent
