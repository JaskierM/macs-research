class Crew:

    def __init__(self, agents: list, tasks: list, verbose: int = 1):
        self.agents = agents
        self.tasks = tasks
        self.verbose = verbose

    def run(self):
        context = ""
        for idx, task in enumerate(self.tasks):
            if self.verbose:
                print(
                    f"\n--- Running Task {idx + 1}: ---\n{task.description.strip()}\n"
                )
            result = task.run(input_context=context)
            context += f"\n\n=== Output from Task {idx + 1} ===\n{result}"
        return context
