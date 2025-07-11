#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from my_crew_project.crew import MyCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic':"""You are tasked with building a powerful, user-friendly desktop application that enables users to visually create, configure, and orchestrate AI agents, tasks, and tools utilizing the crewAI framework as the backend for agent and task orchestration, with a modern React.jsx frontend delivering an intuitive GUI. The app must be packaged using a desktop runtime (such as Electron, Tauri, or similar) to ensure cross-platform compatibility. Core features should include modules for agent creation (with configuration and visualization), comprehensive GUI for adding, editing, and deleting tasks and tools, clear assignment and ordering of tasks to agents, and a real-time project visualization dashboard showing agent-task relationships, execution progress, and logs. Implement robust export functionality that allows users to select any output folder and export the entire configured project—including configuration files, source code, and supporting assets—ready for deployment or sharing. The user journey must support starting new or existing projects, using a stepwise, guided interface to create agents, define tasks/tools, visually link tasks to agents and manage dependencies, preview orchestration flows, and finalize exports. Ensure modular code for extensibility (e.g., plug-ins for agent/task types), strict frontend-backend separation, thorough input validation, informative error messages, onboarding guides, and include templates/sample agents/tasks for rapid onboarding. Final deliverables are the complete, production-ready application, full source code, and comprehensive setup/usage/customization documentation. Usability, modularity, and seamless export must be prioritized for future extensibility.""",
        'current_year': str(datetime.now().year)
    }
    
    try:
        MyCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": input("Enter the topic for the crew: "),
        'current_year': str(datetime.now().year)
    }
    try:
        MyCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        MyCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    
    try:
        MyCrew().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
