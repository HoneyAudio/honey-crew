# Stock Analysis

- File `crew.py`:

```python
from typing import List
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from tools.calculator_tool import CalculatorTool
from tools.sec_tools import SEC10KTool, SEC10QTool

from crewai_tools import WebsiteSearchTool, ScrapeWebsiteTool, TXTSearchTool

from dotenv import load_dotenv
load_dotenv()

from langchain.llms import Ollama
llm = Ollama(model="llama3.1")

@CrewBase
class StockAnalysisCrew:
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def financial_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['financial_analyst'],
            verbose=True,
            llm=llm,
            tools=[
                ScrapeWebsiteTool(),
                WebsiteSearchTool(),
                CalculatorTool(),
                SEC10QTool("AMZN"),
                SEC10KTool("AMZN"),
            ]
        )

    @task
    def financial_analysis(self) -> Task:
        return Task(
            config=self.tasks_config['financial_analysis'],
            agent=self.financial_agent(),
        )


    @agent
    def research_analyst_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['research_analyst'],
            verbose=True,
            llm=llm,
            tools=[
                ScrapeWebsiteTool(),
                # WebsiteSearchTool(),
                SEC10QTool("AMZN"),
                SEC10KTool("AMZN"),
            ]
        )

    @task
    def research(self) -> Task:
        return Task(
            config=self.tasks_config['research'],
            agent=self.research_analyst_agent(),
        )

    @agent
    def financial_analyst_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['financial_analyst'],
            verbose=True,
            llm=llm,
            tools=[
                ScrapeWebsiteTool(),
                WebsiteSearchTool(),
                CalculatorTool(),
                SEC10QTool(),
                SEC10KTool(),
            ]
        )

    @task
    def financial_analysis(self) -> Task:
        return Task(
            config=self.tasks_config['financial_analysis'],
            agent=self.financial_analyst_agent(),
        )

    @task
    def filings_analysis(self) -> Task:
        return Task(
            config=self.tasks_config['filings_analysis'],
            agent=self.financial_analyst_agent(),
        )

    @agent
    def investment_advisor_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['investment_advisor'],
            verbose=True,
            llm=llm,
            tools=[
                ScrapeWebsiteTool(),
                WebsiteSearchTool(),
                CalculatorTool(),
            ]
        )

    @task
    def recommend(self) -> Task:
        return Task(
            config=self.tasks_config['recommend'],
            agent=self.investment_advisor_agent(),
        )


    @crew
    def crew(self) -> Crew:
        """Creates the Stock Analysis"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
```

- File `main.py`:

```python
import sys
from crew import StockAnalysisCrew

def run():
    inputs = {
        'query': 'What is the company you want to analyze?',
        'company_stock': 'AMZN',
    }
    return StockAnalysisCrew().crew().kickoff(inputs=inputs)

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'query': 'What is last years revenue',
        'company_stock': 'AMZN',
    }
    try:
        StockAnalysisCrew().crew().train(n_iterations=int(sys.argv[1]), inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

if __name__ == "__main__":
    print("## Welcome to Stock Analysis Crew")
    print('-------------------------------')
    result = run()
    print("\n\n########################")
    print("## Here is the Report")
    print("########################\n")
    print(result)
```

- File `config/agents.yaml`

```yaml
financial_analyst:
  role: >
    The Best Financial Analyst
  goal: >
    Impress all customers with your financial data and market trends analysis
  backstory: >
    The most seasoned financial analyst with lots of expertise in stock market analysis and investment
    strategies that is working for a super important customer.

research_analyst:
  role: >
    Staff Research Analyst
  goal: >
    Being the best at gathering, interpreting data and amazing
    your customer with it
  backstory: >
    Known as the BEST research analyst, you're skilled in sifting through news, company announcements,
    and market sentiments. Now you're working on a super important customer.

investment_advisor:
  role: >
    Private Investment Advisor
  goal: >
    Impress your customers with full analyses over stocks
    and complete investment recommendations
  backstory: >
    You're the most experienced investment advisor
    and you combine various analytical insights to formulate
    strategic investment advice. You are now working for
    a super important customer you need to impress.
```

