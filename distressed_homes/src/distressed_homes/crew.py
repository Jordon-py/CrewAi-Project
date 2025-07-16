# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators
# Learn more about YAML configuration files here:
# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
# If you would like to add tools to your agents, you can learn more about it here:
# https://docs.crewai.com/concepts/agents#agent-tools


from logging import config
import os
from typing import List
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
from langchain_openai import ChatOpenAI

# Initialize the LLM
llm = ChatOpenAI(
    model=os.getenv('GPT41','openai/gpt-4o'),
    OPENAI_API_KEY=os.getenv("OPENAI_API_KEY"),
    temperature=0.7,
)

# SerperDevTool automatically reads from SERPER_API_KEY environment variable
serper_dev_tool = SerperDevTool()

# ==========================================================
# Distressed Homes Crew
# ==========================================================
@CrewBase
class Distressed_Homes_Crew:
    """Distressed Homes Crew"""
    
    # Configuration file paths
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    
    # These properties will be populated by the decorated methods
    agents = List[Agent]
    tasks = List[Task]

    def __init__(self):
        """Initialize the crew with configuration loading"""
        print(f"Loading agents from {self.agents_config} and tasks from {self.tasks_config}")
        
    # ====================================================================
    # Define the agents you want to use
    # ====================================================================
    @agent
    def manager_llm(self) -> Agent:
        return Agent(
            config=self.agents_config['manager_llm'],
            llm=llm,
            verbose=True
        )
    
    @agent
    def scraper_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['scraper_agent'],
            tools=[ScrapeWebsiteTool(), serper_dev_tool],
            llm=llm,
            verbose=True
        )
    
    @agent
    def analyst_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['analyst_agent'],
            llm=llm,
            verbose=True
        )
    
    @agent
    def writer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['writer_agent'],
            llm=llm,
            verbose=True
        )
        
    @agent
    def acquisitions_prep_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['acquisitions_prep_agent'],
            llm=llm,
            verbose=True
        )
        
    @agent
    def investor_strategy_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['investor_strategy_agent'],
            llm=llm,
            verbose=True
        )

    # ====================================================================
    # Define the tasks you want to use
    # ====================================================================
    @task
    def manager_task(self) -> Task:
        return Task(
            config=self.tasks_config['manager_task'],
            output_file="results/manager_output.md"
        )
    @task
    def scrape_task(self) -> Task:
        return Task(
            config=self.tasks_config['scrape_task'],
            output_file="results/scraped_properties.md"
        )
    
    @task
    def analyst_task(self) -> Task:
        return Task(
            config=self.tasks_config['analyst_task'],
            output_file="results/analyzed_properties.md"
        )
    
    @task
    def report_task(self) -> Task:
        return Task(
            config=self.tasks_config['report_task'],
            output_file="results/distressed_report.md"
        )
    @task
    def acquisitions_prep_task(self) -> Task:
        return Task(
            config=self.tasks_config['acquisitions_prep_task'],
            output_file="results/prepared_properties.md"
        )
    @task
    def investor_strategy_task(self) -> Task:
        return Task(
            config=self.tasks_config['investor_strategy_task'],
            output_file="results/investor_strategy.md"
        )
        
    @crew
    def crew(self) -> Crew:
        """Creates the Distressed Homes crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,
            manager_llm=llm,
            verbose=True,
            allow_delegation=True,
        )
