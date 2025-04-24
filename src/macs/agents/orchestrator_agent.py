from langchain import LLMChain, PromptTemplate
from langchain.schema import BasePromptTemplate


class OrchestratorAgent:
    def __init__(self, llm, researcher, analyzer, recommender):
        self.llm = llm
        self.researcher = researcher
        self.analyzer = analyzer
        self.recommender = recommender

    def run(self, params):
        vuln_list = self.researcher.run(params)
        impact_analysis = self.analyzer.run({"vulnerabilities": vuln_list})
        recommendations = self.recommender.run(
            {"vulnerabilities": vuln_list, "analysis": impact_analysis}
        )

        report_template = PromptTemplate(
            input_variables=["vulnerabilities", "analysis", "recommendations"],
            template="""
                Сводный отчёт по исследованию:
                1. Обнаруженные уязвимости:
                {vulnerabilities}

                2. Анализ влияния:
                {analysis}

                3. Рекомендации по устранению:
                {recommendations}
            """,
        )
        report_chain = LLMChain(llm=self.llm, prompt=report_template)
        return report_chain.run(
            {
                "vulnerabilities": vuln_list,
                "analysis": impact_analysis,
                "recommendations": recommendations,
            }
        )
