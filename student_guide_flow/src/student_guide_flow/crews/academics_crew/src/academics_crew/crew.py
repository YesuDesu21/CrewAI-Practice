from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent


@CrewBase
class AcademicsCrew():
    """AcademicsCrew crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def performance_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['performance_analyst'], # type: ignore[index]
            verbose=True
        )

    @agent
    def time_management_coach(self) -> Agent:
        return Agent(
            config=self.agents_config['time_management_coach'], # type: ignore[index]
            verbose=True
        )

    @task
    def analyze_academic_standing_task(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_academic_standing_task'], # type: ignore[index]
        )

    @task
    def optimize_schedule_task(self) -> Task:
        return Task(
            config=self.tasks_config['optimize_schedule_task'], # type: ignore[index]
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the AcademicsCrew crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
