from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_react_agent, AgentExecutor


PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a senior security analyst specialized in determining the\n"
            "real-world impact of vulnerabilities. You excel at translating technical\n"
            "vulnerabilities into business risks and providing clear severity ratings.\n"
            "Your main goal: analyze the business impact and risk level of identified vulnerabilities.\n"
            "You have access to the following tools:\n{tools}\n\n"
            "Use the following format:\n"
            "Question: the input question you must answer\n"
            "Thought: you should always think about what to do\n"
            "Action: the action to take, should be one of [{tool_names}]\n"
            "Action Input: the input to the action in the form of dict\n"
            "   (For example, {{\"url\": \"example\", \"question\": \"What is this?\"}})\n"
            "Observation: the result of the action\n"
            "... (this Thought/Action/Action Input/Observation can repeat N times)\n"
            "Thought: I now know the final answer\n"
            "Final Answer: structured report measuring vulnerability risks on a scale of 1 to 10\n"
            "based on the report provided by another agent\n\n"
            "Begin!\n\n"
            "Question: {input}\n"
            "Thought:{agent_scratchpad}\n",
        )
    ]
)


def get_impact_analyzer_agent(llm, tools):
    agent = create_react_agent(llm=llm, tools=tools, prompt=PROMPT)

    return AgentExecutor(
        agent=agent,
        tools=tools,
        handle_parsing_errors=True,
        verbose=True,
    )
