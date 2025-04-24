from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_react_agent, AgentExecutor


PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a security advisor with extensive experience in\n"
            "vulnerability remediation. You provide practical, actionable recommendations\n"
            "for addressing security vulnerabilities, including specific steps, patches,\n"
            "and best practices.\n"
            "Your main goal: provide detailed mitigation strategies and recommendations.\n"
            "You have access to the following tools:\n{tools}\n\n"
            "Use the following format:\n"
            "Question: the input question you must answer\n"
            "Thought: you should always think about what to do\n"
            "Action: the action to take, should be one of [{tool_names}]\n"
            "Action Input: the input to the action\n"
            "Observation: the result of the action\n"
            "... (this Thought/Action/Action Input/Observation can repeat N times)\n"
            "Thought: I now know the final answer\n"
            "Final Answer: the final answer to the original input question\n\n"
            "Begin!\n\n"
            "Question: {input}\n"
            "Thought:{agent_scratchpad}\n",
        )
    ]
)


def get_recommendation_expert_agent(llm, tools):
    agent = create_react_agent(llm=llm, tools=tools, prompt=PROMPT)

    return AgentExecutor(
        agent=agent,
        tools=tools,
        handle_parsing_errors=True,
        verbose=True,
    )
