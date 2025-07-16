#!/usr/bin/env python
import sys
import traceback
import warnings
import os

from datetime import datetime
from dotenv import load_dotenv

from distressed_homes.crew import Distressed_Homes_Crew

# Load environment variables
load_dotenv(dotenv_path='C:\\Users\\Christopher\\projects\\distressed_homes\\.env', override=True)
# This will load the .env file from the current directory or the specified path

# Suppress warnings that are causing noise
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Ensure the results directory exists
results_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "results")
if not os.path.exists(results_dir):
    os.makedirs(results_dir)

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': """Scrape and aggregate real estate data on distressed properties, utilizing multiple sources such as MLS listings, public records, and auction sites; identify and extract distress indicators including pre-foreclosure status, auction postings, tax lien status, price reductions, extended time-on-market, code violations, absentee ownership, and other relevant signs; weight and score each property based on customizable indicator values reflecting investment potential; process, clean, normalize, and deduplicate data, filtering properties with the strongest distress signals; rank the top 20 properties by combined distress and investment score, providing for each a summary of key indicators, market context, and actionable next steps for investment teams (e.g., outreach, due diligence, estimated ROI); output the dashboard, with adaptability for custom markets, indicator weights, and report standards, flagging ambiguous or non-compliant cases for review.""",
        'current_year': str(datetime.now().year),
    }
    
    try:
        crew = Distressed_Homes_Crew().crew()
        result = crew.kickoff(inputs=inputs)
    except Exception as e:
        print("An error occurred while running the crew:")
        traceback.print_exc()  # This prints the full traceback
        raise  # Optionally re-raise the original exception


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs",
        'current_year': str(datetime.now().year)
    }
    try:
        Distressed_Homes_Crew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Distressed_Homes_Crew().crew().replay(task_id=sys.argv[1])

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
        Distressed_Homes_Crew().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")


if __name__ == "__main__":
    run()
