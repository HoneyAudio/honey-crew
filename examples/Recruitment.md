# Recruitment

- File `crew.py`:

```python
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from recruitment.tools.linkedin import LinkedInTool

@CrewBase
class RecruitmentCrew():
    """Recruitment crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
						tools=[SerperDevTool(), ScrapeWebsiteTool(), LinkedInTool()],
            allow_delegation=False,
						verbose=True
        )

    @agent
    def matcher(self) -> Agent:
        return Agent(
            config=self.agents_config['matcher'],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            allow_delegation=False,
						verbose=True
        )

    @agent
    def communicator(self) -> Agent:
        return Agent(
            config=self.agents_config['communicator'],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            allow_delegation=False,
						verbose=True
        )

    @agent
    def reporter(self) -> Agent:
        return Agent(
            config=self.agents_config['reporter'],
            allow_delegation=False,
						verbose=True
        )

    @task
    def research_candidates_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_candidates_task'],
            agent=self.researcher()
        )

    @task
    def match_and_score_candidates_task(self) -> Task:
        return Task(
            config=self.tasks_config['match_and_score_candidates_task'],
            agent=self.matcher()
        )

    @task
    def outreach_strategy_task(self) -> Task:
        return Task(
            config=self.tasks_config['outreach_strategy_task'],
            agent=self.communicator()
        )

    @task
    def report_candidates_task(self) -> Task:
        return Task(
            config=self.tasks_config['report_candidates_task'],
            agent=self.reporter(),
            context=[self.research_candidates_task(), self.match_and_score_candidates_task(), self.outreach_strategy_task()],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Recruitment crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=2,
        )
```

- File `main.py`:

```python
#!/usr/bin/env python
import sys
from recruitment.crew import RecruitmentCrew


def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {
        'job_requirements': """
        job_requirement:
  title: >
    Ruby on Rails and React Engineer
  description: >
    We are seeking a skilled Ruby on Rails and React engineer to join our team.
    The ideal candidate will have experience in both backend and frontend development,
    with a passion for building high-quality web applications.

  responsibilities: >
    - Develop and maintain web applications using Ruby on Rails and React.
    - Collaborate with teams to define and implement new features.
    - Write clean, maintainable, and efficient code.
    - Ensure application performance and responsiveness.
    - Identify and resolve bottlenecks and bugs.

  requirements: >
    - Proven experience with Ruby on Rails and React.
    - Strong understanding of object-oriented programming.
    - Proficiency with JavaScript, HTML, CSS, and React.
    - Experience with SQL or NoSQL databases.
    - Familiarity with code versioning tools, such as Git.

  preferred_qualifications: >
    - Experience with cloud services (AWS, Google Cloud, or Azure).
    - Familiarity with Docker and Kubernetes.
    - Knowledge of GraphQL.
    - Bachelor's degree in Computer Science or a related field.

  perks_and_benefits: >
    - Competitive salary and bonuses.
    - Health, dental, and vision insurance.
    - Flexible working hours and remote work options.
    - Professional development opportunities.
        """
    }
    RecruitmentCrew().crew().kickoff(inputs=inputs)

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'job_requirements': """
        job_requirement:
  title: >
    Ruby on Rails and React Engineer
  description: >
    We are seeking a skilled Ruby on Rails and React engineer to join our team.
    The ideal candidate will have experience in both backend and frontend development,
    with a passion for building high-quality web applications.

  responsibilities: >
    - Develop and maintain web applications using Ruby on Rails and React.
    - Collaborate with teams to define and implement new features.
    - Write clean, maintainable, and efficient code.
    - Ensure application performance and responsiveness.
    - Identify and resolve bottlenecks and bugs.

  requirements: >
    - Proven experience with Ruby on Rails and React.
    - Strong understanding of object-oriented programming.
    - Proficiency with JavaScript, HTML, CSS, and React.
    - Experience with SQL or NoSQL databases.
    - Familiarity with code versioning tools, such as Git.

  preferred_qualifications: >
    - Experience with cloud services (AWS, Google Cloud, or Azure).
    - Familiarity with Docker and Kubernetes.
    - Knowledge of GraphQL.
    - Bachelor's degree in Computer Science or a related field.

  perks_and_benefits: >
    - Competitive salary and bonuses.
    - Health, dental, and vision insurance.
    - Flexible working hours and remote work options.
    - Professional development opportunities.
        """
    }
    try:
        RecruitmentCrew().crew().train(n_iterations=int(sys.argv[1]), inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")
```

- File `config/agents.yaml`

```yaml
researcher:
  role: >
    Job Candidate Researcher
  goal: >
    Find potential candidates for the job
  backstory: >
    You are adept at finding the right candidates by exploring various online
    resources. Your skill in identifying suitable candidates ensures the best
    match for job positions.

matcher:
  role: >
    Candidate Matcher and Scorer
  goal: >
    Match the candidates to the best jobs and score them
  backstory: >
    You have a knack for matching the right candidates to the right job positions
    using advanced algorithms and scoring techniques. Your scores help
    prioritize the best candidates for outreach.

communicator:
  role: >
    Candidate Outreach Strategist
  goal: >
    Develop outreach strategies for the selected candidates
  backstory: >
    You are skilled at creating effective outreach strategies and templates to
    engage candidates. Your communication tactics ensure high response rates
    from potential candidates.

reporter:
  role: >
    Candidate Reporting Specialist
  goal: >
    Report the best candidates to the recruiters
  backstory: >
    You are proficient at compiling and presenting detailed reports for recruiters.
    Your reports provide clear insights into the best candidates to pursue.
```

