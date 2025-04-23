class Task:

    def __init__(self, description: str, agent, expected_output: str = ""):
        self.description = description
        self.agent = agent
        self.expected_output = expected_output
        self.result = None

    def run(self, input_context: str = None) -> str:
        prompt = self.description
        if input_context:
            prompt += f"\n\nContext from previous task:\n{input_context}"
        self.result = self.agent.run(prompt)
        return self.result
