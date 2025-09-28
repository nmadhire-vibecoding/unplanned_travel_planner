from crewai import Agent, Crew, Process, Task
from crewai.llm import LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
import os
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class UnplannedTravelPlanner():
    """UnplannedTravelPlanner crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def flight_researcher(self) -> Agent:
        llm = self._maybe_gemini_llm()
        return Agent(
            config=self.agents_config['flight_researcher'],  # type: ignore[index]
            verbose=True,
            llm=llm,
        )

    @agent
    def hotel_researcher(self) -> Agent:
        llm = self._maybe_gemini_llm()
        return Agent(
            config=self.agents_config['hotel_researcher'],  # type: ignore[index]
            verbose=True,
            llm=llm,
        )

    @agent
    def sightseeing_researcher(self) -> Agent:
        llm = self._maybe_gemini_llm()
        return Agent(
            config=self.agents_config['sightseeing_researcher'],  # type: ignore[index]
            verbose=True,
            llm=llm,
        )

    @agent
    def itinerary_planner(self) -> Agent:
        llm = self._maybe_gemini_llm()
        return Agent(
            config=self.agents_config['itinerary_planner'],  # type: ignore[index]
            verbose=True,
            llm=llm,
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def flight_research_task(self) -> Task:
        return Task(
            config=self.tasks_config['flight_research_task'],  # type: ignore[index]
        )

    @task
    def hotel_research_task(self) -> Task:
        return Task(
            config=self.tasks_config['hotel_research_task'],  # type: ignore[index]
        )

    @task
    def sightseeing_research_task(self) -> Task:
        return Task(
            config=self.tasks_config['sightseeing_research_task'],  # type: ignore[index]
        )

    @task
    def itinerary_planning_task(self) -> Task:
        return Task(
            config=self.tasks_config['itinerary_planning_task'],  # type: ignore[index]
            output_file='itinerary.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the UnplannedTravelPlanner crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )

    # Internal helper to construct a Gemini LLM via CrewAI wrapper if env vars request it
    def _maybe_gemini_llm(self):  # type: ignore[override]
        if os.getenv("USE_GEMINI", "1") == "0":
            return None
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return None
        # CrewAI LLM wrapper accepts provider-specific params
        model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        temperature = float(os.getenv("GEMINI_TEMPERATURE", "0.7"))
        try:
            return LLM(
                model=model,
                provider="google",
                api_key=api_key,
                temperature=temperature,
            )
        except Exception:
            return None