- File `config/tasks.yaml`

````yaml
research_candidates_task:
  description: >
    Conduct thorough research to find potential candidates for the specified job.
    Utilize various online resources and databases to gather a comprehensive list of potential candidates.
    Ensure that the candidates meet the job requirements provided.

    Job Requirements:
    {job_requirements}
  expected_output: >
    A list of 10 potential candidates with their contact information and brief profiles highlighting their suitability.

match_and_score_candidates_task:
  description: >
    Evaluate and match the candidates to the best job positions based on their qualifications and suitability.
    Score each candidate to reflect their alignment with the job requirements, ensuring a fair and transparent assessment process.
    Don't try to scrape people's linkedin, since you don't have access to it.

    Job Requirements:
    {job_requirements}
  expected_output: >
    A ranked list of candidates with detailed scores and justifications for each job position.

outreach_strategy_task:
  description: >
    Develop a comprehensive strategy to reach out to the selected candidates.
    Create effective outreach methods and templates that can engage the candidates and encourage them to consider the job opportunity.

    Job Requirements:
    {job_requirements}
  expected_output: >
    A detailed list of outreach methods and templates ready for implementation, including communication strategies and engagement tactics.

report_candidates_task:
  description: >
    Compile a comprehensive report for recruiters on the best candidates to put forward.
    Summarize the findings from the previous tasks and provide clear recommendations based on the job requirements.
  expected_output: >
    A detailed report with the best candidates to pursue, no need to include the job requirements formatted as markdown without '```', including profiles, scores, and outreach strategies.
````

- File `tools/client.py`

```python
import os
import urllib
from selenium.webdriver.common.by import By

from .driver import Driver

class Client:
  def __init__(self):
    url = 'https://linkedin.com/'
    cookie = {
      "name": "li_at",
      "value": os.environ["LINKEDIN_COOKIE"],
      "domain": ".linkedin.com"
    }

    self.driver = Driver(url, cookie)

  def find_people(self, skills):
    skills = skills.split(",")
    search = " ".join(skills)
    encoded_string = urllib.parse.quote(search.lower())
    url = f"https://www.linkedin.com/search/results/people/?keywords={encoded_string}"
    self.driver.navigate(url)

    people = self.driver.get_elements("ul li div div.linked-area")

    results = []
    for person in people:
      try:
        result = {}
        result["name"] = person.find_element(By.CSS_SELECTOR, "span.entity-result__title-line").text
        result["position"] = person.find_element(By.CSS_SELECTOR, "div.entity-result__primary-subtitle").text
        result["location"] = person.find_element(By.CSS_SELECTOR, "div.entity-result__secondary-subtitle").text
        result["profile_link"] = person.find_element(By.CSS_SELECTOR, "a.app-aware-link").get_attribute("href")
      except Exception as e:
        print(e)
        continue
      results.append(result)
    return results

  def close(self):
    self.driver.close()
```

- File `tools/driver.py`

```python
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

class Driver:
    def __init__(self, url, cookie=None):
        self.driver = self._create_driver(url, cookie)

    def navigate(self, url, wait=3):
        self.driver.get(url)
        time.sleep(wait)

    def scroll_to_bottom(self, wait=3):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(wait)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(wait)

    def get_element(self, selector):
        return self.driver.find_element(By.CSS_SELECTOR, selector)

    def get_elements(self, selector):
        return self.driver.find_elements(By.CSS_SELECTOR, selector)

    def fill_text_field(self, selector, text):
        element = self.get_element(selector)
        element.clear()
        element.send_keys(text)

    def click_button(self, selector):
        element = self.get_element(selector)
        element.click()

    def _create_driver(self, url, cookie):
        options = Options()
        # options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        driver.get(url)
        if cookie:
            driver.add_cookie(cookie)
        return driver

    def close(self):
        self.driver.close()
```

- File `tools/linkedin.py`

```python
from crewai_tools import BaseTool

from .client import Client as LinkedinClient


class LinkedInTool(BaseTool):
    name: str = "Retrieve LinkedIn profiles"
    description: str = (
        "Retrieve LinkedIn profiles given a list of skills. Comma separated"
    )

    def _run(self, skills: str) -> str:
        linkedin_client = LinkedinClient()
        people = linkedin_client.find_people(skills)
        people = self._format_publications_to_text(people)
        linkedin_client.close()
        return people

    def _format_publications_to_text(self, people):
        result = ["\n".join([
            "Person Profile",
            "-------------",
            p['name'],
            p['position'],
            p['location'],
            p["profile_link"],
        ]) for p in people]
        result = "\n\n".join(result)

        return result
```
