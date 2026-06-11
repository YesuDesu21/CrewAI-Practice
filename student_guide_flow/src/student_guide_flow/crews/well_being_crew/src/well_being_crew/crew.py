from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent


@CrewBase
class WellBeingCrew():
    """WellBeingCrew crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def fitness_nutrition_guide(self) -> Agent:
        return Agent(
            config=self.agents_config['fitness_nutrition_guide'], # type: ignore[index]
            verbose=True
        )

    @agent
    def mindfulness_supporter(self) -> Agent:
        return Agent(
            config=self.agents_config['mindfulness_supporter'], # type: ignore[index]
            verbose=True
        )

    @task
    def build_athletic_routine_task(self) -> Task:
        return Task(
            config=self.tasks_config['build_athletic_routine_task'], # type: ignore[index]
        )

    @task
    def evaluate_mental_health_task(self) -> Task:
        return Task(
            config=self.tasks_config['evaluate_mental_health_task'], # type: ignore[index]
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the WellBeingCrew crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
