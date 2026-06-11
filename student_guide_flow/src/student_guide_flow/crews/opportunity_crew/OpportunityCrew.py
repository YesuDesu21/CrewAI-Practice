from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.llm import LLM


local_llm = LLM(
    model="ollama/llama3.1",
    base_url="http://localhost:11434"
)

@CrewBase
class OpportunityCrew():
    """OpportunityCrew crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def career_scouting_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['career_scouting_agent'], # type: ignore[index]
            verbose=True
        )

    @agent
    def campus_engagement_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config['campus_engagement_strategist'], # type: ignore[index]
            verbose=True
        )

    @task
    def scout_opportunities_task(self) -> Task:
        return Task(
            config=self.tasks_config['scout_opportunities_task'], # type: ignore[index]
        )

    @task
    def formulate_engagement_strategy_task(self) -> Task:
        return Task(
            config=self.tasks_config['formulate_engagement_strategy_task'], # type: ignore[index]
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the OpportunityCrew crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
