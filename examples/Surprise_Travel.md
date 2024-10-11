# Surprise Travel

- File `crew.py`:

```python
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# Check our tools documentation for more information on how to use them
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from pydantic import BaseModel, Field
from typing import List, Optional

class Activity(BaseModel):
    name: str = Field(..., description="Name of the activity")
    location: str = Field(..., description="Location of the activity")
    description: str = Field(..., description="Description of the activity")
    date: str = Field(..., description="Date of the activity")
    cousine: str = Field(..., description="Cousine of the restaurant")
    why_its_suitable: str = Field(..., description="Why it's suitable for the traveler")
    reviews: Optional[List[str]] = Field(..., description="List of reviews")
    rating: Optional[float] = Field(..., description="Rating of the activity")

class DayPlan(BaseModel):
	date: str = Field(..., description="Date of the day")
	activities: List[Activity] = Field(..., description="List of activities")
	restaurants: List[str] = Field(..., description="List of restaurants")
	flight: Optional[str] = Field(None, description="Flight information")

class Itinerary(BaseModel):
  name: str = Field(..., description="Name of the itinerary, something funny")
  day_plans: List[DayPlan] = Field(..., description="List of day plans")
  hotel: str = Field(..., description="Hotel information")

@CrewBase
class SurpriseTravelCrew():
    """SurpriseTravel crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def personalized_activity_planner(self) -> Agent:
        return Agent(
            config=self.agents_config['personalized_activity_planner'],
            tools=[SerperDevTool(), ScrapeWebsiteTool()], # Example of custom tool, loaded at the beginning of file
            verbose=True,
            allow_delegation=False,
        )

    @agent
    def restaurant_scout(self) -> Agent:
        return Agent(
            config=self.agents_config['restaurant_scout'],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            verbose=True,
            allow_delegation=False,
        )

    @agent
    def itinerary_compiler(self) -> Agent:
        return Agent(
            config=self.agents_config['itinerary_compiler'],
            tools=[SerperDevTool()],
            verbose=True,
            allow_delegation=False,
        )

    @task
    def personalized_activity_planning_task(self) -> Task:
        return Task(
            config=self.tasks_config['personalized_activity_planning_task'],
            agent=self.personalized_activity_planner()
        )

    @task
    def restaurant_scenic_location_scout_task(self) -> Task:
        return Task(
            config=self.tasks_config['restaurant_scenic_location_scout_task'],
            agent=self.restaurant_scout()
        )

    @task
    def itinerary_compilation_task(self) -> Task:
        return Task(
            config=self.tasks_config['itinerary_compilation_task'],
            agent=self.itinerary_compiler(),
            output_json=Itinerary
        )

    @crew
    def crew(self) -> Crew:
        """Creates the SurpriseTravel crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=2,
            # process=Process.hierarchical, # In case you want to use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
```

- File `main.py`:

```python
#!/usr/bin/env python
import sys
from surprise_travel.crew import SurpriseTravelCrew


def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {
        'origin': 'São Paulo, GRU',
        'destination': 'New York, JFK',
        'age': 31,
        'hotel_location': 'Brooklyn',
        'flight_information': 'GOL 1234, leaving at June 30th, 2024, 10:00',
        'trip_duration': '14 days'
    }
    result = SurpriseTravelCrew().crew().kickoff(inputs=inputs)
    print(result)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'origin': 'São Paulo, GRU',
        'destination': 'New York, JFK',
        'age': 31,
        'hotel_location': 'Brooklyn',
        'flight_information': 'GOL 1234, leaving at June 30th, 2024, 10:00',
        'trip_duration': '14 days'
    }
    try:
        SurpriseTravelCrew().crew().train(n_iterations=int(sys.argv[1]), inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")
```

- File `config/agents.yaml`:

```yaml
personalized_activity_planner:
  role: >
    Activity Planner
  goal: >
    Research and find cool things to do at the destination, including activities and events that match the traveler's interests and age group
  backstory: >
    You are skilled at creating personalized itineraries that cater to the specific preferences and demographics of travelers.

restaurant_scout:
  role: >
    Restaurant Scout
  goal: >
    Find highly-rated restaurants and dining experiences at the destination, and recommend scenic locations and fun activities
  backstory: >
    As a food lover, you know the best spots in town for a delightful culinary experience. You also have a knack for finding picturesque and entertaining locations.

itinerary_compiler:
  role: >
    Itinerary Compiler
  goal: >
    Compile all researched information into a comprehensive day-by-day itinerary, ensuring the integration of flights and hotel information
  backstory: >
    With an eye for detail, you organize all the information into a coherent and enjoyable travel plan.
```

- File `config/tasks.yaml`:

```yaml
personalized_activity_planning_task:
  description: >
    Research and find cool things to do at {destination}.
    Focus on activities and events that match the traveler's interests and age group.
    Utilize internet search tools and recommendation engines to gather the information.


    Traveler's information:


    - origin: {origin}

    - destination: {destination}

    - age of the traveler: {age}

    - hotel localtion: {hotel_location}

    - flight infromation: {flight_information}

    - how long is the trip: {trip_duration}
  expected_output: >
    A list of recommended activities and events for each day of the trip.
    Each entry should include the activity name, location, a brief description, and why it's suitable for the traveler.
    And potential reviews and ratings of the activities.

restaurant_scenic_location_scout_task:
  description: >
    Find highly-rated restaurants and dining experiences at {destination}.
    Recommend scenic locations and fun activities that align with the traveler's preferences.
    Use internet search tools, restaurant review sites, and travel guides.
    Make sure to find a variety of options to suit different tastes and budgets, and ratings for them.

    Traveler's information:


    - origin: {origin}

    - destination: {destination}

    - age of the traveler: {age}

    - hotel localtion: {hotel_location}

    - flight infromation: {flight_information}

    - how long is the trip: {trip_duration}
  expected_output: >
    A list of recommended restaurants, scenic locations, and fun activities for each day of the trip.
    Each entry should include the name, location (address), type of cuisine or activity, and a brief description and ratings.

itinerary_compilation_task:
  description: >
    Compile all researched information into a comprehensive day-by-day itinerary for the trip to {destination}.
    Ensure the itinerary integrates flights, hotel information, and all planned activities and dining experiences.
    Use text formatting and document creation tools to organize the information.
  expected_output: >
    A detailed itinerary document, the itinerary should include a day-by-day
    plan with flights, hotel details, activities, restaurants, and scenic locations.
```
