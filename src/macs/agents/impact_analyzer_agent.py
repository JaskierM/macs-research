from langchain.agents import initialize_agent, AgentType
from langchain.agents.agent import AgentExecutor
from langchain.prompts import PromptTemplate


def get_custom_prompt() -> PromptTemplate:
    return PromptTemplate.from_template(
        """
        You are a senior security analyst specialized in translating technical vulnerabilities into real-world business impact.
        Your goal is to evaluate the potential business risks of identified vulnerabilities and rate their severity clearly.
        Use available tools to gather technical context and provide your assessment.

        Question: {input}
        Thought:
        """
    )


def get_impact_analyzer_agent(llm, tools) -> AgentExecutor:
    custom_prompt = get_custom_prompt()

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        agent_kwargs={"prefix": custom_prompt.template},
        verbose=True,
        handle_parsing_errors=True,
    )

    return agent