- File `config/tasks.yaml`

```yaml
financial_analysis:
  description: >
    Conduct a thorough analysis of {company_stock}'s stock financial health and market performance. This includes examining key financial metrics such as
    P/E ratio, EPS growth, revenue trends, and debt-to-equity ratio. Also, analyze the stock's performance in comparison 
    to its industry peers and overall market trends.

  expected_output: >
    The final report must expand on the summary provided but now 
    including a clear assessment of the stock's financial standing, its strengths and weaknesses, 
    and how it fares against its competitors in the current market scenario.
    Make sure to use the most recent data possible.

research:
  description: >
    Collect and summarize recent news articles, press
    releases, and market analyses related to the {company_stock} stock and its industry.
    Pay special attention to any significant events, market sentiments, and analysts' opinions. 
    Also include upcoming events like earnings and others.

  expected_output: >
    A report that includes a comprehensive summary of the latest news, 
    any notable shifts in market sentiment, and potential impacts on the stock. Also make sure to return the stock ticker as {company_stock}.
    Make sure to use the most recent data as possible.

filings_analysis:
  description: >
    Analyze the latest 10-Q and 10-K filings from EDGAR for the stock {company_stock} in question. 
    Focus on key sections like Management's Discussion and analysis, financial statements, insider trading activity, 
    and any disclosed risks. Extract relevant data and insights that could influence
    the stock's future performance.

  expected_output: >
    Final answer must be an expanded report that now also highlights significant findings
    from these filings including any red flags or positive indicators for your customer.

recommend:
  description: >
    Review and synthesize the analyses provided by the
    Financial Analyst and the Research Analyst.
    Combine these insights to form a comprehensive
    investment recommendation. You MUST Consider all aspects, including financial
    health, market sentiment, and qualitative data from
    EDGAR filings. 

    Make sure to include a section that shows insider 
    trading activity, and upcoming events like earnings.

  expected_output: >
    Your final answer MUST be a recommendation for your customer. It should be a full super detailed report, providing a 
    clear investment stance and strategy with supporting evidence.
    Make it pretty and well formatted for your customer.
```

- File `tools/calculator_tool.py`

```python
from crewai_tools import BaseTool


class CalculatorTool(BaseTool):
    name: str = "Calculator tool"
    description: str = (
        "Useful to perform any mathematical calculations, like sum, minus, multiplication, division, etc. The input to this tool should be a mathematical  expression, a couple examples are `200*7` or `5000/2*10."
    )

    def _run(self, operation: str) -> int:
        # Implementation goes here
        return eval(operation)
```

- File `tools/sec_tools.py`

```python
import os
from typing import Any, Optional, Type
from pydantic.v1 import BaseModel, Field
from crewai_tools import RagTool
from sec_api import QueryApi  # Make sure to have sec_api installed
from embedchain.models.data_type import DataType
import requests
import html2text
import re

class FixedSEC10KToolSchema(BaseModel):
    """Input for SEC10KTool."""
    search_query: str = Field(
        ...,
        description="Mandatory query you would like to search from the 10-K report",
    )

class SEC10KToolSchema(FixedSEC10KToolSchema):
    """Input for SEC10KTool."""
    stock_name: str = Field(
        ..., description="Mandatory valid stock name you would like to search"
    )

