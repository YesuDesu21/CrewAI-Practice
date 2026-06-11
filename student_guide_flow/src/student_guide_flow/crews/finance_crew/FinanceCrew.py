from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent

from crewai.llm import LLM


local_llm = LLM(
    model="ollama/llama3.1",
    base_url="http://localhost:11434"
)

@CrewBase
class FinanceCrew():
    """FinanceCrew crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def expense_tracker(self) -> Agent:
        return Agent(
            config=self.agents_config['expense_tracker'], # type: ignore[index]
            verbose=True
        )

    @agent
    def savings_debt_advisor(self) -> Agent:
        return Agent(
            config=self.agents_config['savings_debt_advisor'], # type: ignore[index]
            verbose=True
        )

    @task
    def audit_expenses_task(self) -> Task:
        return Task(
            config=self.tasks_config['audit_expenses_task'], # type: ignore[index]
        )

    @task
    def develop_financial_strategy_task(self) -> Task:
        return Task(
            config=self.tasks_config['develop_financial_strategy_task'], # type: ignore[index]
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the FinanceCrew crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
