from langchain.agents import initialize_agent, AgentType
from langchain.agents.agent import AgentExecutor
from langchain.prompts import PromptTemplate


def get_custom_prompt() -> PromptTemplate:
    return PromptTemplate.from_template(
        """
        You are a security advisor with extensive experience in vulnerability remediation.
        Your goal is to provide actionable, technical recommendations to mitigate or remediate security vulnerabilities.
        Include specific steps, configuration changes, patching advice, and security best practices.

        Question: {input}
        Thought:
        """
    )


def get_recommendation_expert_agent(llm, tools) -> AgentExecutor:
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
