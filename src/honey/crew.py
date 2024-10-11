from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv
load_dotenv()

from honey.tools.elevenlabs_tts_tool import ElevenLabsTTSTool
from honey.tools.database_tool import DatabaseUpdateTool

@CrewBase
class HoneyCrew:
    """Honey Crew"""

    @agent
    def text_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['text_agent'],
            tools=[ElevenLabsTTSTool(), DatabaseUpdateTool()],
            allow_delegation=False,
            verbose=True
        )

    @task
    def generate_text_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_text']
        )

    @task
    def tts_and_update_task(self) -> Task:
        return Task(
            config=self.tasks_config['tts_and_update']
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Honey Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
