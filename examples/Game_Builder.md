# Game Builder

- File `crew.py`:

```python
from typing import List
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class GameBuilderCrew:
    """GameBuilder crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def senior_engineer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['senior_engineer_agent'],
            allow_delegation=False,
            verbose=True
        )

    @agent
    def qa_engineer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['qa_engineer_agent'],
            allow_delegation=False,
            verbose=True
        )

    @agent
    def chief_qa_engineer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['chief_qa_engineer_agent'],
            allow_delegation=True,
            verbose=True
        )


    @task
    def code_task(self) -> Task:
        return Task(
            config=self.tasks_config['code_task'],
            agent=self.senior_engineer_agent()
        )

    @task
    def review_task(self) -> Task:
        return Task(
            config=self.tasks_config['review_task'],
            agent=self.qa_engineer_agent(),
            #### output_json=ResearchRoleRequirements
        )

    @task
    def evaluate_task(self) -> Task:
        return Task(
            config=self.tasks_config['evaluate_task'],
            agent=self.chief_qa_engineer_agent()
        )

    @crew
    def crew(self) -> Crew:
        """Creates the GameBuilderCrew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
```

- File `main.py`:

```python
import sys
import yaml
from game_builder_crew.crew import GameBuilderCrew


def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    print("## Welcome to the Game Crew")
    print('-------------------------------')

    with open('src/game_builder_crew/config/gamedesign.yaml', 'r', encoding='utf-8') as file:
        examples = yaml.safe_load(file)

    inputs = {
        'game' :  examples['example3_snake']
    }
    game= GameBuilderCrew().crew().kickoff(inputs=inputs)

    print("\n\n########################")
    print("## Here is the result")
    print("########################\n")
    print("final code for the game:")
    print(game)


def train():
    """
    Train the crew for a given number of iterations.
    """

    with open('src/game_builder_crew/config/gamedesign.yaml', 'r', encoding='utf-8') as file:
        examples = yaml.safe_load(file)

    inputs = {
        'game' : examples['example1_pacman']
    }
    try:
        GameBuilderCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")
```

- File `config/agents.yaml`

```yaml
senior_engineer_agent:
  role: >
    Senior Software Engineer
  goal: >
    Create software as needed
  backstory: >
    You are a Senior Software Engineer at a leading tech think tank.
    Your expertise in programming in python. and do your best to produce perfect code

qa_engineer_agent:
  role: >
    Software Quality Control Engineer
  goal: >
    Create Perfect code, by analyzing the code that is given for errors
  backstory: >
    You are a software engineer that specializes in checking code
    for errors. You have an eye for detail and a knack for finding
    hidden bugs.
    You check for missing imports, variable declarations, mismatched
    brackets and syntax errors.
    You also check for security vulnerabilities, and logic errors

chief_qa_engineer_agent:
  role: >
    Chief Software Quality Control Engineer
  goal: >
    Ensure that the code does the job that it is supposed to do
  backstory: >
    You feel that programmers always do only half the job, so you are
    super dedicate to make high quality code.
```

- File `config/tasks.yaml`

```yaml
code_task:
  description: >
    You will create a game using python, these are the instructions:

    Instructions
    ------------
    {game}

  expected_output: >
    Your Final answer must be the full python code, only the python code and nothing else.

review_task:
  description: >
    You will create a game using python, these are the instructions:

    Instructions
    ------------
    {game}

    Using the code you got, check for errors. Check for logic errors,
    syntax errors, missing imports, variable declarations, mismatched brackets,
    and security vulnerabilities.
  expected_output: >
    Your Final answer must be the full python code, only the python code and nothing else.

evaluate_task:
  description: >
    You are helping create a game using python, these are the instructions:

    Instructions
    ------------
    {game}

    You will look over the code to insure that it is complete and
    does the job that it is supposed to do.
  expected_output: >
    Your Final answer must be the full python code, only the python code and nothing else.
```