class SEC10KTool(RagTool):
    name: str = "Search in the specified 10-K form"
    description: str = "A tool that can be used to semantic search a query from a 10-K form for a specified company."
    args_schema: Type[BaseModel] = SEC10KToolSchema

    def __init__(self, stock_name: Optional[str] = None, **kwargs):
        print("enter init")
        # exit()
        super().__init__(**kwargs)
        if stock_name is not None:
            content = self.get_10k_url_content(stock_name)
            if content:
                self.add(content)
                # print("exit init")
                # exit()
                self.description = f"A tool that can be used to semantic search a query from {stock_name}'s latest 10-K SEC form's content as a txt file."
                self.args_schema = FixedSEC10KToolSchema
                self._generate_description()

    def get_10k_url_content(self, stock_name: str) -> Optional[str]:
        """Fetches the URL content as txt of the latest 10-K form for the given stock name."""
        try:
            queryApi = QueryApi(api_key=os.environ['SEC_API_API_KEY'])
            query = {
                "query": {
                    "query_string": {
                        "query": f"ticker:{stock_name} AND formType:\"10-K\""
                    }
                },
                "from": "0",
                "size": "1",
                "sort": [{ "filedAt": { "order": "desc" }}]
            }
            filings = queryApi.get_filings(query)['filings']
            if len(filings) == 0:
                print("No filings found for this stock.")
                return None

            url = filings[0]['linkToFilingDetails']

            headers = {
                "User-Agent": "crewai.com bisan@crewai.com",
                "Accept-Encoding": "gzip, deflate",
                "Host": "www.sec.gov"
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            h = html2text.HTML2Text()
            h.ignore_links = False
            text = h.handle(response.content.decode("utf-8"))

            text = re.sub(r"[^a-zA-Z$0-9\s\n]", "", text)
            return text
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")
            return None
        except Exception as e:
            print(f"Error fetching 10-K URL: {e}")
            return None

    def add(self, *args: Any, **kwargs: Any) -> None:
        kwargs["data_type"] = DataType.TEXT
        super().add(*args, **kwargs)

    def _run(self, search_query: str, **kwargs: Any) -> Any:
        return super()._run(query=search_query, **kwargs)


class FixedSEC10QToolSchema(BaseModel):
    """Input for SEC10QTool."""
    search_query: str = Field(
        ...,
        description="Mandatory query you would like to search from the 10-Q report",
    )

class SEC10QToolSchema(FixedSEC10QToolSchema):
    """Input for SEC10QTool."""
    stock_name: str = Field(
        ..., description="Mandatory valid stock name you would like to search"
    )

class SEC10QTool(RagTool):
    name: str = "Search in the specified 10-Q form"
    description: str = "A tool that can be used to semantic search a query from a 10-Q form for a specified company."
    args_schema: Type[BaseModel] = SEC10QToolSchema

    def __init__(self, stock_name: Optional[str] = None, **kwargs):
        print("enter init")
        # exit()
        super().__init__(**kwargs)
        if stock_name is not None:
            content = self.get_10q_url_content(stock_name)
            if content:
                self.add(content)
                self.description = f"A tool that can be used to semantic search a query from {stock_name}'s latest 10-Q SEC form's content as a txt file."
                self.args_schema = FixedSEC10QToolSchema
                self._generate_description()

    def get_10q_url_content(self, stock_name: str) -> Optional[str]:
        """Fetches the URL content as txt of the latest 10-Q form for the given stock name."""
        try:
            queryApi = QueryApi(api_key=os.environ['SEC_API_API_KEY'])
            query = {
                "query": {
                    "query_string": {
                        "query": f"ticker:{stock_name} AND formType:\"10-Q\""
                    }
                },
                "from": "0",
                "size": "1",
                "sort": [{ "filedAt": { "order": "desc" }}]
            }
            filings = queryApi.get_filings(query)['filings']
            if len(filings) == 0:
                print("No filings found for this stock.")
                return None

            url = filings[0]['linkToFilingDetails']

            headers = {
                "User-Agent": "crewai.com bisan@crewai.com",
                "Accept-Encoding": "gzip, deflate",
                "Host": "www.sec.gov"
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            h = html2text.HTML2Text()
            h.ignore_links = False
            text = h.handle(response.content.decode("utf-8"))

            # Removing all non-English words, dollar signs, numbers, and newlines from text
            text = re.sub(r"[^a-zA-Z$0-9\s\n]", "", text)
            return text
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e}")
            return None
        except Exception as e:
            print(f"Error fetching 10-Q URL: {e}")
            return None

    def add(self, *args: Any, **kwargs: Any) -> None:
        kwargs["data_type"] = DataType.TEXT
        super().add(*args, **kwargs)

    def _run(self, search_query: str, **kwargs: Any) -> Any:
        return super()._run(query=search_query, **kwargs)
```
