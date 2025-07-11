# my_crew/src/my_crew_project/crew.py
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import SerperDevTool, CodeInterpreterTool

# Tools

search_tool = SerperDevTool()


code = """
import os
os.system("ls -la")
"""

CodeInterpreterTool(unsafe_mode=True).run(code=code)
code_interpreter = CodeInterpreterTool()


@CrewBase
class MyCrew():
    """MyCrewProject crew with explicit agent handoff/coordination"""

    agents = List[BaseAgent]
    tasks = List[Task]
    
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    llm = LLM(
        model="ollama/llama3.2:latest",
        base_url="http://localhost:11434"
    )
    code_llm = LLM(
        model="ollama/deepseek-r1:latest",
        base_url="http://localhost:11434"
    )

    @agent
    def manager_llm(self) -> Agent:
        """Specialized Reflexive Intelligence Manager LLM for async task delegation and supervision."""
        config = self.agents_config['manager_llm']
        print(f"[HANDOFF] Manager LLM handoff: {config.get('handoff','')}")
        # NOTE: Allow this agent to supervise and coordinate others
        return Agent(
            config=config,
            verbose=True,
            llm=self.llm,
            tools=[search_tool],  # Can use search if desired
            allow_delegation=True,  # must be true for orchestration
            planning=True,
            async_delegation=True,  # must be true for async delegation
        )

    @agent
    def fullstack_coding_expert(self) -> Agent:
        config = self.agents_config['fullstack_coding_expert']
        print(f"[HANDOFF] Fullstack Coding Expert handoff: {config.get('handoff','')}")
        return Agent(
            config=config,
            verbose=True,
            llm=self.code_llm,
            tools=[code_interpreter],
            allow_delegation=True,
            planning=True,
            
        )

    @agent
    def backend_coding_expert(self) -> Agent:
        config = self.agents_config['backend_coding_expert']
        print(f"[HANDOFF] Backend Coding Expert handoff: {config.get('handoff','')}")
        return Agent(
            config=config,
            verbose=True,
            llm=self.code_llm,
            tools=[code_interpreter],
            allow_delegation=True,
            planning=True
        )

    @agent
    def visualization_engineer(self) -> Agent:
        config = self.agents_config['visualization_engineer']
        print(f"[HANDOFF] Visualization Engineer handoff: {config.get('handoff','')}")
        return Agent(
            config=config,
            verbose=True,
            llm=self.code_llm,
            tools=[code_interpreter],
            allow_delegation=True,
            planning=True
        )

    @task
    def fullstack_coding_task(self) -> Task:
        config = self.tasks_config['fullstack_coding_task']
        print(f"[HANDOFF] Fullstack Coding Task handoff: {config.get('handoff','')}")
        return Task(
            config=config,
            output_file='fullstack_solution.md'
        )

    @task
    def backend_coding_task(self) -> Task:
        config = self.tasks_config['backend_coding_task']
        print(f"[HANDOFF] Backend Coding Task handoff: {config.get('handoff','')}")
        return Task(
            config=config,
            output_file='backend_solution.md'
        )

    @task
    def visualization_task(self) -> Task:
        config = self.tasks_config['visualization_task']
        print(f"[HANDOFF] Visualization Task handoff: {config.get('handoff','')}")
        return Task(
            config=config,
            output_file='visualization.md'
        )
        
    @task
    def manager_task(self) -> Task:
        """Meta-level async delegation, coordination, and reflexive feedback."""
        config = self.tasks_config['manager_task']
        print(f"[HANDOFF] Manager Task handoff: {config.get('handoff','')}")
        return Task(
            config=config,
            output_file='manager_meta_report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the MyCrewProject crew with explicit data/state handoff between agents/tasks"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,  # can be changed to hierarchical as needed
            verbose=True,
            manager_llm=self.llm,
            async_delegation=True,
            allow_agent_delegation=True,
        )
